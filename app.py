from flask import Flask, request, render_template, jsonify  # Importa Flask y funciones relacionadas
import os  # Importa el módulo os para interactuar con el sistema operativo
import tempfile  # Importa el módulo tempfile para crear archivos temporales
import librosa  # Importa librosa para la manipulación de audio
import numpy as np  # Importa numpy para el manejo de matrices
from keras.models import load_model  # Importa load_model para cargar el modelo de Keras

# Inicializa la aplicación Flask
app = Flask(__name__)

# Cargar el modelo entrenado
model = load_model('final_model.h5')  # Carga el modelo entrenado desde el archivo 'final_model.h5'

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza el archivo HTML para la página principal

# Ruta para manejar la carga del archivo de audio
@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:  # Verifica si el archivo de audio no está en la solicitud
        return jsonify({"resultado": "Desconocido", "error": "No se ha seleccionado ningún archivo de audio."})  # Devuelve un error si no hay archivo

    audio_file = request.files['audio']  # Obtiene el archivo de audio de la solicitud
    if audio_file.filename == '':  # Verifica si el archivo está vacío
        return jsonify({"resultado": "Desconocido", "error": "El archivo de audio está vacío."})  # Devuelve un error si el archivo está vacío

    if audio_file:  # Si el archivo existe
        temp_dir = tempfile.mkdtemp()  # Crea un directorio temporal
        audio_path = os.path.join(temp_dir, 'temp_audio.wav')  # Define la ruta para el archivo temporal
        audio_file.save(audio_path)  # Guarda el archivo de audio en la ruta temporal

        try:
            # Extraer características de audio
            mfccs = extract_features(audio_path)  # Extrae características MFCC del audio

            # Realizar la predicción
            predicted_class = model.predict(np.expand_dims(mfccs, axis=0))  # Realiza la predicción utilizando el modelo cargado
            predicted_class = np.argmax(predicted_class, axis=1)  # Obtiene la clase predicha

            # Eliminar el archivo temporal después de su procesamiento
            os.remove(audio_path)  # Elimina el archivo temporal

            return jsonify({"resultado": get_tone_rhythm(predicted_class[0]), "error": ""})  # Devuelve el resultado de la predicción
        except Exception as e:  # Captura cualquier excepción que ocurra
            return jsonify({"resultado": "Desconocido", "error": str(e)})  # Devuelve un error en caso de excepción

# Función para extraer características del audio
def extract_features(audio_path):
    audio, sr = librosa.load(audio_path, sr=22050)  # Carga el archivo de audio
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)  # Extrae coeficientes MFCC
    # Ajustar el tamaño de las características
    max_len = 100
    if mfccs.shape[1] > max_len:  # Si la longitud es mayor que max_len
        mfccs = mfccs[:, :max_len]  # Trunca las características
    else:
        pad_width = max_len - mfccs.shape[1]  # Calcula el padding necesario
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')  # Añade padding si es necesario
    return mfccs  # Devuelve las características MFCC ajustadas

# Función para mapear la clase predicha al tono y ritmo correspondiente
def get_tone_rhythm(predicted_class):
    tono_ritmo_mapping = {  # Diccionario para mapear la clase predicha al tono y ritmo
        0: "Rápido Alto",
        1: "Medio Medio",
        2: "Lento Bajo"
    }
    return tono_ritmo_mapping.get(predicted_class, "Desconocido")  # Devuelve el tono y ritmo correspondiente

# Ejecuta la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)  # Ejecuta la aplicación en modo debug
