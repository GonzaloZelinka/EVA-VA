from flask import Flask
from transformers import pipeline


class AudioService:

    def __init__(self, app: Flask) -> None:
        self.app = app
        self._load_model()

    def _load_model(self):
        print("\033[96mLoading Whisper Model..\033[0m", end="")
        if self.app.config["DEVICE"] == "cpu":
            print("\033[93m (Warning: Using CPU, this will be slow!)\033[0m")
        self._modelWhisper = pipeline(
            "automatic-speech-recognition",
            model=f"openai/whisper-{self.app.config['MODEL_WHISPER']}",
            device=self.app.config["DEVICE"],
            generate_kwargs={"task": "transcribe", "language": "<|es|>"},
        )
        print("\033[90m Whisper load complete.\033[0m\n")

    def transcribe_audio_file(self, audio_file_path):
        return self._modelWhisper(audio_file_path)
