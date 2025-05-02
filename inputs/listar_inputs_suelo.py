# listar_inputs_suelo.py

import sys
import streamlit as st

# Especifica la ruta del archivo in_suelo.py
sys.path.insert(0, '/ruta/a/tu/proyecto/inputs')  # Actualiza la ruta al directorio donde está in_suelo.py

# Ahora importa el archivo in_suelo.py
import in_suelo

# Muestra las variables que hemos definido en in_suelo.py
print("Variables en in_suelo.py:")

# Aquí se accede a las variables directamente definidas en in_suelo.py
print(f"superficie_solar: {in_suelo.datos.get('superficie_solar')}")
print(f"coste_suelo: {in_suelo.datos.get('coste_suelo')}")
print(f"fecha_adquisicion_suelo: {in_suelo.datos.get('fecha_adquisicion_suelo')}")
print(f"coste_suelo_m2: {in_suelo.datos.get('coste_suelo_m2')}")
print(f"coste_suelo_vivienda: {in_suelo.datos.get('coste_suelo_vivienda')}")