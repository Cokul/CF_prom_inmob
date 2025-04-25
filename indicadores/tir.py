# indicadores/tir.py

import pandas as pd
import numpy_financial as npf

def calcular_tir_proyecto(datos):
    if "flujo_caja" not in datos:
        return None, "❌ No se ha generado la tabla de flujo de caja."

    df = pd.DataFrame(datos["flujo_caja"])
    df = df[df["Mes"] != "Total"]  # Ignoramos fila total si existe

    if "Flujo mensual" not in df.columns:
        return None, "❌ Falta la columna 'Flujo mensual' en la tabla de flujo de caja."

    flujos = df["Flujo mensual"].astype(float).values

    try:
        tir_mensual = npf.irr(flujos)
        tir_anual = (1 + tir_mensual) ** 12 - 1
        return tir_anual, None
    except Exception as e:
        return None, f"❌ Error al calcular la TIR: {e}"