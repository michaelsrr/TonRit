import spacy
import speech_recognition as sr

# Cargar el modelo de lenguaje en español
nlp = spacy.load("es_core_news_sm")

# Definir las etapas de la conversación
etapas = [
    "es un gusto tenerlo en crea",
    "mi nombre es ",
    "estoy buscando un sofá, colchón mueble",
    "es para cambiar uno que ya tiene",
    "es para usted",
    "con mucho gusto siga y permítame mostrarle los últimos diseño",
    "tenemos muebles cómodos y confortables"
]

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

# Inicializar el sintetizador de voz 
from gtts import gTTS
import os

def speak(text):
    tts = gTTS(text, lang="es")
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

# Configurar el micrófono como fuente de entrada
with sr.Microphone() as source:
    print("¡Hable con el asesor!")

    for i, etapa in enumerate(etapas):
        # Esperar a que el asesor hable y transcribir su respuesta
        print(f"Asesor: {etapa}")
        speak(etapa)

        audio = recognizer.listen(source)

        try:
            respuesta_asesor = recognizer.recognize_google(audio, language="es-ES")
            print("Asesor: " + respuesta_asesor)

            # Tokenizar la respuesta del asesor
            tokens_respuesta = nlp(respuesta_asesor)

            # Calcular palabras clave encontradas en la respuesta del asesor para la etapa actual
            tokens_etapa = nlp(etapa)
            palabras_clave_etapa = [token.text for token in tokens_etapa if token.text in etapas[i]]

            palabras_clave_encontradas = [token.text for token in tokens_respuesta if token.text in palabras_clave_etapa]

            porcentaje_asertividad = (len(palabras_clave_encontradas) / len(palabras_clave_etapa)) * 100

            print(f"Porcentaje de asertividad en la etapa {i + 1}: {porcentaje_asertividad}%")

            if porcentaje_asertividad < 75 or "tenerlo" not in respuesta_asesor:
                print("El asesor no cumplió con la asertividad o no dijo la palabra clave en esta etapa.")
                break

        except sr.UnknownValueError:
            print("No se pudo reconocer el audio.")
        except sr.RequestError as e:
            print("Error en la solicitud al motor de reconocimiento de voz; {0}".format(e))

    print("Fin de la conversación.")
