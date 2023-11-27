import speech_recognition as sr

# Frase original
texto_original = "Hola Marina qué gafas tan bonitas"

# Crear un objeto Recognizer
recognizer = sr.Recognizer()

# Utilizar el micrófono como fuente de entrada
with sr.Microphone() as source:
    print("Di la siguiente frase: 'Hola marina que gafas tan bonitas'")
    recognizer.adjust_for_ambient_noise(source)  # Ajustar para el ruido ambiental
    audio = recognizer.listen(source)

    try:
        # Utilizar el motor de reconocimiento de voz de Google
        texto_reconocido = recognizer.recognize_google(audio, language="es-ES")
        print("Texto reconocido: " + texto_reconocido)

        # Dividir la frase en palabras clave o tokens
        palabras_originales = texto_original.lower().split()
        palabras_reconocidas = texto_reconocido.lower().split()

        # Calcular el número de palabras coincidentes
        palabras_coincidentes = set(palabras_originales) & set(palabras_reconocidas)
        porcentaje_asertividad = len(palabras_coincidentes) / len(palabras_originales) * 100

        print("Porcentaje de asertividad: {:.2f}%".format(porcentaje_asertividad))

    except sr.UnknownValueError:
        print("No se pudo reconocer el audio.")
    except sr.RequestError as e:
        print("Error en la solicitud al motor de reconocimiento de voz; {0}".format(e))
