import speech_recognition as sr  # Importar la librería de reconocimiento de voz

# Frase original y palabra clave
texto_original = "yo soy muy alto"  # Definir la frase original
palabra_clave = "alto"  # Definir la palabra clave que se espera reconocer

# Crear un objeto Recognizer
recognizer = sr.Recognizer()  # Crear una instancia del reconocedor de voz

# Utilizar el micrófono como fuente de entrada
with sr.Microphone() as source:  # Utilizar el micrófono como la fuente de audio
    print(f"Di la siguiente frase: '{texto_original}'")  # Indicar al usuario que debe decir la frase original
    recognizer.adjust_for_ambient_noise(source)  # Ajustar el reconocedor para el ruido ambiental
    audio = recognizer.listen(source)  # Escuchar y grabar el audio del micrófono

    try:
        # Utilizar el motor de reconocimiento de voz de Google
        texto_reconocido = recognizer.recognize_google(audio, language="es-ES")  # Reconocer el audio usando Google y especificar el idioma español
        print("Texto reconocido: " + texto_reconocido)  # Imprimir el texto reconocido

        # Dividir la frase en palabras clave o tokens
        palabras_originales = texto_original.lower().split()  # Convertir la frase original a minúsculas y dividirla en palabras
        palabras_reconocidas = texto_reconocido.lower().split()  # Convertir el texto reconocido a minúsculas y dividirlo en palabras

        # Verificar si la palabra clave está en las palabras reconocidas
        palabra_clave_encontrada = palabra_clave in palabras_reconocidas  # Comprobar si la palabra clave está en las palabras reconocidas

        if palabra_clave_encontrada:  # Si se encuentra la palabra clave
            # Calcular el número de palabras coincidentes
            palabras_coincidentes = set(palabras_originales) & set(palabras_reconocidas)  # Calcular las palabras coincidentes entre el texto original y el reconocido
            porcentaje_asertividad = len(palabras_coincidentes) / len(palabras_originales) * 100  # Calcular el porcentaje de palabras coincidentes
        else:
            porcentaje_asertividad = 0  # Si no se encuentra la palabra clave, el porcentaje de asertividad es 0

        print("Porcentaje de asertividad: {:.2f}%".format(porcentaje_asertividad))  # Imprimir el porcentaje de asertividad

        if palabra_clave_encontrada and porcentaje_asertividad > 0:  # Si se encuentra la palabra clave y el porcentaje de asertividad es mayor a 0
            print("La frase es aceptable ya que contiene la palabra clave.")  # Indicar que la frase es aceptable
        else:
            print("La frase es inaceptable, la palabra clave no fue reconocida.")  # Indicar que la frase es inaceptable

    except sr.UnknownValueError:  # Si no se puede reconocer el audio
        print("No se pudo reconocer el audio.")  # Indicar que no se pudo reconocer el audio
    except sr.RequestError as e:  # Si hay un error en la solicitud al motor de reconocimiento de voz
        print("Error en la solicitud al motor de reconocimiento de voz; {0}".format(e))  # Indicar el error ocurrido
