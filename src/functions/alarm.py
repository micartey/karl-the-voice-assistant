import json
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from loguru import logger

from src.audio.play import play_mp3
from src.chat.response import generate_simple_response
from src.config import ee
from src.main import messages
from src.voice.synthesize import text_to_speech_simple


@ee.on("alarm")
def handle_alarm(json_arg: str) -> None:
    logger.info("Execute function: Alarm")

    hours = json.loads(json_arg)["hour"]
    minutes = json.loads(json_arg)["minute"]

    seconds_to_wait = seconds_until_target(hours, minutes)
    Thread(target=after_seconds, args=(seconds_to_wait,)).start()

    logger.debug(f"Alarm at {hours}:{minutes}")

    # Answer the user that an alarm has been set
    messages.append({"role": "user", "content": f"Tell me in the bevor used language that an alarm has been set to ${hours}:${minutes}"})
    play_mp3(text_to_speech_simple(generate_simple_response(messages)).name)


def after_seconds(delay: int):
    sleep(delay)
    # TODO: Play sound
    logger.debug("Alarm finished!")


def seconds_until_target(hour, minute):
    now = datetime.now()
    today_target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if today_target > now:
        target_time = today_target
    else:
        # Target time is for the next day
        target_time = today_target + timedelta(days=1)

    delta = target_time - now
    return int(delta.total_seconds())
