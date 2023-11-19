import pyaudio
import wave
import pygame
import time


def play_wav(filename):
    # Open the WAV file
    wf = wave.open(filename, "rb")

    # Create a PyAudio instance
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )

    # Read data in chunks
    chunk_size = 1024
    data = wf.readframes(chunk_size)

    # Play the audio
    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Close the stream and PyAudio instance
    stream.stop_stream()
    stream.close()
    p.terminate()


def play_mp3(filename):
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(filename)

    # Play the MP3 file
    pygame.mixer.music.play()

    # Wait for the music to play
    while pygame.mixer.music.get_busy():
        time.sleep(1)
