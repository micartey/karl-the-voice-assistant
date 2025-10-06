import json
from threading import Thread
from time import sleep

from loguru import logger

from src.audio.play import play_mp3
from src.chat.response import generate_simple_response
from src.config import ee
from src.main import messages
from src.voice.synthesize import text_to_speech_simple


@ee.on("timer")
def handle_alarm(json_arg: str) -> None:
    logger.info("Execute function: Timer")

    seconds = json.loads(json_arg)["seconds"]
    Thread(target=after_seconds, args=(seconds,)).start()

    logger.debug(f"Started timer for {seconds} seconds")

    messages.append({"role": "user", "content": f"Tell me in the bevor used language that an timer has been set for ${seconds} seconds"})
    play_mp3(text_to_speech_simple(generate_simple_response(messages)).name)


def after_seconds(delay: int):
    sleep(delay)
    # TODO: Play sound
    logger.debug("Timer finished!")
