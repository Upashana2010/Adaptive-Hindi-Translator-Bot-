import whisper

_model = None

def get_stt_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")  # try "small" or "medium" for better accuracy
    return _model
