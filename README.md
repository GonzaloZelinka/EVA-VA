# Personal Assistant Backend

A personal assistant with help of AI. The goal is to have a module easy to use in different backend environments, like in a API.

### Create a python env

```bash
# For mac
$ python3 -m virtualenv -p Python39 .venv
# For windows
$ python -m virtualenv -p='path-to-python' .venv
```

Start the env

```bash
# For mac
$ source .venv/bin/activate
# For windows
$ source .venv/Scripts/activate
```

### Install Python dependencies

1. Install [PyTorch](https://pytorch.org/get-started/locally/)

```bash
$ pip install -r requirements.txt
```

### Download models

Download [Vosk small model](https://alphacephei.com/vosk/models) inside a folder called `model` in src/listener/model

## Use Cases

- [ ] Create reminders

## Capabilities:

- [x] Speech recognition.
- [ ] Tasks Management.
- [ ] Response doubts to the user.
- [ ] Send messages and remember reminders.
- [ ] Send all responses to telegram bot.

## Models used

- Google Text To Speech.
- Whisper.
- GPT-4 for complex request.
- GPT-3.5 for simple request.

## Workflow and documentation of the project

- [Doc](https://drive.google.com/drive/folders/1Nnn7RBA9Lzi_jqQynN_inBtx3IYG7OLu?usp=sharing)
