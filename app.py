from flask import Flask, request, jsonify, send_from_directory
import os
import soundfile as sf
from backend.models.translate_model import get_translation_pipeline
from backend.models.tts_model import get_tts_pipeline
from backend.models.stt_model import get_stt_model  # 👈 new import

app = Flask(__name__)

translation_model = get_translation_pipeline()
tts_model = get_tts_pipeline()
stt_model = get_stt_model()  # 👈 load once

STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return send_from_directory(STATIC_FOLDER, 'index.html')

def generate_audio(text, output_path=os.path.join(STATIC_FOLDER, "output.wav")):
    tts_output = tts_model(text)
    audio_array = tts_output['audio'][0]
    sampling_rate = tts_output['sampling_rate']
    sf.write(output_path, audio_array, samplerate=sampling_rate)
    return output_path


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files['audio']
    audio_path = os.path.join(STATIC_FOLDER, 'input_audio.wav')
    audio_file.save(audio_path)

    # Transcribe speech to text
    result = stt_model.transcribe(audio_path)
    text = result['text']

    return jsonify({"text": text})


@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    translated = translation_model(text)[0]['translation_text']
    audio_path = generate_audio(translated)

    return jsonify({
        "translated": translated,
        "audio_url": "/static/output.wav"
    })


if __name__ == '__main__':
    app.run(debug=True)
