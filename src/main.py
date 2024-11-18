import tempfile
import copy

from loguru import logger

import src.config as config
from src.audio.play import play_mp3, play_wav
from src.audio.record import AudioRecorder
from src.chat.response import generate_simple_response, generate_response
from src.parser.prompt import Prompt

from src.voice.wake_word import listen_for_wake_word
from src.voice.request import record_audio_sample
from src.voice.synthesize import text_to_speech
from src.voice.transcription import transcripe_audio_file

# Configure input device
AudioRecorder.select_input_device()

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

    # Check for abort - In case of an abort, abort_state will equal "Y" for Yes
    abort_prompt = copy.deepcopy(config.abort_prompt)
    abort_prompt.append({"role": "user", "content": transcription})

    if generate_simple_response(abort_prompt).upper() == "Y":
        # TODO: Play abort sound
        return

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
        logger.info("Wake word detected!")
        on_signal()


if __name__ == "__main__":
    try:
        main()  # Main loop

    # Terminate
    except KeyboardInterrupt:
        logger.warning("Interupting...")
