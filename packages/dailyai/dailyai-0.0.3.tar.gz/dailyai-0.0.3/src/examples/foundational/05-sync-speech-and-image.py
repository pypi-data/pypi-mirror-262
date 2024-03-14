import asyncio
from re import S
import aiohttp
import os
import logging

from dataclasses import dataclass
from typing import AsyncGenerator

from dailyai.pipeline.aggregators import (
    GatedAggregator,
    LLMFullResponseAggregator,
    ParallelPipeline,
    SentenceAggregator,
)
from dailyai.pipeline.frames import (
    Frame,
    TextFrame,
    EndFrame,
    ImageFrame,
    LLMMessagesQueueFrame,
    LLMResponseStartFrame,
)
from dailyai.pipeline.frame_processor import FrameProcessor

from dailyai.pipeline.pipeline import Pipeline
from dailyai.services.daily_transport_service import DailyTransportService
from dailyai.services.open_ai_services import OpenAILLMService
from dailyai.services.elevenlabs_ai_service import ElevenLabsTTSService
from dailyai.services.fal_ai_services import FalImageGenService

from examples.support.runner import configure

logging.basicConfig(format=f"%(levelno)s %(asctime)s %(message)s")
logger = logging.getLogger("dailyai")
logger.setLevel(logging.DEBUG)


@dataclass
class MonthFrame(Frame):
    month: str


class MonthPrepender(FrameProcessor):
    def __init__(self):
        self.most_recent_month = "Placeholder, month frame not yet received"
        self.prepend_to_next_text_frame = False

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, MonthFrame):
            self.most_recent_month = frame.month
        elif self.prepend_to_next_text_frame and isinstance(frame, TextFrame):
            yield TextFrame(f"{self.most_recent_month}: {frame.text}")
            self.prepend_to_next_text_frame = False
        elif isinstance(frame, LLMResponseStartFrame):
            self.prepend_to_next_text_frame = True
            yield frame
        else:
            yield frame


async def main(room_url):
    async with aiohttp.ClientSession() as session:
        transport = DailyTransportService(
            room_url,
            None,
            "Month Narration Bot",
            mic_enabled=True,
            camera_enabled=True,
            mic_sample_rate=16000,
            camera_width=1024,
            camera_height=1024,
        )

        tts = ElevenLabsTTSService(
            aiohttp_session=session,
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            voice_id=os.getenv("ELEVENLABS_VOICE_ID"),
        )

        llm = OpenAILLMService(
            api_key=os.getenv("OPENAI_CHATGPT_API_KEY"), model="gpt-4-turbo-preview"
        )

        imagegen = FalImageGenService(
            image_size="square_hd",
            aiohttp_session=session,
            key_id=os.getenv("FAL_KEY_ID"),
            key_secret=os.getenv("FAL_KEY_SECRET"),
        )

        source_queue = asyncio.Queue()

        for month in [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]:
            messages = [
                {
                    "role": "system",
                    "content": f"Describe a nature photograph suitable for use in a calendar, for the month of {month}. Include only the image description with no preamble. Limit the description to one sentence, please.",
                }
            ]
            await source_queue.put(MonthFrame(month))
            await source_queue.put(LLMMessagesQueueFrame(messages))

        await source_queue.put(EndFrame())

        gated_aggregator = GatedAggregator(
            gate_open_fn=lambda frame: isinstance(frame, ImageFrame),
            gate_close_fn=lambda frame: isinstance(frame, LLMResponseStartFrame),
            start_open=False,
        )

        sentence_aggregator = SentenceAggregator()
        month_prepender = MonthPrepender()
        llm_full_response_aggregator = LLMFullResponseAggregator()

        pipeline = Pipeline(
            source=source_queue,
            sink=transport.send_queue,
            processors=[
                llm,
                sentence_aggregator,
                ParallelPipeline(
                    [[month_prepender, tts], [llm_full_response_aggregator, imagegen]]
                ),
                gated_aggregator,
            ],
        )
        pipeline_task = pipeline.run_pipeline()

        other_joined = asyncio.Event()

        @transport.event_handler("on_first_other_participant_joined")
        async def on_first_other_participant_joined(transport):
            other_joined.set()

        async def show_calendar():
            await other_joined.wait()
            await pipeline_task
            await transport.stop_when_done()

        await asyncio.gather(transport.run(), show_calendar())


if __name__ == "__main__":
    (url, token) = configure()
    asyncio.run(main(url))
