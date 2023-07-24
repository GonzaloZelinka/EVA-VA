import time
import os
from .config import Config
from transformers import pipeline
import pyaudio
import webrtcvad
import signal
import collections
import array
import sys
import wave
from struct import pack


class WhisperListener:

    """
    This class is responsible for listening to the user's voice and
    sending it to the Whisper model for transcription.

    Returns:
        str: The transcription of the user's voice.
    """

    def __init__(self, assist=None):
        self._vad = webrtcvad.Vad(1)
        self._pa = pyaudio.PyAudio()
        self._FORMAT = pyaudio.paInt16
        self.__load_model()
        self._stream = self._pa.open(
            format=self._FORMAT,
            channels=Config.CHANNELS,
            rate=Config.RATE,
            input=True,
            start=False,
            frames_per_buffer=Config.CHUNK_SIZE,
        )

        self.got_a_sentence = False
        self.leave = False

    def __load_model(self):
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

    def process(self):
        print("\n\033[90mTranscribing..\033[0m")
        result = self._modelWhisper("dictate.wav")
        print("\033[92mTranscription complete.\033[0m\n")
        return result

    def record_to_file(self, path, data, sample_width):
        data = pack("<" + ("h" * len(data)), *data)
        wf = wave.open(path, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(Config.RATE)
        wf.writeframes(data)
        wf.close()

    def normalize(self, snd_data):
        MAXIMUM = 32767
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)
        r = array.array("h")
        for i in snd_data:
            r.append(int(i * times))
        return r

    def _close_stream(self, start_point, raw_data):
        self._stream.stop_stream()
        print("* done recording")
        self.got_a_sentence = False

        raw_data.reverse()
        for index in range(start_point):
            raw_data.pop()
        raw_data.reverse()
        raw_data = self.normalize(raw_data)
        self.record_to_file("dictate.wav", raw_data, 2)

    def handle_int(self, sig, chunk):
        self.leave = True
        self.got_a_sentence = True

    def listen(self):
        signal.signal(signal.SIGINT, self.handle_int)
        while not self.leave:
            ring_buffer = collections.deque(maxlen=Config.NUM_PADDING_CHUNKS)
            triggered = False
            ring_buffer_flags = [0] * Config.NUM_WINDOW_CHUNKS
            ring_buffer_index = 0
            ring_buffer_flags_end = [0] * Config.NUM_WINDOW_CHUNKS_END
            ring_buffer_index_end = 0
            raw_data = array.array("h")
            index = 0
            start_point = 0
            StartTime = time.time()
            print("Listening...")
            self._stream.start_stream()

            while not self.got_a_sentence and not self.leave:
                chunk = self._stream.read(Config.CHUNK_SIZE)
                raw_data.extend(array.array("h", chunk))
                index += Config.CHUNK_SIZE
                TimeUse = time.time() - StartTime

                active = self._vad.is_speech(chunk, Config.RATE)
                sys.stdout.write("1" if active else "_")
                ring_buffer_flags[ring_buffer_index] = 1 if active else 0
                ring_buffer_index += 1
                ring_buffer_index %= Config.NUM_WINDOW_CHUNKS
                ring_buffer_flags_end[ring_buffer_index_end] = 1 if active else 0
                ring_buffer_index_end += 1
                ring_buffer_index_end %= Config.NUM_WINDOW_CHUNKS_END

                if not triggered:
                    ring_buffer.append(chunk)
                    num_voiced = sum(ring_buffer_flags)
                    if num_voiced > 0.8 * Config.NUM_WINDOW_CHUNKS:
                        sys.stdout.write(" Open ")
                        triggered = True
                        start_point = index - Config.CHUNK_SIZE * 20
                        ring_buffer.clear()
                else:
                    ring_buffer.append(chunk)
                    num_unvoiced = Config.NUM_WINDOW_CHUNKS_END - sum(
                        ring_buffer_flags_end
                    )
                    if num_unvoiced > 0.90 * Config.NUM_WINDOW_CHUNKS_END:
                        sys.stdout.write(" Close ")
                        triggered = False
                        self.got_a_sentence = True

                sys.stdout.flush()

            sys.stdout.write("\n")
            self._close_stream(start_point, raw_data)
            self.leave = True

        self._stream.close()
        return self.process()

    def execute(self):
        response = self.listen()
        if os.path.exists("dictate.wav"):
            os.remove("dictate.wav")
        return response
