from modules.executionController.execution_controller import ExecutionController
from modules.listener.word_listener import WakeWordListener
import time

if __name__ == "__main__":
    execution_controller = ExecutionController()
    ww_listener = WakeWordListener()
    while True:
        activate_whisper = ww_listener.execute()
        if activate_whisper:
            execution_controller.execute()
            print("FINISHED EXECUTION, WAITING FOR WAKE WORD...")
            activate_whisper = False
        time.sleep(0.20)
