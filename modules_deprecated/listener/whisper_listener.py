import sys
from ..api.config import Config
from transformers import pipeline
import pyaudio
import webrtcvad
import numpy as np


class WhisperListener:
    """
    This class is responsible for _listening to the user's voice and
    sending it to the Whisper model for transcription.

    Returns:
        str: The transcription of the user's voice.
    """

    def __init__(self):
        self._vad = webrtcvad.Vad(0)
        self._pa = pyaudio.PyAudio()
        self._FORMAT = pyaudio.paInt16
        self._load_model()
        self._stream = self._pa.open(
            format=self._FORMAT,
            channels=Config.CHANNELS,
            rate=Config.RATE,
            input=True,
            frames_per_buffer=Config.CHUNK_SIZE,
        )

    def _load_model(self):
        print("\033[96mLoading Whisper Model..\033[0m", end="")
        if Config.DEVICE == "cpu":
            print("\033[93m (Warning: Using CPU, this will be slow!)\033[0m")
        self._modelWhisper = pipeline(
            "automatic-speech-recognition",
            model=f"openai/whisper-{Config.MODEL_WHISPER}",
            device=Config.DEVICE,
            generate_kwargs={"task": "transcribe", "language": "<|es|>"},
        )
        print("\033[90m Whisper load complete.\033[0m\n")

    def _listen_and_transcribe(self):
        print("Listening...")
        self._stream.start_stream()
        frames = []
        is_active = False
        silence_frames = 0  # Counter for consecutive non-speaking frames

        # Define a threshold for how many consecutive silent frames are allowed before considering it the end of speech
        silence_threshold = 40  # Adjust this value based on your specific needs

        while True:
            chunk = self._stream.read(Config.CHUNK_SIZE)
            is_speech = self._vad.is_speech(chunk, Config.RATE)
            sys.stdout.write("-" if is_speech else "_")
            if not is_active:
                if is_speech:
                    is_active = True
                    silence_frames = 0
                    print("Start speaking...")
            else:
                if is_speech:
                    silence_frames = 0  # Reset the counter when speech is detected
                    frames.append(chunk)
                else:
                    silence_frames += 1  # Increment the counter for each silent frame
                    if silence_frames < silence_threshold:
                        # Include a short period of silence in the recording
                        frames.append(chunk)
                    else:
                        print("End of speech detected")
                        break

        audio_data = b"".join(frames)
        # Convert raw audio bytes to a numpy array
        # Assuming the audio data is in PCM 16-bit format
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        return self._modelWhisper(audio_array)

    def execute(self):
        try:
            response = self._listen_and_transcribe()
            return response["text"]
        finally:
            self._stream.stop_stream()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._stream.close()
        self._pa.terminate()
