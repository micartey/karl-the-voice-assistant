import tempfile
import copy

from loguru import logger

import src.config as config
from src.audio.play import play_mp3, play_wav
from src.audio.record import AudioRecorder
from src.chat.response import generate_simple_response, generate_response
from src.voice.wake_word import listen_for_wake_word
from src.voice.request import record_audio_sample
from src.voice.synthesize import text_to_speech
from src.voice.transcription import transcripe_audio_file

# Configure input device
AudioRecorder.select_input_device()

# Debug role
logger.debug(config.ROLE)

voice = config.VOICE
messages = [
    {"role": "system", "content": config.ROLE},
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

    # Respond to the transcription of the user
    # TLDR: Answer
    respond_with_audio(transcription, history=messages)


def respond_with_audio(transcription: str, history) -> None:
    # Append request to message history
    history.append({"role": "user", "content": transcription})

    gpt_response = generate_response(history)
    if gpt_response is None:
        logger.debug("Answer has been suppressed")
        return

    logger.debug(gpt_response)

    # Append answer to message history
    history.append({"role": "assistant", "content": gpt_response})

    # Generate audio file and play it
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
