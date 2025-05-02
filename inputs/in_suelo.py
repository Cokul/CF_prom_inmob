import streamlit as st
from datetime import date
import pandas as pd

def cargar_inputs_suelo(datos):
    with st.expander("🌍 Coste del suelo", expanded=False):
        # Claves dinámicas basadas en el nombre del campo
        key_superficie_solar = "superficie_solar_" + str(id(datos))  # ID único para cada ejecución
        key_coste_suelo = "coste_suelo_" + str(id(datos))  # ID único para cada ejecución
        key_fecha_adquisicion = "fecha_adquisicion_suelo_" + str(id(datos))  # ID único para cada ejecución
        
        datos["superficie_solar"] = st.number_input(
            "Superficie del solar (m²)",
            min_value=0.0,
            value=datos.get("superficie_solar", 1000.0),
            step=10.0,
            key=key_superficie_solar
        )

        datos["coste_suelo"] = st.number_input(
            "Coste de adquisición del solar (€)",
            min_value=0.0,
            value=datos.get("coste_suelo", 500000.0),
            step=10000.0,
            key=key_coste_suelo
        )

        datos["fecha_adquisicion_suelo"] = st.date_input(
            "📅 Fecha de adquisición",
            value=datos.get("fecha_adquisicion_suelo", date.today()),
            key=key_fecha_adquisicion
        )

        # Calcular y guardar el coste de suelo por m² y por vivienda
        datos["coste_suelo_m2"] = round(datos["coste_suelo"] / datos["superficie_solar"], 2) if datos["superficie_solar"] > 0 else 0
        datos["coste_suelo_vivienda"] = round(datos["coste_suelo"] / datos.get("n_viviendas_ingresos", 1), 2) if datos.get("n_viviendas_ingresos", 1) > 0 else 0

        # Calcular coste del suelo con IVA (usamos el IVA de "iva_otros")
        iva_otros = datos.get("iva_otros", 21.0)  # IVA Otros, valor por defecto si no está configurado
        coste_suelo_con_iva = datos["coste_suelo"] * (1 + iva_otros / 100)

        # Mostrar coste suelo por m² y por vivienda
        st.markdown(f"💡 **Coste suelo por m²**: {datos['coste_suelo_m2']:.2f} €/m²")
        st.markdown(f"🏠 **Coste suelo por vivienda**: {datos['coste_suelo_vivienda']:.2f} €")
        
        # Generamos la tabla de coste de suelo (sin IVA y con IVA)
        fecha_adquisicion = pd.to_datetime(datos["fecha_adquisicion_suelo"]).strftime("%Y-%m")  # Convertir a formato mes-año
        df_suelo = pd.DataFrame({
            fecha_adquisicion: [datos["coste_suelo"], coste_suelo_con_iva]
        }, index=["Coste suelo sin IVA", "Coste suelo con IVA"]).T

        # Mostrar la tabla en el expander
        st.dataframe(df_suelo)

        # Asegurarnos de que los datos están bien guardados
        datos["coste_suelo_con_iva"] = coste_suelo_con_iva  # Guardamos la variable en el diccionario

        st.success("Coste del suelo con IVA añadido correctamente.")