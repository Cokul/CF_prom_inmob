import streamlit as st



def cargar_costes_financieros_comerciales(datos):
    with st.expander("🏦 Costes financieros", expanded=False):
        datos["coste_financiero_vivienda"] = st.number_input(
            "💶 Coste financiero por vivienda (€)",
            min_value=0.0,
            value=datos.get("coste_financiero_vivienda", 5000.0),
            step=100.0
        )

    with st.expander("💼 Costes comerciales", expanded=False):
        datos["porcentaje_costes_comerciales"] = st.number_input(
            "📊 Porcentaje de costes comerciales sobre precio sin IVA (%)",
            min_value=0.0,
            max_value=100.0,
            value=datos.get("porcentaje_costes_comerciales", 15.0),
            step=0.5
        )