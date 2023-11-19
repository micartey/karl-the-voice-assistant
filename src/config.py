import os
import sys

from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI

load_dotenv()

OPENAI_API_TOKEN = os.getenv("OPENAI_API_TOKEN")
WAKE_WORD = os.getenv("WAKE_WORD")
ROLE = os.getenv("ROLE")

logger.add(
    sys.stdout, format="{time} {level} {message}", filter="my_module", level="INFO"
)

logger.add("logs/log_{time}.log", rotation="10 MB", serialize=True)

openai = OpenAI(api_key=OPENAI_API_TOKEN)
