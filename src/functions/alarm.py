from datetime import datetime, timedelta
import json

from loguru import logger

from src.config import ee


@ee.on("alarm")
def handle_alarm(json_arg: str) -> None:
    logger.info("Execute function: Alarm")

    hours = json.loads(json_arg)["hours"]
    minutes = json.loads(json_arg)["minutes"]

    seconds_to_wait = seconds_until_target(hours, minutes)

    ee.emit("timer", json.dumps({"seconds": seconds_to_wait}))

    logger.debug(f"Alarm at {hours}:{minutes}")


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
