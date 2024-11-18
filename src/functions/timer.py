import json
from threading import Thread
from time import sleep

from loguru import logger

from src.audio.play import play_mp3
from src.config import ee


@ee.on("timer")
def handle_timer(json_arg: str) -> None:
    logger.info("Execute function: Timer")

    seconds = json.loads(json_arg)["seconds"]
    Thread(target=after_seconds, args=(seconds,)).start()

    logger.debug(f"Started timer for {seconds} seconds")


def after_seconds(delay: int):
    sleep(delay)
    # TODO: Play sound

    play_mp3("assets/sounds/timer_finished.mp3")
    logger.debug("Timer finished!")
