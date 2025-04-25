import os
import json
import streamlit as st
import shutil
from datetime import date, datetime 
import pandas as pd

# Importar la función de estilos
from utils.styles import aplicar_estilos

# Activar modo ancho
st.set_page_config(layout="wide")

# Aplicar los estilos personalizados
aplicar_estilos()

# Inicializar datos
if "datos_proyecto" not in st.session_state:
    st.session_state["datos_proyecto"] = {}
datos = st.session_state["datos_proyecto"]

# Bienvenida
from bienvenida import mostrar_pantalla_bienvenida

# Importar la función de la sidebar
from utils.sidebar import gestionar_proyecto_y_version

# Llamar a la función para gestionar proyectos y versiones
gestionar_proyecto_y_version()

# Módulos de inputs
from inputs.in_generales import cargar_inputs_generales
from inputs.in_ingresos import cargar_inputs_ingresos
from inputs.in_suelo import cargar_inputs_suelo
from inputs.in_ejecucion import cargar_inputs_ejecucion
from inputs.in_costes_indirectos import cargar_costes_indirectos
from inputs.in_costes_financieros_comerciales import cargar_costes_financieros_comerciales

# Módulos de outputs
from outputs.out_ingresos import generar_tablas_ingresos
from outputs.out_costes_ejecucion import generar_tablas_costes_ejecucion
from outputs.out_costes_indirectos import generar_tablas_costes_indirectos
from outputs.out_costes_financieros import generar_tabla_costes_financieros

# Módulos flujo de caja
from flujo_caja.flujo_caja import generar_tabla_flujo_caja

# Módulos de gráficas
from graficas.gr_ingresos import mostrar_graficas_ingresos
from graficas.gr_costes_ejecucion import mostrar_graficas_costes_ejecucion
from graficas.gr_resumen_acumulado import mostrar_grafico_resumen_acumulado



# Mostrar pantalla de bienvenida si no hay proyecto cargado
mostrar_pantalla_bienvenida()

# Mostrar versión actual cargada
ruta_actual = st.session_state.get("ruta_version_actual")
if ruta_actual and os.path.exists(ruta_actual):
    nombre_actual = os.path.splitext(os.path.basename(ruta_actual))[0]
    fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta_actual)).strftime("%Y-%m-%d %H:%M")
    st.info(f"📂 Versión cargada: `{nombre_actual}`  \n🕒 Última modificación: `{fecha_mod}`")
    

# 🧮 Pestañas principales
tabs = st.tabs(["📥 Inputs", "📊 Outputs", "📈 Flujo de Caja", "📋 Resumen", "📉 Gráficas"])

# 📥 Pestaña Inputs
with tabs[0]:
    st.header("📥 Inputs del Proyecto")
    cargar_inputs_generales(datos)
    cargar_inputs_ingresos(datos)
    cargar_inputs_suelo(datos)
    cargar_inputs_ejecucion(datos)   
    cargar_costes_indirectos(datos)  
    cargar_costes_financieros_comerciales(datos) 

# 📊 Pestaña Outputs
with tabs[1]:
    st.header("📊 Outputs auxiliares")
    st.info("Aquí se mostrarán los resultados intermedios por bloques: ingresos, costes, cronogramas, etc.")

    # Ingresos:
    with st.expander("📦 Ingresos", expanded=False):
        from outputs.out_ingresos import generar_tablas_ingresos
        generar_tablas_ingresos(datos)

    # Costes ejecución:
    with st.expander("🏗️ Costes de ejecución"):
        generar_tablas_costes_ejecucion(datos)

    # Costes indirectos
    with st.expander("💼 Costes indirectos"):
        generar_tablas_costes_indirectos(datos)

    # Costes financieros
    with st.expander("🏦 Costes financieros"):
        generar_tabla_costes_financieros(datos)


# 📈 Pestaña Flujo de Caja
with tabs[2]:
    st.header("📈 Flujo de Caja General")
    st.info("Aquí se integrará el flujo de caja consolidado mensual con todos los inputs procesados.")

    from flujo_caja.flujo_caja import generar_tabla_flujo_caja
    generar_tabla_flujo_caja(datos)

# 📋 Pestaña Resumen
with tabs[3]:
    st.header("📋 Resumen del Proyecto")
    from resumen.resumen_general import mostrar_resumen_general
    mostrar_resumen_general(datos)

# 📊 Pestaña Gráficas
with tabs[4]:
    st.header("📊 Gráficas del Proyecto")
    
    # Gráficas ingresos
    with st.expander("📈 Gráficas de ingresos", expanded=False):
        mostrar_graficas_ingresos(datos)

    # Gráficas costes ejecución
    with st.expander("🏗️ Gráficas de costes de ejecución", expanded=False):
        mostrar_graficas_costes_ejecucion(datos)

    # Gráfica tabla resumen acumulado
    with st.expander("📊 Gráfica de resumen acumulado", expanded=False):
        mostrar_grafico_resumen_acumulado(datos)

with st.expander("🛠️ Debug: contenido completo de datos", expanded=False):
    import json
    from datetime import date, datetime

    def serializar_objetos(o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        return str(o)

    st.code(json.dumps(datos, indent=2, ensure_ascii=False, default=serializar_objetos), language="json")
    
