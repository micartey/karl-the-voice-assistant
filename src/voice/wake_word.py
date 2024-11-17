import subprocess
import time

import pvporcupine
from pvrecorder import PvRecorder

from src.audio.record import AudioRecorder
from src.config import (
    PICOVOICE_API_TOKEN,
    WAKE_WORD_FILE,
)

picovoice = pvporcupine.create(
    access_key=PICOVOICE_API_TOKEN,
    keyword_paths=[f"{WAKE_WORD_FILE}"],
    sensitivities=[0.5],
)


def listen_for_wake_word() -> None:
    """
    Listen for wake word
    :return: finishes once word has been detected and microphone has been freed
    """

    recorder = PvRecorder(
        frame_length=picovoice.frame_length,
        device_index=AudioRecorder.selected_device_index,
    )
    recorder.start()

    while True:
        pcm = recorder.read()

        keyword_index = picovoice.process(pcm)
        if keyword_index >= 0:
            # Wake word detected, abort loop
            break

    recorder.stop()
    recorder.delete()

    """
    Wait until microphone has been freed
    """
    while True:
        time.sleep(0.05)

        # Get the status for **ALL** microphones
        result = subprocess.getoutput(
            "find /proc/asound -name status -exec grep -v closed {} +"
        )

        if len(result) == 0:
            break
