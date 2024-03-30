from dotenv import load_dotenv
from openai import OpenAI
from modules.executionController.execution_controller import ExecutionController
from modules.listener.word_listener import WakeWordListener
import time
import threading
from queue import Queue

load_dotenv()


def wake_word_listener(
    ww_listener: WakeWordListener,
    command_queue: Queue,
    wake_word_detected_flag: threading.Event,
):
    while True:
        activate_whisper = ww_listener.execute()
        print("check activate_whisper", activate_whisper)
        if activate_whisper:
            print("WAKE WORD DETECTED!")
            wake_word_detected_flag.set()  # Set the flag when wake word is detected

            # Try to acquire the lock without blocking; if successful, the command processor is not busy
            if execution_lock.acquire(blocking=False):
                print("EXECUTION CONTROLLER IS FREE!")
                # Put a command in the queue for the command processor to execute
                command_queue.put(True)
                # Important: The lock is not released here; it's released by the command processor after execution
            else:
                print("EXECUTION CONTROLLER IS BUSY!")
                # Execution controller is busy; you might want to handle this case (e.g., play a busy tone or LED indication)
                pass
        # Small delay to prevent this loop from consuming too much CPU
        time.sleep(0.20)


def command_processor(
    command_queue: Queue,
    execution_lock: threading.Lock,
    execution_controller: ExecutionController,
    wake_word_detected_flag: threading.Event,
):
    while True:
        # Block until a command is available in the queue
        command_queue.get()
        try:
            print("STARTING EXECUTION...")
            execution_controller.execute()
        finally:
            # Always release the lock once execution is complete
            print("FINISHED EXECUTION, WAITING FOR WAKE WORD...")
            execution_lock.release()  # Release the lock once execution is complete
            wake_word_detected_flag.clear()  # Clear the flag after execution


if __name__ == "__main__":
    open_ai = OpenAI()
    execution_controller = ExecutionController(open_ai)
    ww_listener = WakeWordListener()

    command_queue = Queue()
    execution_lock = threading.Lock()
    wake_word_detected_flag = threading.Event()  # Flag to indicate wake word detection

    # Setting up and starting threads
    ww_thread = threading.Thread(
        target=wake_word_listener,
        args=(ww_listener, command_queue, wake_word_detected_flag),
    )
    cp_thread = threading.Thread(
        target=command_processor,
        args=(
            command_queue,
            execution_lock,
            execution_controller,
            wake_word_detected_flag,
        ),
    )

    # Setting threads as daemon so they will automatically close when the main thread terminates
    ww_thread.daemon = True
    cp_thread.daemon = True

    ww_thread.start()
    cp_thread.start()

    try:
        # Wait for threads to complete their tasks. They will run indefinitely until an exception occurs.
        ww_thread.join()
        cp_thread.join()
    except KeyboardInterrupt:
        print("\nExecution interrupted by user. Exiting...")
        # Any additional cleanup can be done here
