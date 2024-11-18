import importlib
import os
import sys

from pymitter import EventEmitter
from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI

# Load .env file
load_dotenv()

#
# Configure logging
#
logger.add(
    sys.stdout, format="{time} {level} {message}", filter="my_module", level="INFO"
)
logger.add("logs/log_{time}.log", rotation="10 MB", serialize=True)

#
# Environment variables
#
OPENAI_API_TOKEN = os.getenv("OPENAI_API_TOKEN")
PICOVOICE_API_TOKEN = os.getenv("PICOVOICE_API_TOKEN")

WAKE_WORD_FILE = os.getenv("WAKE_WORD_FILE")
GPT_MODEL = os.getenv("GPT_MODEL")
ROLE = os.getenv("ROLE")

AMBIENT_NOISE_LEVEL = os.getenv("AMBIENT_NOISE_LEVEL")
SAMPLE_RATE = os.getenv("SAMPLE_RATE")
CHUNK_SIZE = os.getenv("CHUNK_SIZE")

DEBUG_RMS = os.getenv("DEBUG_RMS")

#
# Objects
#
openai = OpenAI(api_key=OPENAI_API_TOKEN)

abort_prompt = [
    {
        "role": "system",
        "content": "You will be provided with some words or sentences. If the sentence goes into "
        'the direction to abort, stop or to be silent: Return "Y". Else Return "N"',
    },
]

ee = EventEmitter()


def import_functions(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            module_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)


import_functions("src/functions")
