import spacy  # Importar la librería de procesamiento de lenguaje natural
import speech_recognition as sr  # Importar la librería de reconocimiento de voz

# Cargar el modelo de lenguaje en español
nlp = spacy.load("es_core_news_sm")  # Cargar el modelo de lenguaje en español de spaCy

# Definir las etapas de la conversación
etapas = [
    "es un gusto tenerlo en crea",  # Etapa 1
    "mi nombre es ",  # Etapa 2
    "estoy buscando un sofá, colchón mueble",  # Etapa 3
    "es para cambiar uno que ya tiene",  # Etapa 4
    "es para usted",  # Etapa 5
    "con mucho gusto siga y permítame mostrarle los últimos diseño",  # Etapa 6
    "tenemos muebles cómodos y confortables"  # Etapa 7
]

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()  # Crear una instancia del reconocedor de voz

# Inicializar el sintetizador de voz 
from gtts import gTTS  # Importar la librería para convertir texto a voz
import os  # Importar la librería para interactuar con el sistema operativo

def speak(text):
    tts = gTTS(text, lang="es")  # Crear un objeto gTTS con el texto y el idioma español
    tts.save("response.mp3")  # Guardar el audio generado en un archivo MP3
    os.system("mpg321 response.mp3")  # Reproducir el archivo MP3

# Configurar el micrófono como fuente de entrada
with sr.Microphone() as source:  # Utilizar el micrófono como la fuente de audio
    print("¡Hable con el asesor!")  # Indicar al usuario que puede empezar a hablar

    for i, etapa in enumerate(etapas):  # Iterar sobre cada etapa de la conversación
        # Esperar a que el asesor hable y transcribir su respuesta
        print(f"Asesor: {etapa}")  # Imprimir la etapa actual
        speak(etapa)  # Convertir la etapa actual a voz y reproducirla

        audio = recognizer.listen(source)  # Escuchar y grabar el audio del micrófono

        try:
            respuesta_asesor = recognizer.recognize_google(audio, language="es-ES")  # Reconocer el audio usando Google y especificar el idioma español
            print("Asesor: " + respuesta_asesor)  # Imprimir el texto reconocido

            # Tokenizar la respuesta del asesor
            tokens_respuesta = nlp(respuesta_asesor)  # Procesar la respuesta con el modelo de spaCy

            # Calcular palabras clave encontradas en la respuesta del asesor para la etapa actual
            tokens_etapa = nlp(etapa)  # Procesar la etapa actual con el modelo de spaCy
            palabras_clave_etapa = [token.text for token in tokens_etapa if token.text in etapas[i]]  # Obtener las palabras clave de la etapa actual

            palabras_clave_encontradas = [token.text for token in tokens_respuesta if token.text in palabras_clave_etapa]  # Comparar las palabras clave en la respuesta del asesor

            porcentaje_asertividad = (len(palabras_clave_encontradas) / len(palabras_clave_etapa)) * 100  # Calcular el porcentaje de asertividad

            print(f"Porcentaje de asertividad en la etapa {i + 1}: {porcentaje_asertividad}%")  # Imprimir el porcentaje de asertividad

            if porcentaje_asertividad < 75 or "tenerlo" not in respuesta_asesor:  # Verificar si el porcentaje de asertividad es menor al 75% o si falta una palabra clave
                print("El asesor no cumplió con la asertividad o no dijo la palabra clave en esta etapa.")  # Indicar que no se cumplió con la asertividad
                break  # Terminar el bucle

        except sr.UnknownValueError:  # Si no se puede reconocer el audio
            print("No se pudo reconocer el audio.")  # Indicar que no se pudo reconocer el audio
        except sr.RequestError as e:  # Si hay un error en la solicitud al motor de reconocimiento de voz
            print("Error en la solicitud al motor de reconocimiento de voz; {0}".format(e))  # Indicar el error ocurrido

    print("Fin de la conversación.")  # Indicar el fin de la conversación
