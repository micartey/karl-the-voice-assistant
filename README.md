# karl-the-voice-assistant

<div align="center">
    <img src="assets/images/banner.png" />
</div>

<br />

<div align="center">
    <img
        src="https://img.shields.io/badge/Written%20in-python-%23F2B655?style=for-the-badge"
        height="30"
    />
    <a href="https://discord.gg/fxTn7v8">
        <img 
            src="https://img.shields.io/discord/647922123192533022?color=212121&label=Discord&logo=discord&logoColor=212121&style=for-the-badge"
            height="30"
        />
    </a>
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
The aim of this voice assistant is, to have a voice assistant with the power of OpenAI's GPT and continouse conversations.
The wake word detection is done on the client side and not processed by any cloud provider.

### Motivation

I coded this voice assistant, to tackle two goals: 

1. Refactor an old and broken Apple HomePod 1 and build my own smart home / voice assistant.
2. Get to know Python development as I am mostly sticking to Java
3. Use AI in a useful manner

### Hardships

The wake word detection is the hardest issue to solve. 
It still is not perfect and uses a local whisper instance to check for the wake word.
Using a local whisper instance doesn't really work on a Raspberry Pi and takes tens of seconds to decode.

A second possibility is to use pocketsphinx - This seems to work on a Raspberry Pi, **however**, it is very limited and inaccuarte.
Both not good traits for a wake word detection

## 🚀 Getting Started

Firstly, clone the repository by executing the following command. This command also takes care of navigating into the repository and deleting the git folder.

```
git clone git@github.com:micartey/karl-the-voice-assistant.git \
    cd karl-the-voice-assistant \
    rm -rf .git
```

Afterward, you can simply execute the following command. `Makefile` should be pre-installed on most linux distros. If this is not the case for you, make sure to install Makefile first.

```shell
make setup
```

While executing the setup script, a new `.env` file will be created. Make sure to edit the file, as it will store your `OPENAI_API_TOKEN` which you need to provide.

Afterward, you can simply start the voice assistant by executing the following command:

```shell
make start
```

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

### Wake Word

You can choose a wake word to trigger the voice assistant to listen and process the next sentence(s).
The wake word can be configured in the `.env` file as well, by setting `WAKE_WORD` to a disired word / name.
Some words work better than others, so this step requires some trial and error.