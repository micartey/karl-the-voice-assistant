import os
import ffmpeg


def play_wav(filename: str) -> None:
    """
    Initially pyaudio was used, but it keeps having issues with channels etc.
    Therfore we will used the linux build-in "aplay" command

    :param filename: relative path to file including file and extension
    :return: sound
    """
    os.system(f"aplay {filename}")


def play_mp3(filename: str) -> None:
    """
    Translate mp3 to wav as my raspberry pi + setup is only able to play wav files for some weird reason
    :param filename: path to the file (with name)
    :return: sound
    """
    ffmpeg.input(filename).output(f"{filename}.wav").run()
    play_wav(f"{filename}.wav")
