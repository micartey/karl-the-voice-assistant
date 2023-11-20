from src.audio.record import AudioRecorder
from src.config import AMBIENT_NOISE_LEVEL


def record_audio_sample(file: str) -> None:
    """
    Record audio file until it is silent for a moment
    :param file: wav file
    :return: None
    """

    recorder = AudioRecorder(
        silence_threshold=int(AMBIENT_NOISE_LEVEL),
        silence_duration=2,
        min_duration=2,
    )
    recorder.start_recording()

    while recorder.process_stream():
        ...

    recorder.stop_recording()
    recorder.save_recording(file)
