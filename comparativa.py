#comparativa.py

import streamlit as st
import pandas as pd
import json
from utils.proyectos import listar_proyectos_guardados_con_fecha
from indicadores.indicadores_rentabilidad import calcular_indicadores_resumen

def mostrar_comparativa():
    st.title("Comparativa de promociones")

    # 🔹 1. Listar con metadatos
    proyectos_info = listar_proyectos_guardados_con_fecha()
    claves = [p[0] for p in proyectos_info]
    mapa_ruta = {p[0]: p[1] for p in proyectos_info}
    mapa_fecha = {p[0]: p[2] for p in proyectos_info}

    seleccion = st.multiselect(
        "Selecciona promociones o versiones para comparar:",
        options=claves
    )

    # 🔹 2. Cargar datos seleccionados
    datos_promociones = {}
    for clave in seleccion:
        ruta = mapa_ruta[clave]
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)

        # 👇 Calcular indicadores aunque no estén guardados
        calcular_indicadores_resumen(datos)
        datos_promociones[clave] = datos

    # 🔹 3. Mostrar metadatos
    if seleccion:
        st.subheader("📄 Metadatos de las versiones seleccionadas")
        tabla_meta = pd.DataFrame({
            "Proyecto": seleccion,
            "Fecha de guardado": [mapa_fecha[k] for k in seleccion]
        })
        st.table(tabla_meta)

    # 🔹 Tabla comparativa con indicadores clave extendidos
    resumen = {}
    indicadores = [
        "tir_proyecto", "tir_promotora", "precio_medio",
        "coste_suelo_vivienda", "coste_ejecucion_vivienda",
        "costes_tecnicos_vivienda", "costes_administracion_vivienda",
        "costes_comerciales_vivienda", "costes_financieros_vivienda",
        "margen_unitario", "margen_pct"
    ]

    nombres = {
        "tir_proyecto": "TIR Proyecto",
        "tir_promotora": "TIR Promotora",
        "precio_medio": "Precio medio vivienda (€)",
        "coste_suelo_vivienda": "Coste suelo (€/vvda)",
        "coste_ejecucion_vivienda": "Coste ejecución (€/vvda)",
        "costes_tecnicos_vivienda": "Costes técnicos (€/vvda)",
        "costes_administracion_vivienda": "Gastos administración (€/vvda)",
        "costes_comerciales_vivienda": "Costes comerciales (€/vvda)",
        "costes_financieros_vivienda": "Costes financieros (€/vvda)",
        "margen_unitario": "Margen (€/vvda)",
        "margen_pct": "Margen %"
    }

    for clave, datos in datos_promociones.items():
        resumen_data = datos.get("resumen", {})
        for ind in indicadores:
            valor = resumen_data.get(ind)
            if ind not in resumen:
                resumen[ind] = {}
            if ind == "margen_pct" or ind.startswith("tir_"):
                resumen[ind][clave] = f"{valor:.2%}" if isinstance(valor, (int, float)) else "ND"
            else:
                resumen[ind][clave] = f"{valor:,.0f} €" if isinstance(valor, (int, float)) else "ND"

    st.subheader("📊 Comparativa de indicadores clave")

    # Crear DataFrame y transponer: indicadores como filas, versiones como columnas
    df = pd.DataFrame(resumen).T
    df.index = df.index.map(lambda x: nombres.get(x, x))  # Aplica nombres amigables

    # Mostrar tabla nativa de Streamlit
    st.dataframe(df, use_container_width=True)