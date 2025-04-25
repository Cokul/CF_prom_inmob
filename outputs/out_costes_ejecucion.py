# outputs/out_costes_ejecucion.py

import pandas as pd
import streamlit as st
from utils.planificacion_helpers import preparar_planificacion_costes
from utils.formatos import formatear_moneda
from utils.fechas import formatear_fecha
from pandas.tseries.offsets import DateOffset

def generar_tablas_costes_ejecucion(datos):
    # Preparar la planificación de los capítulos
    df_plan = preparar_planificacion_costes(datos)
    
    if df_plan.empty:
        st.warning("No hay capítulos de obra cargados.")
        return

    # Asegurarnos de que si se carga el archivo Excel, usamos los valores directamente del archivo
    if "Capítulo" in df_plan.columns and "Coste" in df_plan.columns:
        # Si se cargaron los datos de coste desde el archivo, no usamos los pesos y tomamos los costes directamente del archivo
        st.warning("Usando los valores cargados desde el archivo de Excel.")
        df_plan["Coste capítulo"] = df_plan["Coste"]
    else:
        # Verificación de la columna "Peso (%)"
        if "Peso (%)" not in df_plan.columns:
            st.warning("No se encontró la columna 'Peso (%)'. Usando valores por defecto.")
        
            # Asignamos los valores predeterminados a 'Peso (%)' y calculamos los costes de ejecución
            pesos_default = {
                'Actuaciones previas': 0.0008,
                'Demoliciones': 0.03554,
                'Acondicionamiento del terreno': 2.43289,
                'Cimentaciones': 2.36372,
                'Estructuras': 10.64831,
                'Fachadas y particiones': 8.71951,
                'Carpintería, cerrajería, vidrios y protecciones solares': 9.88736,
                'Remates y ayudas': 1.11051,
                'Instalaciones': 17.93712,
                'Aislamientos e impermeabilizaciones': 1.36965,
                'Cubiertas': 3.1591,
                'Revestimientos y trasdosados': 19.7394,
                'Señalización y equipamiento': 6.44508,
                'Urbanización interior de la parcela': 14.79113,
                'Gestión de residuos': 1.03846,
                'Control de calidad y ensayos': 0.05725,
                'Seguridad y salud': 0.26417
            }
        
            # Asignamos los valores predeterminados a 'Peso (%)' y calculamos los costes de ejecución
            df_plan["Peso (%)"] = df_plan["Capítulo"].map(pesos_default).fillna(0)
        
            # Verificar que 'coste_total_ejecucion' no esté vacío
            if "coste_total_ejecucion" in datos and datos["coste_total_ejecucion"]:
                df_plan["Coste capítulo"] = df_plan["Peso (%)"] * datos["coste_total_ejecucion"]
            else:
                df_plan["Coste capítulo"] = 0

        else:
            # Convertir 'Peso (%)' a numérico (por si es texto o tiene comas)
            df_plan["Peso (%)"] = pd.to_numeric(df_plan["Peso (%)"], errors="coerce") / 100
        
            # Verificar que "Peso (%)" no tenga valores NaN y que la división haya sido exitosa
            df_plan["Peso (%)"] = df_plan["Peso (%)"].fillna(0)
        
            # Calcular el "Coste capítulo" multiplicando el "Peso (%)" por el "coste_total_ejecucion"
            if "coste_total_ejecucion" in datos and datos["coste_total_ejecucion"]:
                df_plan["Coste capítulo"] = df_plan["Peso (%)"] * datos["coste_total_ejecucion"]
            else:
                df_plan["Coste capítulo"] = 0

    # Multiplicamos por -1 para que los costes sean negativos (importante para cálculo de financiación, movimientos de cuenta, etc.)
    df_plan["Coste capítulo"] = df_plan["Coste capítulo"] * -1

    # Calcular los costes mensuales
    df_costes_mensual = pd.DataFrame()
    for _, row in df_plan.iterrows():
        inicio = row["Fecha inicio"]
        duracion = row["Duración (meses)"]
        coste = row["Coste capítulo"]

        for i in range(duracion):
            mes = (inicio + DateOffset(months=i)).strftime("%Y-%m")
            df_costes_mensual.loc[mes, row["Capítulo"]] = coste / duracion

    df_costes_mensual = df_costes_mensual.fillna(0)
    df_costes_mensual["Total"] = df_costes_mensual.sum(axis=1)
    total_row = df_costes_mensual.sum().to_frame().T
    total_row.index = ["Total"]
    df_costes_mensual = pd.concat([df_costes_mensual, total_row])

    # Calcular los costes con IVA
    df_costes_iva = df_costes_mensual.copy()
    iva_ejecucion = datos.get("iva_ejecucion", 10.0) / 100
    df_costes_iva[df_costes_iva.columns] = df_costes_iva[df_costes_iva.columns] * (1 + iva_ejecucion)

    # Mostrar las tablas de planificación
    st.markdown("### 📅 Planificación por capítulo")
    df_mostrar_plan = df_plan.copy()
    df_mostrar_plan["Fecha inicio"] = df_mostrar_plan["Fecha inicio"].dt.strftime("%Y-%m")
    df_mostrar_plan["Fecha fin"] = df_mostrar_plan["Fecha fin"].dt.strftime("%Y-%m")
    df_mostrar_plan["Coste capítulo"] = df_mostrar_plan["Coste capítulo"].apply(formatear_moneda)
    st.dataframe(df_mostrar_plan, use_container_width=True)

    st.markdown("### 💸 Costes mensuales (sin IVA)")
    st.dataframe(df_costes_mensual.style.format(formatear_moneda), use_container_width=True)

    st.markdown("### 💸 Costes mensuales (con IVA ejecución)")
    st.dataframe(df_costes_iva.style.format(formatear_moneda), use_container_width=True)

    # Guardar los resultados en 'datos' para su posterior uso
    datos["planificacion_capitulos"] = df_plan.to_dict(orient="records")
    datos["costes_mensuales_ejecucion"] = df_costes_mensual.reset_index().rename(columns={"index": "Mes"}).to_dict(orient="records")
    datos["costes_mensuales_ejecucion_iva"] = df_costes_iva.reset_index().rename(columns={"index": "Mes"}).to_dict(orient="records")