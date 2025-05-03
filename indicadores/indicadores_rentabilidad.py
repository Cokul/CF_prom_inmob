# indicadores/indicadores_rentabilidad.py

import pandas as pd
import streamlit as st
from utils.u_tir import calcular_tir_proyecto, calcular_tir_promotora


def calcular_indicadores_resumen(datos):
    tir_proyecto, _, _, _ = calcular_tir_proyecto(datos)
    tir_promotora, _, _, _ = calcular_tir_promotora(datos)

    precio_medio = datos.get("precio_medio_ingresos", 0)
    n_viviendas = datos.get("n_viviendas_ingresos", 1) or 1
    coste_suelo_total = datos.get("coste_suelo", 0)
    coste_ejecucion_total = datos.get("coste_total_ejecucion", 0)

    coste_suelo_vivienda = - coste_suelo_total / n_viviendas
    coste_ejecucion_vivienda = - coste_ejecucion_total / n_viviendas
    costes_tecnicos_vivienda = - (datos.get("honorarios_tecnicos", 0.0) / 100) * coste_ejecucion_total / n_viviendas
    costes_administracion_vivienda = - (datos.get("gastos_administracion", 0.0) / 100) * coste_ejecucion_total / n_viviendas
    costes_comerciales_vivienda = - (datos.get("porcentaje_costes_comerciales", 0.0) / 100) * precio_medio
    costes_financieros_vivienda = - datos.get("coste_financiero_vivienda", 0.0)

    coste_total = sum([
        -coste_suelo_vivienda,
        -coste_ejecucion_vivienda,
        -costes_tecnicos_vivienda,
        -costes_administracion_vivienda,
        -costes_comerciales_vivienda,
        -costes_financieros_vivienda
    ])

    margen_unitario = precio_medio - coste_total
    margen_pct = (margen_unitario / precio_medio) if precio_medio else 0

    datos["resumen"] = {
        "tir_proyecto": tir_proyecto,
        "tir_promotora": tir_promotora,
        "precio_medio": precio_medio,
        "coste_suelo_vivienda": coste_suelo_vivienda,
        "coste_ejecucion_vivienda": coste_ejecucion_vivienda,
        "costes_tecnicos_vivienda": costes_tecnicos_vivienda,
        "costes_administracion_vivienda": costes_administracion_vivienda,
        "costes_comerciales_vivienda": costes_comerciales_vivienda,
        "costes_financieros_vivienda": costes_financieros_vivienda,
        "margen_unitario": margen_unitario,
        "margen_pct": margen_pct
    }

    return datos["resumen"]

def mostrar_indicadores_rentabilidad(datos):
    resumen = calcular_indicadores_resumen(datos)
    return resumen["tir_proyecto"], resumen["tir_promotora"]