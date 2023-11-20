import tempfile

import whisper
from loguru import logger

from src.audio.record import AudioRecorder
from src.config import WAKE_WORD, AMBIENT_NOISE_LEVEL


# def listen_for_wake_word() -> bool:
#     """
#     Listen for wake word
#     :return: True once wake word has been detected
#     """
#
#     recognizer = LiveSpeech(sampling_rate=14000)
#
#     for phrase in recognizer:
#         logger.debug(f"Detected: {phrase}")
#
#         #
#         # Check if wake word is in sentence
#         #
#         if WAKE_WORD.lower() in str(phrase).lower():
#             logger.info(f"Detected signal word in sentence: {phrase}")
#             return True
#
#     logger.debug("Stopping...")
#     return False


def listen_for_wake_word() -> None:
    model = whisper.load_model("base")

    while True:
        recorder = AudioRecorder(
            min_duration=3, silence_duration=1, silence_threshold=AMBIENT_NOISE_LEVEL
        )

        stream_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".wav", delete=True)
        recorder.start_recording()

        while recorder.process_stream():
            ...

        recorder.stop_recording()
        recorder.save_recording(stream_file.name)

        audio = whisper.load_audio(stream_file.name)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)

        options = whisper.DecodingOptions(
            fp16=False
        )  # To make it run on a Raspberry PI
        result = whisper.decode(model, mel, options)

        logger.debug(f"Detected text ({max(probs, key=probs.get)}): {result.text}")
        stream_file.close()

        if WAKE_WORD.lower() in result.text.lower():
            logger.info("Wake word detected!")
            break
