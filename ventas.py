import spacy  # Importar la librería de procesamiento de lenguaje natural
import speech_recognition as sr  # Importar la librería de reconocimiento de voz
from gtts import gTTS  # Importar la librería para convertir texto a voz
import os  # Importar la librería para interactuar con el sistema operativo
import time  # Importar la librería para manejar tiempos

# Cargar el modelo de lenguaje en español
nlp = spacy.load("es_core_news_sm")  # Cargar el modelo de Spacy para español

# Definir las etapas y las frases clave de la conversación
conversacion = [  # Lista que contiene las etapas de la conversación y las frases clave asociadas a cada etapa
    {
        "etapa": 1,  # Etapa 1
        "frases": [  # Lista de frases de la etapa 1
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
        "etapa": 2,  # Etapa 2
        "frases": [  # Lista de frases de la etapa 2
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
recognizer = sr.Recognizer()  # Crear una instancia del reconocedor de voz

def speak(text):
    tts = gTTS(text, lang="es")  # Convertir el texto a voz en español
    tts.save("response.mp3")  # Guardar la voz generada en un archivo mp3
    os.system("mpg321 response.mp3")  # Reproducir el archivo de audio mp3

# Configurar el micrófono como fuente de entrada
with sr.Microphone() as source:  # Utilizar el micrófono como la fuente de audio
    time.sleep(2)  # Agrega un retraso de 2 segundos antes de mostrar el mensaje
    print("¡Hable con el asesor!")  # Mensaje para iniciar la conversación

    for etapa_info in conversacion:  # Iterar a través de cada etapa de la conversación
        etapa = etapa_info["etapa"]  # Obtener el número de la etapa
        print(f"\nEtapa {etapa}:")  # Imprimir el número de la etapa

        for i, frase_info in enumerate(etapa_info["frases"]):  # Iterar a través de cada frase de la etapa
            frase = frase_info["texto"]  # Obtener el texto de la frase
            palabras_claves = frase_info["palabras_claves"]  # Obtener las palabras clave de la frase

            print(f"\nFrase {i + 1}: {frase}")  # Imprimir el número y el texto de la frase
            print(f"Palabras claves: {', '.join(palabras_claves)}")  # Imprimir las palabras clave

            input("Presione Enter para continuar...")  # Espera a que el usuario presione Enter antes de continuar
            speak(frase)  # Reproducir la frase usando texto a voz
            
            while True:
                audio = recognizer.listen(source)  # Escuchar y grabar el audio del micrófono

                try:
                    respuesta_asesor = recognizer.recognize_google(audio, language="es-ES")  # Reconocer el audio usando Google y especificar el idioma español
                    print("Asesor: " + respuesta_asesor)  # Imprimir el texto reconocido

                    tokens_respuesta = nlp(respuesta_asesor)  # Procesar el texto reconocido con Spacy
                    tokens_frase = nlp(frase)  # Procesar el texto de la frase con Spacy
                    palabras_clave_encontradas = [token.text for token in tokens_respuesta if token.text in palabras_claves]  # Encontrar las palabras clave en la respuesta

                    porcentaje_asertividad = (len(palabras_clave_encontradas) / len(palabras_claves)) * 100  # Calcular el porcentaje de palabras clave encontradas

                    print(f"Porcentaje de asertividad en la etapa {etapa}, frase {i + 1}: {porcentaje_asertividad}%")  # Imprimir el porcentaje de asertividad

                    if porcentaje_asertividad >= 75 and all(palabra_clave in respuesta_asesor for palabra_clave in palabras_claves):  # Si el porcentaje de asertividad es mayor o igual al 75% y todas las palabras clave están en la respuesta
                        break  # Salir del bucle y pasar a la siguiente frase
                    else:
                        print("El asesor no cumplió con la asertividad o no dijo la palabra clave en esta etapa. Repitiendo la frase.")  # Indicar que no se cumplió con la asertividad y repetir la frase

                except sr.UnknownValueError:  # Si no se puede reconocer el audio
                    print("No se pudo reconocer el audio.")  # Indicar que no se pudo reconocer el audio
                except sr.RequestError as e:  # Si hay un error en la solicitud al motor de reconocimiento de voz
                    print(f"Error en la solicitud al motor de reconocimiento de voz; {e}")  # Indicar el error ocurrido

print("Fin de la conversación.")  # Mensaje al finalizar la conversación