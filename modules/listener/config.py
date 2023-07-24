class Config:
    # Whisper model size (tiny, base, small, medium, large)
    MODEL_WHISPER = "small"

    CHANNELS = 1
    RATE = 16000
    CHUNK_DURATION_MS = 30
    PADDING_DURATION_MS = 1500
    CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)
    CHUNK_BYTES = CHUNK_SIZE * 2
    NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
    NUM_WINDOW_CHUNKS = int(400 / CHUNK_DURATION_MS)
    NUM_WINDOW_CHUNKS_END = NUM_WINDOW_CHUNKS * 2
    START_OFFSET = int(NUM_WINDOW_CHUNKS * CHUNK_DURATION_MS * 0.5 * RATE)

    WAKE_WORD = "EVA"
    VOSK_MODEL = "G:/GIZ_C/Desktop/AVIA/assistant_backend/src/Listener/model/vosk-model-small-es-0.42"
    SAMPLE_RATE_VOSK = 16000
    FRAME_SIZE = 8192
    STREAM_SIZE = 4096
    DEVICE = "cuda:0"  # Device to use for inference, "cuda:0" or "cpu"
