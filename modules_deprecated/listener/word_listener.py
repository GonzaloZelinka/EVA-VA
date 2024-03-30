import threading
from vosk import Model, KaldiRecognizer
from ..api.config import Config
import time
import pyaudio


class WakeWordListener:
    """
    This class is responsible for listening to the wake word.

    Returns:
        bool: True if the wake word is detected, False otherwise.

    """

    def __init__(self) -> None:
        print("\033[96mLoading Vosk Model..\033[0m", end="")
        self._model = Model(Config.VOSK_MODEL)
        self._rec = KaldiRecognizer(self._model, Config.RATE)
        print("\033[90m Vosk load complete.\033[0m\n")
        self._FORMAT = pyaudio.paInt16
        self._pa = pyaudio.PyAudio()
        self._stream = self._pa.open(
            format=self._FORMAT,
            channels=Config.CHANNELS,
            rate=Config.RATE,
            input=True,
            frames_per_buffer=8192,
            stream_callback=self.callback,
        )
        self.wake_word_event = threading.Event()

    def callback(self, in_data, frame_count, time_info, status):
        if self._rec.AcceptWaveform(in_data):
            result = self._rec.Result()
            print(result)
            if (
                result[14:-3].upper() in Config.WAKE_WORD
                and result[14:-3] != " "
                and result[14:-3] != ""
            ):
                print("Wake word detected!")
                self.wake_word_event.set()
                return (None, pyaudio.paComplete)
        return (in_data, pyaudio.paContinue)

    def start_stream(self):
        if not self._stream.is_active():
            self._stream.start_stream()

    def stop_stream(self):
        if self._stream.is_active():
            self._stream.stop_stream()
        self.wake_word_event.clear()

    def execute(self):
        self.wake_word_event.wait()  # Wait until the wake word is detected
        self.wake_word_event.clear()  # Reset the event for the next detection
        return True

    def __enter__(self):
        self.start_stream()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_stream()
        self._stream.close()
        self._pa.terminate()
