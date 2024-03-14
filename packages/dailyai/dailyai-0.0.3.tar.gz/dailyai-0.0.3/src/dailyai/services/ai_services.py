import asyncio
import io
import logging
import time
import wave
from dailyai.pipeline.frame_processor import FrameProcessor

from dailyai.pipeline.frames import (
    AudioFrame,
    EndFrame,
    ImageFrame,
    LLMMessagesQueueFrame,
    LLMResponseEndFrame,
    LLMResponseStartFrame,
    LLMFunctionStartFrame,
    LLMFunctionCallFrame,
    Frame,
    TextFrame,
    TranscriptionQueueFrame,
)

from abc import abstractmethod
from typing import AsyncGenerator, AsyncIterable, BinaryIO, Iterable, List


class AIService(FrameProcessor):

    def __init__(self):
        self.logger = logging.getLogger("dailyai")

    def stop(self):
        pass

    async def run_to_queue(
        self, queue: asyncio.Queue, frames, add_end_of_stream=False
    ) -> None:
        async for frame in self.run(frames):
            await queue.put(frame)

        if add_end_of_stream:
            await queue.put(EndFrame())

    async def run(
        self,
        frames: Iterable[Frame] | AsyncIterable[Frame] | asyncio.Queue[Frame],
    ) -> AsyncGenerator[Frame, None]:
        try:
            if isinstance(frames, AsyncIterable):
                async for frame in frames:
                    async for output_frame in self.process_frame(frame):
                        yield output_frame
            elif isinstance(frames, Iterable):
                for frame in frames:
                    async for output_frame in self.process_frame(frame):
                        yield output_frame
            elif isinstance(frames, asyncio.Queue):
                while True:
                    frame = await frames.get()
                    async for output_frame in self.process_frame(frame):
                        yield output_frame
                    if isinstance(frame, EndFrame):
                        break
            else:
                raise Exception("Frames must be an iterable or async iterable")
        except Exception as e:
            self.logger.error("Exception occurred while running AI service", e)
            raise e


class LLMService(AIService):
    """This class is a no-op but serves as a base class for LLM services."""

    def __init__(self):
        super().__init__()


class TTSService(AIService):
    def __init__(self, aggregate_sentences=True):
        super().__init__()
        self.aggregate_sentences: bool = aggregate_sentences
        self.current_sentence: str = ""

    # Some TTS services require a specific sample rate. We default to 16k
    def get_mic_sample_rate(self):
        return 16000

    # Converts the text to audio. Yields a list of audio frames that can
    # be sent to the microphone device
    @abstractmethod
    async def run_tts(self, text) -> AsyncGenerator[bytes, None]:
        # yield empty bytes here, so linting can infer what this method does
        yield bytes()

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, EndFrame):
            if self.current_sentence:
                async for audio_chunk in self.run_tts(self.current_sentence):
                    yield AudioFrame(audio_chunk)
                yield TextFrame(self.current_sentence)

        if not isinstance(frame, TextFrame):
            yield frame
            return

        text: str | None = None
        if not self.aggregate_sentences:
            text = frame.text
        else:
            self.current_sentence += frame.text
            if self.current_sentence.strip().endswith((".", "?", "!")):
                text = self.current_sentence
                self.current_sentence = ""

        if text:
            async for audio_chunk in self.run_tts(text):
                yield AudioFrame(audio_chunk)

            # note we pass along the text frame *after* the audio, so the text frame is completed after the audio is processed.
            yield TextFrame(text)

    # Convenience function to send the audio for a sentence to the given queue
    async def say(self, sentence, queue: asyncio.Queue):
        await self.run_to_queue(
            queue, [LLMResponseStartFrame(), TextFrame(sentence), LLMResponseEndFrame()]
        )


class ImageGenService(AIService):
    def __init__(self, image_size, **kwargs):
        super().__init__(**kwargs)
        self.image_size = image_size

    # Renders the image. Returns an Image object.
    @abstractmethod
    async def run_image_gen(self, sentence: str) -> tuple[str, bytes]:
        pass

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if not isinstance(frame, TextFrame):
            yield frame
            return

        (url, image_data) = await self.run_image_gen(frame.text)
        yield ImageFrame(url, image_data)


class STTService(AIService):
    """STTService is a base class for speech-to-text services."""

    _frame_rate: int

    def __init__(self, frame_rate: int = 16000, **kwargs):
        super().__init__(**kwargs)
        self._frame_rate = frame_rate

    @abstractmethod
    async def run_stt(self, audio: BinaryIO) -> str:
        """Returns transcript as a string"""
        pass

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        """Processes a frame of audio data, either buffering or transcribing it."""
        if not isinstance(frame, AudioFrame):
            return

        data = frame.data
        content = io.BufferedRandom(io.BytesIO())
        ww = wave.open(self._content, "wb")
        ww.setnchannels(1)
        ww.setsampwidth(2)
        ww.setframerate(self._frame_rate)
        ww.writeframesraw(data)
        ww.close()
        content.seek(0)
        text = await self.run_stt(content)
        yield TranscriptionQueueFrame(text, "", str(time.time()))


class FrameLogger(AIService):
    def __init__(self, prefix="Frame", **kwargs):
        super().__init__(**kwargs)
        self.prefix = prefix

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, (AudioFrame, ImageFrame)):
            self.logger.info(f"{self.prefix}: {type(frame)}")
        else:
            print(f"{self.prefix}: {frame}")

        yield frame
