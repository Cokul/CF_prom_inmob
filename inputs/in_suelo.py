import streamlit as st
from datetime import date


def cargar_inputs_suelo(datos):
    with st.expander("🌍 Coste del suelo", expanded=False):
        datos["superficie_solar"] = st.number_input(
            "Superficie del solar (m²)",
            min_value=0.0,
            value=datos.get("superficie_solar", 1000.0),
            step=10.0
        )

        datos["coste_suelo"] = st.number_input(
            "Coste de adquisición del solar (€)",
            min_value=0.0,
            value=datos.get("coste_suelo", 500000.0),
            step=10000.0
        )

        datos["fecha_adquisicion_suelo"] = st.date_input(
            "📅 Fecha de adquisición",
            value=datos.get("fecha_adquisicion_suelo", date.today())
        )

        # Calcular y guardar el coste de suelo por m² y por vivienda
        datos["coste_suelo_m2"] = round(datos["coste_suelo"] / datos["superficie_solar"], 2) if datos["superficie_solar"] > 0 else 0
        datos["coste_suelo_vivienda"] = round(datos["coste_suelo"] / datos.get("n_viviendas_ingresos", 1), 2) if datos.get("n_viviendas_ingresos", 1) > 0 else 0

        st.markdown(f"💡 **Coste suelo por m²**: {datos['coste_suelo_m2']:.2f} €/m²")
        st.markdown(f"🏠 **Coste suelo por vivienda**: {datos['coste_suelo_vivienda']:.2f} €")
