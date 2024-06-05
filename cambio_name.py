import os # Importar la librería para interactuar con el sistema operativo

def rename_files(directory, base_name):
    # Recorre todos los archivos en el directorio dado
    for count, filename in enumerate(os.listdir(directory)):
        # Crea el nuevo nombre del archivo
        dst = base_name + str(count) + ".wav"  # Añade un número y la extensión .wav
        src = os.path.join(directory, filename)  # Ruta completa del archivo original
        dst = os.path.join(directory, dst)  # Ruta completa del nuevo archivo

        # Renombra el archivo
        os.rename(src, dst)

# Uso de la función
rename_files(r"C:/Users/Michael/Desktop/Tono - Ritmo/audios/lento_bajo", "lento_bajo_")
