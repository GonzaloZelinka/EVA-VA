from .whisperListener import WhisperListener
from .wordListener import WakeWordListener


class Listener:
    def __init__(self):
        self.mainListener = WhisperListener()
        self.wwListener = WakeWordListener()
        self.activateWhisper = False
        self.response = None

    def execute(self):
        self.activateWhisper = self.wwListener.execute()
        if self.activateWhisper == True:
            self.response = self.mainListener.execute()
            print("RESPONSE: ", self.response)
        return self.response
