import audioop

import pyaudio

pyaudio_instance = pyaudio.PyAudio()
print("Available input devices:")
for i in range(pyaudio_instance.get_device_count()):
    dev = pyaudio_instance.get_device_info_by_index(i)
    if dev["maxInputChannels"] > 0:
        print(f"{i}: {dev['name']}")

# User selects the device
selected_device_index = int(input("Enter the number of the desired input device: "))
pyaudio_instance.terminate()


def main() -> None:
    chunk_size = 4096

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=48000,
        input=True,
        input_device_index=selected_device_index,
        frames_per_buffer=chunk_size,
    )

    while True:
        data = stream.read(chunk_size)
        rms = audioop.rms(data, 2)

        print(rms)


if __name__ == "__main__":
    main()
