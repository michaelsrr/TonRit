import speech_recognition as sr

# Frase original y palabra clave
texto_original = "yo soy muy alto"
palabra_clave = "alto"

# Crear un objeto Recognizer
recognizer = sr.Recognizer()

# Utilizar el micrófono como fuente de entrada
with sr.Microphone() as source:
    print(f"Di la siguiente frase: '{texto_original}'")
    recognizer.adjust_for_ambient_noise(source)  # Ajustar para el ruido ambiental
    audio = recognizer.listen(source)

    try:
        # Utilizar el motor de reconocimiento de voz de Google
        texto_reconocido = recognizer.recognize_google(audio, language="es-ES")
        print("Texto reconocido: " + texto_reconocido)

        # Dividir la frase en palabras clave o tokens
        palabras_originales = texto_original.lower().split()
        palabras_reconocidas = texto_reconocido.lower().split()

        # Verificar si la palabra clave está en las palabras reconocidas
        palabra_clave_encontrada = palabra_clave in palabras_reconocidas

        if palabra_clave_encontrada:
            # Calcular el número de palabras coincidentes
            palabras_coincidentes = set(palabras_originales) & set(palabras_reconocidas)
            porcentaje_asertividad = len(palabras_coincidentes) / len(palabras_originales) * 100
        else:
            porcentaje_asertividad = 0

        print("Porcentaje de asertividad: {:.2f}%".format(porcentaje_asertividad))

        if palabra_clave_encontrada and porcentaje_asertividad > 0:
            print("La frase es aceptable ya que contiene la palabra clave.")
        else:
            print("La frase es inaceptable, la palabra clave no fue reconocida.")

    except sr.UnknownValueError:
        print("No se pudo reconocer el audio.")
    except sr.RequestError as e:
        print("Error en la solicitud al motor de reconocimiento de voz; {0}".format(e))
