import json
from loguru import logger
from src.config import ee


@ee.on("alarm")
def handle_alarm(json_arg):
    logger.info("Execute function: Alarm")

    minutes = json.loads(json_arg)["minutes"]

    logger.debug(minutes)
