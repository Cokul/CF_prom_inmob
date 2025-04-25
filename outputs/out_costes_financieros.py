import pandas as pd
import streamlit as st
from utils.formatos import formatear_miles

def generar_tabla_costes_financieros(datos):
    st.markdown("## 🏦 Costes Financieros")

    coste_por_vivienda = datos.get("coste_financiero_vivienda", 0.0)
    unidades_raw = datos.get("tabla_unidades_vendidas", [])

    if not unidades_raw or coste_por_vivienda == 0:
        st.warning("Faltan datos de ventas por mes o el coste por vivienda es cero.")
        return

    df = pd.DataFrame(unidades_raw)
    if "Mes" not in df.columns or "Unidades" not in df.columns:
        st.error("La tabla de unidades no tiene el formato esperado.")
        return

    df = df[df["Mes"] != "Total"]  # Eliminar fila de totales si existe
    df["Mes"] = pd.to_datetime(df["Mes"], errors="coerce")
    df = df.sort_values("Mes")

    df["Coste financiero"] = -(df["Unidades"] * coste_por_vivienda)

    fila_total = pd.DataFrame({
        "Mes": ["Total"],
        "Unidades": [df["Unidades"].sum()],
        "Coste financiero": [df["Coste financiero"].sum()]
    })

    df_final = pd.concat([df, fila_total], ignore_index=True)
    df_final["Mes"] = df_final["Mes"].apply(lambda x: x.strftime("%Y-%m") if isinstance(x, pd.Timestamp) else x)

    # Copia para visualización con formato
    df_mostrar = df_final.copy()
    df_mostrar["Coste financiero"] = df_mostrar["Coste financiero"].apply(formatear_miles)

    st.dataframe(df_mostrar, use_container_width=True)

    # Guardar versión con datos numéricos para cálculos
    datos["costes_financieros"] = df_final.to_dict(orient="records")