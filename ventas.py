import spacy
import speech_recognition as sr
from gtts import gTTS
import os
import time

# Cargar el modelo de lenguaje en español
nlp = spacy.load("es_core_news_sm")

# Definir las etapas y las frases clave de la conversación
conversacion = [
    {
        "etapa": 1,
        "frases": [
            {"texto": "es un gusto tenerlo en crea", "palabras_claves": ["gusto", "crea"]},
            {"texto": "mi nombre es", "palabras_claves": ["nombre"]},
            {"texto": "estoy buscando un sofá, colchón mueble", "palabras_claves": ["sofá", "colchón", "mueble"]},
            {"texto": "es para cambiar uno que ya tiene", "palabras_claves": ["cambiar"]},
            {"texto": "es para usted", "palabras_claves": ["es para usted"]},
            {"texto": "con mucho gusto, siga y permítame mostrarle los últimos diseños", "palabras_claves": ["mostrarle"]},
            {"texto": "tenemos muebles cómodos y confortables", "palabras_claves": ["cómodos", "confortables"]}
        ]
    },
    {
        "etapa": 2,
        "frases": [
            {"texto": "le voy a efectuar unas preguntas para determinar con exactitud el tipo de producto que está buscando y poderle asesorar mejor", "palabras_claves": ["preguntas", "para", "determinar", "exactitud", "asesorar"]},
            {"texto": "exactamente qué tipo de producto está buscando", "palabras_claves": ["exactamente"]},
            {"texto": "con qué tipo de producto en diseño se identifica normalmente", "palabras_claves": ["identifica"]},
            {"texto": "que es lo mas importante para usted al momento de comprar un", "palabras_claves": ["lo", "mas", "importante", "comprar"]},
            {"texto": "que es lo mas valioso para usted al momento de comprar un", "palabras_claves": ["valioso", "comprar"]},
            {"texto": "que colores predominan en el lugar donde va a poner el", "palabras_claves": ["predominan"]},
            {"texto": "como se lo imagina", "palabras_claves": ["como", "se", "lo", "imagina"]},
            {"texto": "como es el que tiene actualmente", "palabras_claves": ["como"]},
            {"texto": "cual es el motivo del cambio", "palabras_claves": ["motivo"]},
            {"texto": "como es el que tiene actualmente", "palabras_claves": ["como"]},
            {"texto": "busca algo totalmente diferente", "palabras_claves": ["diferente"]},
            {"texto": "busca algo similar al que tiene en la actualidad", "palabras_claves": ["similar"]},
            {"texto": "cual de estas opciones le llama mas la atencion", "palabras_claves": ["le", "llama", "mas", "la", "atencion"]},
            {"texto": "cual de estas alternativas lo conecta mas", "palabras_claves": ["lo", "conecta", "mas"]},
            {"texto": "cual de estas posibilidades veria en el espacio", "palabras_claves": ["veria"]},
            {"texto": "cual de estas opciones es mas comodo", "palabras_claves": ["comodo"]},
            {"texto": "que es moderno para usted", "palabras_claves": ["que", "es"]},
            {"texto": "que es clasico para usted", "palabras_claves": ["que", "es"]},
            {"texto": "de este producto que es lo que más le gusta", "palabras_claves": ["producto"]}
        ]
    }
    # Puedes agregar más etapas según sea necesario
]

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

def speak(text):
    tts = gTTS(text, lang="es")
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

# Configurar el micrófono como fuente de entrada
with sr.Microphone() as source:
    time.sleep(2)  # Agrega un retraso de 2 segundos antes de mostrar el mensaje
    print("¡Hable con el asesor!")

    for etapa_info in conversacion:
        etapa = etapa_info["etapa"]
        print(f"\nEtapa {etapa}:")

        for i, frase_info in enumerate(etapa_info["frases"]):
            frase = frase_info["texto"]
            palabras_claves = frase_info["palabras_claves"]

            print(f"\nFrase {i + 1}: {frase}")
            print(f"Palabras claves: {', '.join(palabras_claves)}")

            input("Presione Enter para continuar...")  # Espera a que el usuario presione Enter antes de continuar
            speak(frase)
            
            while True:
                audio = recognizer.listen(source)

                try:
                    respuesta_asesor = recognizer.recognize_google(audio, language="es-ES")
                    print("Asesor: " + respuesta_asesor)

                    tokens_respuesta = nlp(respuesta_asesor)
                    tokens_frase = nlp(frase)
                    palabras_clave_encontradas = [token.text for token in tokens_respuesta if token.text in palabras_claves]

                    porcentaje_asertividad = (len(palabras_clave_encontradas) / len(palabras_claves)) * 100

                    print(f"Porcentaje de asertividad en la etapa {etapa}, frase {i + 1}: {porcentaje_asertividad}%")

                    if porcentaje_asertividad >= 75 and all(palabra_clave in respuesta_asesor for palabra_clave in palabras_claves):
                        break
                    else:
                        print("El asesor no cumplió con la asertividad o no dijo la palabra clave en esta etapa. Repitiendo la frase.")

                except sr.UnknownValueError:
                    print("No se pudo reconocer el audio.")
                except sr.RequestError as e:
                    print(f"Error en la solicitud al motor de reconocimiento de voz; {e}")

print("Fin de la conversación.")

