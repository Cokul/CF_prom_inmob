import pandas as pd
import streamlit as st
from utils.fechas import formatear_fecha

def generar_tablas_costes_indirectos(datos):
    st.markdown("## 🧾 Costes Indirectos")

    # Fechas
    fecha_inicio_obra = pd.to_datetime(datos.get("fecha_inicio_obra"))
    fecha_fin_obra = pd.to_datetime(datos.get("fecha_fin_obra"))
    if pd.isna(fecha_inicio_obra) or pd.isna(fecha_fin_obra):
        st.error("❌ Faltan fechas de inicio o fin de obra.")
        return

    meses_obra = pd.date_range(start=fecha_inicio_obra, end=fecha_fin_obra, freq="MS")

    # Parámetros
    coste_total = datos.get("coste_total_ejecucion", 0)
    porcentaje_admin = datos.get("gastos_administracion", 0) / 100
    porcentaje_tecnicos = datos.get("honorarios_tecnicos", 0) / 100
    iva = datos.get("iva_otros", 21.0) / 100

    gastos_admin = coste_total * porcentaje_admin
    honorarios_tec = coste_total * porcentaje_tecnicos

    # Honorarios técnicos: 50% inicio, 20% lineal durante la obra, 30% fin
    df_tecnicos = pd.DataFrame(index=meses_obra)
    df_tecnicos["Honorarios técnicos"] = 0.0

    if not df_tecnicos.empty:
        df_tecnicos.iloc[0, 0] += honorarios_tec * 0.50
        if len(df_tecnicos) > 2:
            lineal = honorarios_tec * 0.20 / (len(df_tecnicos) - 2)
            df_tecnicos.iloc[1:-1, 0] += lineal
        elif len(df_tecnicos) == 2:
            df_tecnicos.iloc[1, 0] += honorarios_tec * 0.20
        df_tecnicos.iloc[-1, 0] += honorarios_tec * 0.30

    # Gastos administración: 50% inicio, 50% fin
    df_admin = pd.DataFrame(index=meses_obra)
    df_admin["Gastos de administración"] = 0.0
    if not df_admin.empty:
        df_admin.iloc[0, 0] += gastos_admin * 0.50
        df_admin.iloc[-1, 0] += gastos_admin * 0.50

    # Unir y aplicar signo negativo (salida de caja)
    df_indirectos = df_tecnicos.join(df_admin, how="outer").fillna(0)
    df_indirectos["Total"] = df_indirectos.sum(axis=1)
    df_indirectos *= -1

    # Añadir fila total
    fila_total = pd.DataFrame(df_indirectos.sum()).T
    fila_total.index = ["Total"]
    df_indirectos_final = pd.concat([df_indirectos, fila_total])

    # Aplicar IVA sobre valores ya negativos
    df_con_iva = df_indirectos * (1 + iva)
    fila_total_iva = pd.DataFrame(df_con_iva.sum()).T
    fila_total_iva.index = ["Total"]
    df_indirectos_iva_final = pd.concat([df_con_iva, fila_total_iva])

    # Mostrar
    st.markdown("### 💶 Costes indirectos sin IVA")
    df_mostrar = df_indirectos_final.copy()
    df_mostrar.index = [formatear_fecha(i) if not isinstance(i, str) else i for i in df_mostrar.index]
    st.dataframe(df_mostrar, use_container_width=True)

    st.markdown("### 💶 Costes indirectos con IVA")
    df_mostrar_iva = df_indirectos_iva_final.copy()
    df_mostrar_iva.index = [formatear_fecha(i) if not isinstance(i, str) else i for i in df_mostrar_iva.index]
    st.dataframe(df_mostrar_iva, use_container_width=True)

    # Guardar
    df_indirectos_final = df_indirectos_final.reset_index().rename(columns={"index": "Mes"})
    df_indirectos_iva_final = df_indirectos_iva_final.reset_index().rename(columns={"index": "Mes"})
    datos["costes_indirectos_sin_iva"] = df_indirectos_final.to_dict(orient="records")
    datos["costes_indirectos_con_iva"] = df_indirectos_iva_final.to_dict(orient="records")