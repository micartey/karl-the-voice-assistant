import audioop

import pyaudio


def main():
    chunk_size = 4096

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=chunk_size,
    )

    while True:
        data = stream.read(chunk_size)
        rms = audioop.rms(data, 2)

        print(rms)


if __name__ == "__main__":
    main()
