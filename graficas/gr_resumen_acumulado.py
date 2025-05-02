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

    columnas_a_graficar = [
        "Ingresos acumulados",
        "Flujo total acumulado",
        "Déficit cuenta especial acumulado",
        "Necesidades financiación acumuladas"
    ]

    seleccionadas = st.multiselect(
        "Selecciona las curvas que deseas visualizar:",
        columnas_a_graficar,
        default=columnas_a_graficar
    )

    if not seleccionadas:
        st.info("Selecciona al menos una serie para mostrar el gráfico.")
        return

    fig = go.Figure()

    for col in seleccionadas:
        if col in df.columns:
            valores = df[col]
            valores_millones = valores / 1e6  # Mostrar en millones

            fig.add_trace(go.Scatter(
                x=df["Mes"],
                y=valores_millones,
                mode="lines+markers",
                name=col
            ))

    # Línea horizontal en el umbral de rentabilidad (igualar necesidades acumuladas)
    # Obtener última fila válida (no Total)
    ult_fila = df[df["Mes"] != "Total"].iloc[-1]
    umbral_valor = abs(ult_fila.get("Necesidades financiación acumuladas", 0)) / 1e6  # en millones

    fig.add_trace(go.Scatter(
        x=[df["Mes"].min(), df["Mes"].max()],
        y=[umbral_valor, umbral_valor],
        mode="lines",
        name="Umbral de rentabilidad",
        line=dict(color="gray", dash="dash")
    ))

    # 1. Detectar mes en que los ingresos acumulados superan el umbral
    df["Ingresos acumulados (M€)"] = df["Ingresos acumulados"] / 1e6
    df_umbral = df[df["Ingresos acumulados (M€)"] >= umbral_valor]

    if not df_umbral.empty:
        fila_umbral = df_umbral.iloc[0]
        fig.add_trace(go.Scatter(
            x=[fila_umbral["Mes"]],
            y=[fila_umbral["Ingresos acumulados (M€)"]],
            mode="markers+text",
            name="Punto de rentabilidad",
            marker=dict(size=12, color="green", symbol="diamond"),
            text=[f"{fila_umbral['Mes'].strftime('%b %Y')}"],
            textposition="top center",
            showlegend=True
        ))

    fig.update_layout(
        xaxis_title="Mes",
        yaxis_title="Importe acumulado (Millones de €)",
        hovermode="x unified",
        legend_title="Concepto",
        margin=dict(l=40, r=40, t=40, b=40),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Panel resumen con los valores finales
    st.markdown("### 🧾 Panel resumen (valores finales)")
    ult_fila = df[df["Mes"] != "Total"].iloc[-1]
    panel = {
        "Ingresos acumulados": ult_fila.get("Ingresos acumulados", 0) / 1e6,
        "Flujo total acumulado": ult_fila.get("Flujo total acumulado", 0) / 1e6,
        "Déficit cuenta especial acumulado": ult_fila.get("Déficit cuenta especial acumulado", 0) / 1e6,
        "Necesidades financiación acumuladas": ult_fila.get("Necesidades financiación acumuladas", 0) / 1e6,
    }
    df_panel = pd.DataFrame(panel.items(), columns=["Indicador", "Valor final (Millones €)"])
    st.dataframe(df_panel, use_container_width=True)