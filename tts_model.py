from transformers import pipeline

def get_tts_pipeline():
    print("Loading TTS model...")

    # Using a supported model
    return pipeline("text-to-speech", model="suno/bark-small")

