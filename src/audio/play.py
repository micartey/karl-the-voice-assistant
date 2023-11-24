import wave
import pyaudio
import ffmpeg


def play_wav(filename: str) -> None:
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


def play_mp3(filename: str) -> None:
    """
    Translate mp3 to wav as my raspberry pi is only able to play wav files for some weird reason
    :param filename: path to the file (with name)
    :return: sound
    """
    ffmpeg.input(filename).output(f"{filename}.wav").run()
    play_wav(f"{filename}.wav")
