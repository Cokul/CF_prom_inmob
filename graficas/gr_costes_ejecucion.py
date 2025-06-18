import pandas as pd
import plotly.express as px
import streamlit as st
from dateutil.relativedelta import relativedelta

def mostrar_graficas_costes_ejecucion(datos):
    st.subheader("🏗️ Gráficas de costes de ejecución")

    df_plan = pd.DataFrame(datos.get("planificacion_capitulos", []))
    if df_plan.empty:
        st.warning("No hay datos de planificación por capítulo.")
        return

    superficie = datos.get("superficie_construida_total", 0)
    coste_m2 = datos.get("coste_ejecucion_m2", 0)
    coste_total = superficie * coste_m2

    df_plan["Fecha inicio"] = pd.to_datetime(df_plan["Fecha inicio"], errors="coerce")
    df_plan["Duración (meses)"] = pd.to_numeric(df_plan["Duración (meses)"], errors="coerce").fillna(1).astype(int)
    df_plan["Fecha fin"] = df_plan.apply(lambda row: row["Fecha inicio"] + relativedelta(months=row["Duración (meses)"]), axis=1)

    if "Coste (€)" in df_plan.columns:
        df_plan["Coste capitulo"] = df_plan["Coste (€)"]
    elif any(col for col in df_plan.columns if "coste" in col.lower() and "cap" in col.lower()):
        # Buscar columna que contenga "coste" y "cap" (para detectar variantes con tilde)
        col_candidata = next(col for col in df_plan.columns if "coste" in col.lower() and "cap" in col.lower())
        df_plan["Coste capitulo"] = df_plan[col_candidata]

    elif "Peso (%)" in df_plan.columns:
        df_plan["Coste capitulo"] = df_plan["Peso (%)"] / 100 * coste_total
    else:
        st.error("No se puede calcular el coste por capítulo: faltan columnas 'Coste (€)', 'Coste capitulo' o 'Peso (%)'.")
        return

    df_plan["Coste mensual"] = df_plan["Coste capitulo"] / df_plan["Duración (meses)"]

    fecha_fin_obra = df_plan["Fecha fin"].max()
    fechas = pd.date_range(start=df_plan["Fecha inicio"].min(), end=fecha_fin_obra, freq="MS")
    df_mensual = pd.DataFrame(index=fechas)

    for _, row in df_plan.iterrows():
        inicio = row["Fecha inicio"]
        duracion = row["Duración (meses)"]
        coste_mensual = float(-row["Coste mensual"])
        meses = pd.date_range(start=inicio, periods=duracion, freq="MS")
        for mes in meses:
            if mes not in df_mensual.index:
                df_mensual.loc[mes] = 0.0
            capitulo = row["Capítulo"]
            if capitulo not in df_mensual.columns:
                df_mensual[capitulo] = 0.0
            df_mensual.at[mes, capitulo] += coste_mensual

    df_mensual.fillna(0.0, inplace=True)
    df_mensual["Total"] = df_mensual.sum(axis=1)
    df_mensual = df_mensual.sort_index()

    # 🧱 Treemap de pesos por capítulo
    st.markdown("### 🗂️ Distribución del peso por capítulo")

    # Calcular "Peso (%)" si no existe, usando "Coste (€)" o "Coste capitulo"
    if "Peso (%)" not in df_plan.columns:
        if "Coste (€)" in df_plan.columns:
            total_coste = df_plan["Coste (€)"].sum()
            if total_coste > 0:
                df_plan["Peso (%)"] = df_plan["Coste (€)"] / total_coste * 100
        elif "Coste capitulo" in df_plan.columns:
            total_coste = df_plan["Coste capitulo"].sum()
            if total_coste != 0:
                df_plan["Peso (%)"] = df_plan["Coste capitulo"] / total_coste * 100

    if "Peso (%)" in df_plan.columns:
        df_plan["Peso (%)"] = df_plan["Peso (%)"].abs()
        df_pesos = df_plan[["Capítulo", "Peso (%)"]].copy().dropna(subset=["Peso (%)"])
        if df_pesos["Peso (%)"].sum() > 0:
            fig_treemap = px.treemap(
                df_pesos,
                path=["Capítulo"],
                values="Peso (%)",
                title="Distribución de pesos por capítulo en el coste de ejecución",
                color="Peso (%)",
                color_continuous_scale="OrRd"
            )
            st.plotly_chart(fig_treemap, use_container_width=True)
        else:
            st.info("No se muestra el treemap porque todos los pesos son cero.")
    else:
        st.info("No se muestra el treemap porque no se han definido pesos por capítulo.")


    # 📅 Gantt
    st.markdown("### 📅 Cronograma de ejecución por capítulos")
    df_gantt = df_plan[["Capítulo", "Fecha inicio", "Fecha fin"]].copy()
    df_gantt = df_gantt.rename(columns={"Capítulo": "Task", "Fecha inicio": "Start", "Fecha fin": "Finish"})
    orden_original = df_plan["Capítulo"].tolist()
    fig_gantt = px.timeline(
        df_gantt,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Task",
        title="Cronograma de ejecución por capítulos",
        category_orders={"Task": orden_original}
    )
    st.plotly_chart(fig_gantt, use_container_width=True)

    # 📉 Coste acumulado mensual sin IVA
    st.markdown("### 📉 Coste acumulado mensual (sin IVA)")
    df_plot = df_mensual.reset_index().rename(columns={"index": "Mes"})
    df_plot["Acumulado"] = df_plot["Total"].cumsum()
    fig = px.line(
        df_plot,
        x="Mes",
        y="Acumulado",
        markers=True,
        title="Coste acumulado mensual sin IVA"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 📊 Coste acumulado mensual con IVA
    st.markdown("### 📊 Coste acumulado mensual (con IVA)")
    iva = datos.get("iva_ejecucion", 21.0) / 100
    df_plot_con_iva = df_mensual.copy()
    df_plot_con_iva["Total con IVA"] = df_plot_con_iva["Total"] * (1 + iva)
    df_plot_con_iva = df_plot_con_iva.reset_index().rename(columns={"index": "Mes"})
    df_plot_con_iva["Acumulado con IVA"] = df_plot_con_iva["Total con IVA"].cumsum()
    fig_con_iva = px.line(
        df_plot_con_iva,
        x="Mes",
        y="Acumulado con IVA",
        markers=True,
        title="Coste acumulado mensual con IVA"
    )
    st.plotly_chart(fig_con_iva, use_container_width=True)
