import tempfile

from loguru import logger
from openwakeword.model import Model

from src.audio.play import play_wav
from src.audio.record import AudioRecorder
from src.config import (
    AMBIENT_NOISE_LEVEL,
    WAKE_WORD_FILE,
    WAKE_WORD_THRESHOLD,
    DEBUG_WAKE_WORD,
)

model = Model(
    wakeword_models=[f"{WAKE_WORD_FILE}"],
)


def process_predictions(predictions: list) -> float:
    value = 0

    for prediction in predictions:
        for score in prediction.values():
            value = max(float(score), value)

    logger.debug(f"Wake word score: {value}")
    return value


def listen_for_wake_word() -> None:
    """
    Listen for wake word
    :return: True once wake word has been detected
    """
    while True:
        recorder = AudioRecorder(
            min_duration=3,
            silence_duration=1,
            silence_threshold=int(AMBIENT_NOISE_LEVEL),
        )

        stream_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".wav", delete=True)
        recorder.start_recording()

        while recorder.process_stream():
            ...

        recorder.stop_recording()
        recorder.save_recording(stream_file.name)

        if DEBUG_WAKE_WORD:
            play_wav(stream_file.name)

        predictions = model.predict_clip(stream_file.name)

        if process_predictions(predictions) >= float(WAKE_WORD_THRESHOLD):
            break


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
