import tempfile

from loguru import logger
from openwakeword.model import Model

from src.audio.record import AudioRecorder
from src.config import AMBIENT_NOISE_LEVEL, WAKE_WORD_FILE

model = Model(
    wakeword_models=[f"{WAKE_WORD_FILE}"],
)


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

        predictions = model.predict_clip(stream_file.name)
        logger.debug("Debugging predictions")

        def process_predictions() -> int:
            matches = 0

            for prediction in predictions:
                for score in prediction.values():
                    if float(score) < 0.005:
                        continue

                    logger.info(f"Detected wake word with score of {score}")
                    matches += 1

            logger.debug(f"Found {matches} matches")
            return matches

        if process_predictions() >= 1:
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
