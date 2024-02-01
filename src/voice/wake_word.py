import struct

import pvporcupine
import pyaudio
from loguru import logger

from src.config import (
    PICOVOICE_API_TOKEN,
    WAKE_WORD_FILE,
)

picovoice = pvporcupine.create(
    access_key=PICOVOICE_API_TOKEN,
    keyword_paths=[f"{WAKE_WORD_FILE}"]
    # keywords=["ok google"]
)


def listen_for_wake_word() -> None:
    """
    Listen for wake word
    :return: finishes once word has been detected
    """

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=picovoice.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=picovoice.frame_length
    )

    while True:
        pcm = audio_stream.read(picovoice.frame_length)
        pcm = struct.unpack_from("h" * picovoice.frame_length, pcm)

        keyword_index = picovoice.process(pcm)
        if keyword_index >= 0:
            # Wake word detected, abort loop
            break

    audio_stream.stop_stream()
    audio_stream.close()
    pa.terminate()

#         audio = whisper.load_audio(stream_file.name)
#         audio = whisper.pad_or_trim(audio)
#
#         mel = whisper.log_mel_spectrogram(audio).to(model.device)
#         _, probs = model.detect_language(mel)
#
#         options = whisper.DecodingOptions(
#             fp16=False
#         )  # To make it run on a Raspberry PI
#         result = whisper.decode(model, mel, options)
#
#         logger.debug(f"Detected text ({max(probs, key=probs.get)}): {result.text}")
#         stream_file.close()
#
#         if WAKE_WORD.lower() in result.text.lower():
#             logger.info("Wake word detected!")
#             break
