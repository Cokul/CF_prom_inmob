import pandas as pd
import streamlit as st
import plotly.express as px

def mostrar_graficas_ingresos(datos):
    st.header("📉 Gráficas de ingresos")

    def graficar_tabla(nombre_tabla, titulo_barra, titulo_linea):
        data = datos.get(nombre_tabla, [])
        if not data:
            st.warning(f"La tabla '{nombre_tabla}' no contiene datos válidos.")
            return

        df = pd.DataFrame(data)

        # Asegurar que 'Mes' esté como columna
        if "Mes" not in df.columns:
            if "index" in df.columns:
                df.rename(columns={"index": "Mes"}, inplace=True)
            elif "level_0" in df.columns:
                df.rename(columns={"level_0": "Mes"}, inplace=True)
            else:
                st.error("No se encuentra la columna 'Mes'.")
                return

        df = df[df["Mes"] != "Total"]

        # Formato largo
        df_largo = df.melt(id_vars=["Mes"], var_name="Fase", value_name="Importe")
        df_largo["Importe"] = pd.to_numeric(df_largo["Importe"], errors="coerce")
        df_largo.dropna(inplace=True)
        df_largo["Mes"] = pd.to_datetime(df_largo["Mes"])
        df_largo = df_largo.sort_values("Mes")

        # Gráfico de barras por fase
        fig1 = px.bar(df_largo, x="Mes", y="Importe", color="Fase", barmode="stack", title=titulo_barra)
        st.plotly_chart(fig1, use_container_width=True)

        # Gráfico de línea total
        if "Total" in df.columns:
            df_total = df[["Mes", "Total"]].copy()
            df_total["Mes"] = pd.to_datetime(df_total["Mes"])
            df_total = df_total.sort_values("Mes")

            fig2 = px.line(df_total, x="Mes", y="Total", markers=True, title=titulo_linea)
            st.plotly_chart(fig2, use_container_width=True)

    # BLOQUE: Ingresos
    st.subheader("💶 Ingresos mensuales por fase (sin IVA)")
    graficar_tabla(
        "tabla_ingresos_sin_iva",
        "Distribución mensual por fase (sin IVA)",
        "Evolución mensual del total (sin IVA)"
    )

    st.markdown("---")

    st.subheader("💶 Ingresos mensuales por fase (con IVA)")
    graficar_tabla(
        "tabla_ingresos_con_iva",
        "Distribución mensual por fase (con IVA)",
        "Evolución mensual del total (con IVA)"
    )

    st.markdown("---")

    # BLOQUE: Comisiones
    st.subheader("💸 Comisiones mensuales por fase (sin IVA)")
    graficar_tabla(
        "tabla_comisiones_sin_iva",
        "Comisiones por fase (sin IVA)",
        "Total mensual de comisiones (sin IVA)"
    )

    st.markdown("---")

    st.subheader("💸 Comisiones mensuales por fase (con IVA)")
    graficar_tabla(
        "tabla_comisiones_con_iva",
        "Comisiones por fase (con IVA)",
        "Total mensual de comisiones (con IVA)"
    )