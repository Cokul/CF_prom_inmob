# bienvenida.py

import streamlit as st
import base64

def mostrar_pantalla_bienvenida():
    if "ruta_version_actual" in st.session_state:
        return  # Ya hay proyecto cargado, no mostrar bienvenida

    

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("assets/logo/website-logo.svg", width=100)
    with col2:
        st.markdown("""
            ## Bienvenido al **Generador de Presupuestos de Promociones**
            Herramienta de análisis económico para promociones inmobiliarias.

            Esta aplicación ha sido desarrollada para simplificar la creación de flujos de caja,
            planificaciones de obra, y necesidades de financiación, con un enfoque claro, modular
            y adaptado a la operativa habitual del sector promotor.
        """)

    st.divider()

    st.markdown("""
    ### ¿Cómo empezar?
    1. Ve al panel lateral izquierdo.
    2. Crea un nuevo proyecto o selecciona uno existente.
    3. Empieza a cargar los inputs del proyecto y genera los outputs.
    4. Cuando termines, guarda la versión o crea una nueva.

    ---
    """)

    st.info("Selecciona un proyecto desde el menú lateral para comenzar.")
    st.stop()