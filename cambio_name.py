import os

def rename_files(directory, base_name):
    for count, filename in enumerate(os.listdir(directory)):
        dst = base_name + "_" + str(count) + ".wav"  # Añade un guion bajo y cambia a .wav
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, dst)

        os.rename(src, dst)  # Renombra el archivo

# Uso:
rename_files(r"C:/Users/Michael/Desktop/Tono - Ritmo/audios/lento_bajo", "lento_bajo_")

