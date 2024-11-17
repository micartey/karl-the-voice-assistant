import json
from threading import Thread
from time import sleep

from loguru import logger

from src.config import ee


@ee.on("timer")
def handle_alarm(json_arg: str) -> None:
    logger.info("Execute function: Timer")

    seconds = json.loads(json_arg)["seconds"]
    Thread(target=after_seconds, args=(seconds,)).start()

    logger.debug(f"Started timer for {seconds} seconds")


def after_seconds(delay: int):
    sleep(delay)
    # TODO: Play sound
    logger.debug("Timer finished!")
