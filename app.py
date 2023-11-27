from flask import Flask, request, render_template, jsonify
import os
import tempfile
import librosa
import numpy as np
from keras.models import load_model

app = Flask(__name__)

# Cargar el modelo entrenado
model = load_model('final_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return jsonify({"resultado": "Desconocido", "error": "No se ha seleccionado ningún archivo de audio."})

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"resultado": "Desconocido", "error": "El archivo de audio está vacío."})

    if audio_file:
        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, 'temp_audio.wav')  # Nombre fijo para el archivo temporal
        audio_file.save(audio_path)

        try:
            # Extraer características de audio
            mfccs = extract_features(audio_path)

            # Realizar la predicción
            predicted_class = model.predict(np.expand_dims(mfccs, axis=0))
            predicted_class = np.argmax(predicted_class, axis=1)

            # Eliminar el archivo temporal después de su procesamiento
            os.remove(audio_path)

            return jsonify({"resultado": get_tone_rhythm(predicted_class[0]), "error": ""})
        except Exception as e:
            return jsonify({"resultado": "Desconocido", "error": str(e)})

def extract_features(audio_path):
    audio, sr = librosa.load(audio_path, sr=22050)  # Cargar el archivo de audio
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)  # Extraer coeficientes MFCC
    # Ajustar el tamaño de las características
    max_len = 100
    if mfccs.shape[1] > max_len:
        mfccs = mfccs[:, :max_len]
    else:
        pad_width = max_len - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
    return mfccs

def get_tone_rhythm(predicted_class):
    # Mapea la clase predicha al tono y ritmo correspondiente
    tono_ritmo_mapping = {
        0: "Rápido Alto",
        1: "Medio Medio",
        2: "Lento Bajo"
    }
    return tono_ritmo_mapping.get(predicted_class, "Desconocido")

if __name__ == '__main__':
    app.run(debug=True)
