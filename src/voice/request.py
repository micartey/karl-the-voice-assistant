from src.audio.record import AudioRecorder


def record_audio_sample(file: str):
    """
    Record audio file until it is silent for a moment
    :param file: wav file
    :return: None
    """

    recorder = AudioRecorder(silence_threshold=20, silence_duration=2, min_duration=2)
    recorder.start_recording()

    while recorder.process_stream():
        ...

    recorder.stop_recording()
    recorder.save_recording(file)
