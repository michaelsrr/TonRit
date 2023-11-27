import speech_recognition as sr
textoanterior = "Buenos días Claro que sí antes de mostrarle las diferentes opciones que tenemos una pregunta el colchón es para usted"

# Crear un objeto Recognizer
recognizer = sr.Recognizer()

# Utilizar el micrófono como fuente de entrada
with sr.Microphone() as source:
    print("Cliente: Buenos días, estoy buscando un colchon")
    print("Amigo vendedor, dí la siguiente frase para atender a tu cliente: Buenos días, claro que si antes de mostrarle las diferentes opciones que tenemos una pregunta ¿El colchón es para usted?")
    recognizer.adjust_for_ambient_noise(source)  # Ajustar para el ruido ambiental
    audio = recognizer.listen(source)

    try:
        # Utilizar el motor de reconocimiento de voz de Google
        text = recognizer.recognize_google(audio, language="es-ES")
        print("Texto reconocido: " + text)
        if (text == textoanterior):
           print("Correcto")
        else:
            print("incorrecto")
        
        #print(textoanterior)

    except sr.UnknownValueError:
        print("No se pudo reconocer el audio.")
    except sr.RequestError as e:
        print("Error en la solicitud al motor de reconocimiento de voz; {0}".format(e))

