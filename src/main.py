import tempfile

from loguru import logger

import src.config as config
from src.audio.play import play_mp3, play_wav
from src.parser.prompt import Prompt
from src.voice.wake_word import listen_for_wake_word
from src.voice.request import record_audio_sample
from src.voice.response import generate_response
from src.voice.synthesize import text_to_speech
from src.voice.transcription import transcripe_audio_file

# Read System Role Prompt and Voice Data
prompt = Prompt.load_from_json(config.ROLE)
logger.debug(prompt)

voice = prompt.voice
messages = [
    {"role": "system", "content": prompt.role},
]


def on_signal():
    play_wav("assets/sounds/listening.wav")

    request_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".wav", delete=True)
    record_audio_sample(request_file.name)
    transcription = transcripe_audio_file(request_file.name)
    request_file.close()

    # TODO: Play record finish sound

    # Append request to message history
    messages.append({"role": "user", "content": transcription})

    gpt_response = generate_response(messages)
    logger.debug(gpt_response)

    # Append answer to message history
    messages.append({"role": "assistant", "content": gpt_response})

    response_file = text_to_speech(gpt_response, voice)
    play_mp3(response_file.name)


def main():
    # Detect wake word, can be configured setting WAKE_WORD environment variable
    while True:
        listen_for_wake_word()
        logger.info("Signal word detected... Start recording")
        on_signal()


if __name__ == "__main__":
    # main()
    play_mp3("assets/sounds/response.mp3")
