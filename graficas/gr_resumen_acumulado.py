# graficas/gr_resumen_acumulado.py

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def mostrar_grafico_resumen_acumulado(datos):
    st.subheader("📈 Evolución acumulada de la promoción")

    if "tabla_resumen_acumulado" not in datos:
        st.warning("No se ha generado la tabla resumen acumulada aún.")
        return

    df = pd.DataFrame(datos["tabla_resumen_acumulado"])
    if df.empty:
        st.warning("La tabla de resumen acumulado está vacía.")
        return

    df["Mes"] = pd.to_datetime(df["Mes"])
    df = df.sort_values("Mes")

    # Columnas disponibles para graficar
    columnas_a_graficar = [
        "Ingresos acumulados",
        "Flujo total acumulado",
        "Déficit cuenta especial acumulado",
        "Necesidades financiación acumuladas"
    ]

    # Widget de selección múltiple
    seleccionadas = st.multiselect(
        "Selecciona las curvas que deseas visualizar:",
        columnas_a_graficar,
        default=columnas_a_graficar
    )

    # Si no se selecciona ninguna, mostramos aviso
    if not seleccionadas:
        st.info("Selecciona al menos una serie para mostrar el gráfico.")
        return

    fig = go.Figure()

    for col in seleccionadas:
        if col in df.columns:
            # Verificamos si los valores de la columna son correctos, para evitar escalado accidental
            values = df[col]
            if values.max() > 1e6:  # Si el valor máximo es mayor a 1M, lo podemos ajustar
                values = values / 1e6  # Convertimos los valores a millones
                yaxis_title = "Importe acumulado (Millones de €)"
            else:
                yaxis_title = "Importe acumulado (€)"

            fig.add_trace(go.Scatter(
                x=df["Mes"],
                y=values,
                mode="lines+markers",
                name=col
            ))

    fig.update_layout(
        xaxis_title="Mes",
        yaxis_title=yaxis_title,
        hovermode="x unified",
        legend_title="Concepto",
        margin=dict(l=40, r=40, t=40, b=40),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)