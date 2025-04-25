import streamlit as st
from datetime import date


def cargar_costes_indirectos(datos):
    with st.expander("📦 Costes indirectos", expanded=False):

        st.markdown("### 🧾 Honorarios técnicos")
        datos["honorarios_tecnicos"] = st.number_input(
            "Honorarios técnicos (% sobre PEM)",
            min_value=0.0,
            max_value=100.0,
            value=datos.get("honorarios_tecnicos", 5.0),
            step=0.1,
            format="%.1f"
        )

        st.markdown("### 🏢 Gastos de administración")
        datos["gastos_administracion"] = st.number_input(
            "Gastos de administración (% sobre PEM)",
            min_value=0.0,
            max_value=100.0,
            value=datos.get("gastos_administracion", 4.0),
            step=0.1,
            format="%.1f"
        )

        st.markdown("### 🧮 Otros costes indirectos")
        datos["otros_costes_indirectos"] = st.number_input(
            "Otros costes indirectos (% sobre PEM)",
            min_value=0.0,
            max_value=100.0,
            value=datos.get("otros_costes_indirectos", 0.0),
            step=0.1,
            format="%.1f"
        )

        # Cálculo del total sobre el PEM (coste total de ejecución)
        pem = datos.get("coste_total_ejecucion", 0)
        total_indirectos = round(pem * (
            datos["honorarios_tecnicos"] +
            datos["gastos_administracion"] +
            datos["otros_costes_indirectos"]
        ) / 100, 2)

        datos["costes_indirectos_totales"] = total_indirectos

        n_viviendas = datos.get("n_viviendas_ingresos", 0)
        datos["costes_indirectos_vivienda"] = round(total_indirectos / n_viviendas, 2) if n_viviendas > 0 else 0

        st.markdown(f"**Total costes indirectos**: {total_indirectos:,.2f} €")
        st.markdown(f"**Costes indirectos por vivienda**: {datos['costes_indirectos_vivienda']:,.2f} €")

        st.markdown("### 📌 Información adicional")
        datos["descripcion_costes_indirectos"] = st.text_area(
            "Descripción o notas sobre costes indirectos",
            value=datos.get("descripcion_costes_indirectos", "")
        )