#utils/proyectos.py

import os
import json
from datetime import datetime

def listar_proyectos_guardados_con_fecha():
    """
    Devuelve una lista de tuplas: (clave_visible, ruta_json, fecha_modificación)
    clave_visible = 'promoción - versión'
    """
    proyectos = []
    base_path = "proyectos"  # carpeta raíz

    for promocion in os.listdir(base_path):
        ruta_promocion = os.path.join(base_path, promocion)
        if os.path.isdir(ruta_promocion):
            for archivo in os.listdir(ruta_promocion):
                if archivo.endswith(".json"):
                    version = archivo.replace(".json", "")
                    clave = f"{promocion} - {version}"
                    ruta_json = os.path.join(ruta_promocion, archivo)
                    fecha = datetime.fromtimestamp(os.path.getmtime(ruta_json)).strftime("%Y-%m-%d %H:%M")
                    proyectos.append((clave, ruta_json, fecha))
    return proyectos


def cargar_proyecto_guardado(nombre_completo):
    """
    Carga un proyecto dado su identificador en formato 'promocion - version'.
    """
    try:
        promocion, version = nombre_completo.split(" - ")
    except ValueError:
        return None

    ruta_archivo = os.path.join(RUTA_PROYECTOS, promocion, f"{version}.json")
    if not os.path.isfile(ruta_archivo):
        return None

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        datos = json.load(f)

    return datos