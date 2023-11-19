import audioop
import time
import wave

import pyaudio
from loguru import logger


class AudioRecorder:
    def __init__(self, min_duration=5, silence_threshold=500, silence_duration=4):
        self.chunk_size = 4096
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration

        self.min_duration = min_duration
        self.recording_start = None

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.last_sound_time = time.time()

    def start_recording(self):
        self.stream = self.audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        self.frames = []
        self.last_sound_time = time.time()
        self.recording_start = time.time()

        logger.info("Start recording audio")

    def process_stream(self):
        data = self.stream.read(self.chunk_size)
        self.frames.append(data)

        # Check volume
        rms = audioop.rms(data, 2)
        if rms > self.silence_threshold:
            self.last_sound_time = time.time()
            return True

        if time.time() - self.recording_start < self.min_duration:
            return True

        if time.time() - self.last_sound_time > self.silence_duration:
            return False

        return True

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        logger.info("Stop recording audio")

    def save_recording(self, filename):
        wave_file = wave.open(filename, "wb")
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.audio.get_sample_size(self.audio_format))
        wave_file.setframerate(self.sample_rate)
        wave_file.writeframes(b"".join(self.frames))
        wave_file.close()

        logger.info(f"Save audiofile to {filename}")
