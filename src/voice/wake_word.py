import pvrecorder
from loguru import logger


import openwakeword
from openwakeword.model import Model

openwakeword.utils.download_models()
model = Model(
    # wakeword_models=[f"{WAKE_WORD_FILE}"],
)


def listen_for_wake_word() -> None:
    """
    Listen for wake word
    :return: True once wake word has been detected
    """
    recorder = pvrecorder.PvRecorder(device_index=-1, frame_length=16_000)

    recorder.start()

    logger.info("Listening for wake word")

    while True:
        pcm = recorder.read()
        prediction = model.predict(pcm)

        print(prediction)

    recorder.delete()


# def listen_for_wake_word() -> None:
#     model = whisper.load_model("base")
#
#     while True:
#         recorder = AudioRecorder(
#             min_duration=3,
#             silence_duration=1,
#             silence_threshold=int(AMBIENT_NOISE_LEVEL),
#         )
#
#         stream_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".wav", delete=True)
#         recorder.start_recording()
#
#         while recorder.process_stream():
#             ...
#
#         recorder.stop_recording()
#         recorder.save_recording(stream_file.name)
#
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
