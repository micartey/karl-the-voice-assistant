import audioop
import time
import wave
import sounddevice
import pyaudio

from loguru import logger

from src import config

# This line serves no purpose except to hide the ALSA errors. Don't ask me why this works
# https://github.com/Uberi/speech_recognition/issues/182#issuecomment-1426939447
_ = sounddevice.default


class AudioRecorder:
    # Class variable to store the selected device index
    selected_device_index = None

    @staticmethod
    def select_input_device():
        pyaudio_instance = pyaudio.PyAudio()

        available_microphones = [
            (i, pyaudio_instance.get_device_info_by_index(i)["name"])
            for i in range(pyaudio_instance.get_device_count())
            if pyaudio_instance.get_device_info_by_index(i)["maxInputChannels"] > 0
        ]

        if len(available_microphones) <= 1:
            AudioRecorder.selected_device_index = (
                available_microphones[0][0] if available_microphones else -1
            )

            logger.debug(f"Selected {available_microphones[0][1]}")

        else:
            print(
                "Multiple input devices detected. Please specify which device you want to use:"
            )

            # Print a list of available microphones
            for index, name in available_microphones:
                print(f"{index}: {name}")

            AudioRecorder.selected_device_index = int(
                input("Enter the number of the desired input device: ")
            )

        pyaudio_instance.terminate()

    def __init__(self, min_duration=5, silence_threshold=500, silence_duration=4):
        self.chunk_size = int(config.CHUNK_SIZE)
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = int(config.SAMPLE_RATE)
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration

        self.min_duration = min_duration
        self.recording_start = None

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.last_sound_time = time.time()

    def start_recording(self) -> None:
        while True:
            try:
                self.stream = self.audio.open(
                    format=self.audio_format,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    input_device_index=AudioRecorder.selected_device_index,
                    frames_per_buffer=self.chunk_size,
                )

                self.frames = []
                self.last_sound_time = time.time()
                self.recording_start = time.time()

                logger.info("Start recording audio")
                break

            except OSError:
                logger.error("Failed to open device. Try again...")

    def process_stream(self) -> bool:
        data = self.stream.read(self.chunk_size, exception_on_overflow=False)
        self.frames.append(data)

        # Check volume
        rms = audioop.rms(data, 2)

        if config.DEBUG_RMS:
            logger.debug(f"RMS: {rms}")

        if rms > self.silence_threshold:
            self.last_sound_time = time.time()
            return True

        if time.time() - self.recording_start < self.min_duration:
            return True

        if time.time() - self.last_sound_time > self.silence_duration:
            return False

        return True

    def stop_recording(self) -> None:
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        logger.info("Stop recording audio")

    def save_recording(self, filename) -> None:
        wave_file = wave.open(filename, "wb")
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.audio.get_sample_size(self.audio_format))
        wave_file.setframerate(self.sample_rate)
        wave_file.writeframes(b"".join(self.frames))
        wave_file.close()

        logger.info(f"Save audiofile to {filename}")
