import os  # Importar la librería para interactuar con el sistema operativo
import numpy as np  # Importar la librería NumPy para operaciones numéricas
import librosa  # Importar la librería librosa para procesamiento de audio
from tensorflow import keras  # Importar TensorFlow y Keras para construir el modelo de red neuronal
from keras.models import Sequential  # Importar el modelo secuencial de Keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout  # Importar capas necesarias para la red neuronal
from keras.utils import to_categorical  # Importar la función para convertir etiquetas a codificación one-hot
from sklearn.model_selection import train_test_split  # Importar la función para dividir los datos en conjuntos de entrenamiento y prueba
from sklearn.preprocessing import LabelEncoder  # Importar la clase para codificar etiquetas
from keras.callbacks import ModelCheckpoint  # Importar el callback para guardar el mejor modelo

# Definir las categorías de ritmo y tono
categorias = {
    'rapido_alto': 0,  # Categoría 'rapido_alto' con etiqueta 0
    'medio_medio': 1,  # Categoría 'medio_medio' con etiqueta 1
    'lento_bajo': 2  # Categoría 'lento_bajo' con etiqueta 2
}

# Directorio de los audios
audio_dir = 'C:/Users/Michael/Desktop/Tono-Ritmo/audios'  # Ruta al directorio que contiene los archivos de audio

# Obtener las rutas de los archivos de audio y las etiquetas correspondientes
audio_paths = []  # Lista para almacenar las rutas de los archivos de audio
labels = []  # Lista para almacenar las etiquetas

for categoria, label in categorias.items():  # Iterar sobre cada categoría y su etiqueta
    categoria_dir = os.path.join(audio_dir, categoria)  # Obtener la ruta del directorio de la categoría
    audio_files = os.listdir(categoria_dir)  # Listar los archivos de audio en el directorio de la categoría
    for audio_file in audio_files:  # Iterar sobre cada archivo de audio
        audio_path = os.path.join(categoria_dir, audio_file)  # Obtener la ruta completa del archivo de audio
        audio_paths.append(audio_path)  # Agregar la ruta a la lista
        labels.append(label)  # Agregar la etiqueta a la lista

# Convertir las etiquetas a números enteros
label_encoder = LabelEncoder()  # Crear una instancia del codificador de etiquetas
labels = label_encoder.fit_transform(labels)  # Codificar las etiquetas

# Definir el tamaño deseado para las características MFCC
max_len = 100  # Número máximo de marcos de tiempo para las características MFCC

# Función para extraer características de los audios utilizando librosa
def extract_features(audio_path):
    audio, sr = librosa.load(audio_path, sr=22050)  # Cargar el archivo de audio con una frecuencia de muestreo de 22050 Hz
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)  # Extraer 13 coeficientes MFCC del audio
    # Ajustar el tamaño de las características
    if mfccs.shape[1] > max_len:  # Si el número de marcos de tiempo es mayor que max_len
        mfccs = mfccs[:, :max_len]  # Truncar los marcos de tiempo a max_len
    else:  # Si el número de marcos de tiempo es menor que max_len
        pad_width = max_len - mfccs.shape[1]  # Calcular el número de marcos de tiempo faltantes
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')  # Rellenar con ceros hasta max_len
    return mfccs  # Devolver los coeficientes MFCC ajustados

# Extraer características de los audios y almacenarlos en una matriz
features = []
for audio_path in audio_paths:  # Iterar sobre cada ruta de archivo de audio
    mfccs = extract_features(audio_path)  # Extraer las características MFCC del audio
    features.append(mfccs)  # Agregar las características a la lista
features = np.array(features)  # Convertir la lista de características a un array de NumPy

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)  # Dividir los datos con un 20% para prueba

# Expandir dimensiones para que se ajusten a la entrada de la red neuronal
X_train = np.expand_dims(X_train, axis=-1)  # Expandir dimensiones en el eje final para el conjunto de entrenamiento
X_test = np.expand_dims(X_test, axis=-1)  # Expandir dimensiones en el eje final para el conjunto de prueba

# Convertir las etiquetas a codificación one-hot
y_train = to_categorical(y_train)  # Convertir las etiquetas de entrenamiento a codificación one-hot
y_test = to_categorical(y_test)  # Convertir las etiquetas de prueba a codificación one-hot

# Construir el modelo de la red neuronal
model = Sequential()  # Crear un modelo secuencial
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(X_train.shape[1], X_train.shape[2], 1)))  # Agregar una capa convolucional con 32 filtros
model.add(MaxPooling2D((2, 2)))  # Agregar una capa de agrupamiento máximo
model.add(Conv2D(64, (3, 3), activation='relu'))  # Agregar una segunda capa convolucional con 64 filtros
model.add(MaxPooling2D((2, 2)))  # Agregar una segunda capa de agrupamiento máximo
model.add(Flatten())  # Aplanar las características para conectarlas a la capa densa
model.add(Dense(128, activation='relu'))  # Agregar una capa densa con 128 neuronas
model.add(Dropout(0.5))  # Agregar una capa de dropout para evitar el sobreajuste
model.add(Dense(len(categorias), activation='softmax'))  # Agregar una capa de salida con activación softmax para la clasificación

# Compilar el modelo
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])  # Compilar el modelo con pérdida de entropía cruzada categórica y el optimizador Adam

# Guardar los pesos del modelo con mejor precisión durante el entrenamiento
checkpoint = ModelCheckpoint('model.h5', monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)  # Configurar el checkpoint para guardar el mejor modelo basado en la precisión de validación

# Entrenar el modelo
model.fit(X_train, y_train, batch_size=32, epochs=50, validation_data=(X_test, y_test), callbacks=[checkpoint])  # Entrenar el modelo con los datos de entrenamiento y validación

# Guardar el modelo entrenado
model.save('final_model.h5')  # Guardar el modelo final entrenado
