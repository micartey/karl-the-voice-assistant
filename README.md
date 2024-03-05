# karl-the-voice-assistant

<div align="center">
    <img src=".github/assets/images/banner.png" />
</div>

<br />

<div align="center">
    <img
        src="https://img.shields.io/badge/Written%20in-python-%23F2B655?style=for-the-badge"
        height="30"
    />
</div>

<br />

<p align="center">
  <a href="#-introduction">Introduction</a> •
  <a href="#-getting-started">Getting started</a> •
  <a href="CONCEPT.md">Concept</a> •
  <a href="https://github.com/micartey/karl-the-voice-assistant/issues">Troubleshooting</a>
</p>

## 📚 Introduction


This project is a simple voice assistant that watches for a wake word, plays a sound once the wake word has been recognized and listens for audio input.
The aim of this voice assistant is, to have a voice assistant with the power of OpenAI's GPT and continuous conversations.
The wake word detection is done on the client side and not processed by any cloud provider as per [concept](CONCEPT.md).

### Motivation

I coded this voice assistant, to tackle some goals: 

1. Refactor an old and broken Apple HomePod 1 and build my own voice assistant.
2. Get to know Python development as I am mostly sticking to Java
3. Use AI in an useful manner

### Hardships

The wake word detection is the hardest issue to solve. 
I started with using a local whisper instance and while this worked perfectly, an embedded device such as the Raspberry Pi 4 has to little power to run a whisper model.

I then went on the search for wake word detections that can run on an embedded device and the only good and working solution out there seems to be picovoice.
There are a few things I don't like about this:

- depending on proprietary software for wake words
- they seem to are a [company with bad reputation](https://www.reddit.com/r/cscareerquestionsCAD/comments/qee7zp/picovoice_vancouver_interview_dlsde_roles/)
- they ban users on unknown factors. Just pretend you are canadian - worked fine for me

### TODO

The rough functionality is already implemented, and you can have continues conversations. 
However, there are still some things to do!  

- [ ] Function calling (Useful for smart home solutions)
- [ ] Hide ffmpeg output
- [ ] Alarm clock / Timer

## 🚀 Getting Started

Firstly, clone the repository by executing the following command. This command also takes care of navigating into the repository and deleting the git folder.

```
git clone git@github.com:micartey/karl-the-voice-assistant.git \
    cd karl-the-voice-assistant \
    rm -rf .git
```

Afterward, you can simply execute the following command. `Makefile` should be pre-installed on most linux distros. If this is not the case for you, make sure to install Makefile first.

```shell
make install
```

While executing the setup script, a new `.env` file will be created. Make sure to edit the file, as it will store your api tokens which you need to provide.

Afterward, you can simply start the voice assistant by executing the following command:

```shell
make start
```

You can use a tool like [screen](https://linuxize.com/post/how-to-use-linux-screen/) if you want to run the application in the background.

### Adjust noise level

You might want to adjust the noise level depending on your microphone and ambient noise.
To do this, you first have to figure out, what rms you have. 
This can be done, by setting the following environment flag and restarting the application:

```shell
export DEBUG_RMS=true
```

This will print the rms which will go up if you talk.
Figure out what values are displayed when being silent and what values are displayed when talking.
After you have figured out the value, you can specify it in the `.env` file (default: 20).

### Roles

You can set a role for your voice assistant. Roles are stored in [assets/prompts](https://github.com/micartey/karl-the-voice-assistant/tree/master/assets/prompts) and can easily be created and implemented.
To create a new role, simply create a new json file with the desired name.

```yaml
{
  "role": "Your name is Sarah and you are a helpful assistant that keeps its answers short but informative",
  "voice": "nova" # Checkout https://platform.openai.com/docs/guides/text-to-speech for other voices
}
```

To select a role, simply edit `.env` and set the `ROLE` variable to the filename of the json file.
The python app will automatically look for a json with the same filename in the `prompts` directory.

### Register as a Service

If you are on linux, you can register karl as a service.
This will allow it to automatically start with your device booting up and easier control.
You can also be more specific about logging.

```shell
sudo make service
```

### Wake Word

[Picovoice](https://picovoice.ai/) is a fast and mostly accurate wake word detection and "training" custom models is fast and works without any hardships.
However, custom models run on only the hardware that you selected, which might not be desirable when testing it on e.g. Windows. 
I am fairly certain that this is intentionally as the "training" doesn't even take a second to do and no data at all.