from vosk import Model, KaldiRecognizer
from .config import Config
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
            start=False,
            frames_per_buffer=8192,
        )

    def __exit__(self):
        self._stream.stop_stream()
        self._stream.close()

    def execute(self):
        self._stream.start_stream()
        while True:
            data = self._stream.read(4096)

            if self._rec.AcceptWaveform(data):
                result = self._rec.Result()
                print(result)
                if (
                    result[14:-3].upper() in Config.WAKE_WORD
                    and result[14:-3] != " "
                    and result[14:-3] != ""
                ):
                    print("Wake word detected!")
                    return True
            time.sleep(0.20)
