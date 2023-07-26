from .whisper_listener import WhisperListener
from .word_listener import WakeWordListener


class Listener:
    def __init__(self):
        self._mainListener = WhisperListener()
        self._wwListener = WakeWordListener()
        self._activateWhisper = False
        self._response = None

    def execute(self):
        self._activateWhisper = self._wwListener.execute()
        if self._activateWhisper == True:
            self._response = self._mainListener.execute()
        return self._response
