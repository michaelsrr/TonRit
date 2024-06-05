import speech_recognition as sr  # Importar la librería de reconocimiento de voz

# Frase esperada
textoanterior = "Buenos días Claro que sí antes de mostrarle las diferentes opciones que tenemos una pregunta el colchón es para usted"  # Definir la frase que se espera escuchar

# Crear un objeto Recognizer
recognizer = sr.Recognizer()  # Crear una instancia del reconocedor de voz

# Utilizar el micrófono como fuente de entrada
with sr.Microphone() as source:  # Utilizar el micrófono como la fuente de audio
    print("Cliente: Buenos días, estoy buscando un colchon")  # Imprimir el texto del cliente para contexto
    print("Amigo vendedor, dí la siguiente frase para atender a tu cliente: Buenos días, claro que si antes de mostrarle las diferentes opciones que tenemos una pregunta ¿El colchón es para usted?")  # Pedir al vendedor que diga la frase esperada
    recognizer.adjust_for_ambient_noise(source)  # Ajustar el reconocedor para el ruido ambiental
    audio = recognizer.listen(source)  # Escuchar y grabar el audio del micrófono

    try:
        # Utilizar el motor de reconocimiento de voz de Google
        text = recognizer.recognize_google(audio, language="es-ES")  # Reconocer el audio usando Google y especificar el idioma español
        print("Texto reconocido: " + text)  # Imprimir el texto reconocido

        if text == textoanterior:  # Comparar el texto reconocido con el texto esperado
            print("Correcto")  # Imprimir "Correcto" si coinciden
        else:
            print("incorrecto")  # Imprimir "Incorrecto" si no coinciden

    except sr.UnknownValueError:  # Si no se puede reconocer el audio
        print("No se pudo reconocer el audio.")  # Indicar que no se pudo reconocer el audio
    except sr.RequestError as e:  # Si hay un error en la solicitud al motor de reconocimiento de voz
        print("Error en la solicitud al motor de reconocimiento de voz; {0}".format(e))  # Indicar el error ocurrido
