class Config(object):
    # Whisper model size (tiny, base, small, medium, large)
    MODEL_WHISPER = "small"
    UPLOAD_FOLDER = "api/uploads"
    MAX_CONTENT_PATH = 10000000  # to set max upload size
    DEVICE = "cuda:0"  # Device to use for inference, "cuda:0" or "cpu"
