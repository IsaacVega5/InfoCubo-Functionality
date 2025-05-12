import os
import subprocess
import platform
import re
import unicodedata
from tkinter.filedialog import askdirectory, asksaveasfilename

def open_file(path):
    try:
        if platform.system() == "Windows":
            # Windows - abrir explorador y seleccionar archivo
            path = path.replace("/", "\\")
            subprocess.Popen(f'explorer /select,"{path}"')
        elif platform.system() == "Darwin":
            # MacOS - abrir Finder
            subprocess.Popen(["open", "-R", path])
        else:
            # Linux - abrir gestor de archivos (puede variar según distribución)
            subprocess.Popen(["xdg-open", os.path.dirname(path)])
    except Exception as e:
        print(f"No se pudo abrir el archivo: {e}")


def get_metadata(path):
    file = open(path, "r")
    lines = file.readlines()

    metadata = {}
    past_key = ""
    for line in lines:
        line = line.strip()
        if line == "ENVI":
            continue
        if "=" in line:
            list_line = line.split("=")
            key = list_line[0].strip()
            value = "=".join(list_line[1:])
            metadata[key.strip()] = value.strip()
            past_key = key.strip()
        else:
            metadata[past_key] += line

    if metadata.get("description") is not None:
        metadata["description"] = (
            metadata["description"].replace("{", "").replace("}", "")
        )
    file.close()
    return metadata


def get_firmware(metadata):
    for key in metadata.keys():
        if "firmware" in str(key).lower():
            return metadata[key]
    return None


def formate_filename(nombre):
    # Normalizar caracteres unicode (convertir acentos a caracteres base)
    nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('ascii')
    
    # Reemplazar espacios y caracteres no permitidos por guiones bajos
    nombre = nombre.replace(',', '-')
    nombre = re.sub(r'[^\w\-_. ]', '', nombre)
    nombre = nombre.replace(' ', '_')
    nombre = nombre.replace("*", "x")
    
    # Limitar la longitud del nombre (opcional)
    nombre = nombre[:255]  # Límite común en muchos sistemas de archivos
    
    return nombre

def save_to_folder(title = "Select directory", initialdir = "/"):
    file = initialdir.split("/")[-1]
    folder = initialdir.replace(file, "")
    
    if not os.path.exists(initialdir):
        path = asksaveasfilename(
            initialdir=folder,
            initialfile=file,
            title=title,
            filetypes=[("Folder", ".")],
        )
    else:
        path = askdirectory(
            initialdir=initialdir,
            title=title,
        )
    
    if not path:
        return None
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def find_value_on_dict(d, to_find):
    for key, value in d.items():
        if value is to_find:
            return True
        elif isinstance(value, dict):
            if find_value_on_dict(value, to_find):
                return True
    return False