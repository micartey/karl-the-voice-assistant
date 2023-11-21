import time

from playsound import playsound


def main() -> None:
    while True:
        print("Playing sound...")
        playsound("assets/sounds/listening.wav")
        time.sleep(2)


if __name__ == "__main__":
    main()
