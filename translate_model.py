from transformers import pipeline

def get_translation_pipeline(direction="hi-en"):
    print(f"Loading Translation model ({direction})...")

    if direction == "hi-en":
        # Hindi → English
        return pipeline("translation", model="Helsinki-NLP/opus-mt-hi-en")
    elif direction == "en-hi":
        # English → Hindi
        return pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")
    else:
        raise ValueError("Unsupported translation direction")
