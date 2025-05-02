# utils/u_tir.py

import numpy_financial as npf
import pandas as pd

def calcular_tir_proyecto(datos):
    flujo = datos.get("flujo_caja", [])
    if not flujo:
        return None, "No se ha generado el flujo de caja.", pd.DataFrame(), 0

    df = pd.DataFrame(flujo)
    df = df[df["Mes"] != "Total"]

    if "Mes" not in df.columns or "Flujo mensual" not in df.columns:
        return None, "Faltan columnas necesarias en el flujo de caja.", pd.DataFrame(), 0

    df["Mes"] = pd.to_datetime(df["Mes"], errors="coerce")
    df = df.dropna(subset=["Mes"]).sort_values("Mes")

    flujos = pd.to_numeric(df["Flujo mensual"], errors="coerce").fillna(0)
    df_resultado = df[["Mes"]].copy()
    df_resultado["Flujo utilizado"] = flujos

    if not any(f < 0 for f in flujos) or not any(f > 0 for f in flujos):
        return None, "Los flujos deben contener al menos un valor positivo y uno negativo.", df_resultado, 0

    try:
        tir = npf.irr(flujos)
        años = (df["Mes"].max() - df["Mes"].min()).days / 365.25
        return tir, None, df_resultado, round(años, 2)
    except Exception as e:
        return None, f"Error al calcular la TIR del proyecto: {e}", df_resultado, 0


def calcular_tir_promotora(datos):
    tabla_necesidades = datos.get("tabla_necesidades_financiacion")
    flujo_caja = datos.get("flujo_caja")

    if not tabla_necesidades or not flujo_caja:
        return None, "Faltan datos de necesidades de financiación o flujo de caja.", pd.DataFrame(), 0

    try:
        df_necesidades = pd.DataFrame(tabla_necesidades)
        df_necesidades = df_necesidades[df_necesidades["Mes"] != "Total"]
        df_necesidades["Mes"] = pd.to_datetime(df_necesidades["Mes"], errors="coerce")
        df_necesidades = df_necesidades.dropna(subset=["Mes"]).set_index("Mes")

        df_ingresos = pd.DataFrame(flujo_caja)
        df_ingresos = df_ingresos[df_ingresos["Mes"] != "Total"]
        df_ingresos["Mes"] = pd.to_datetime(df_ingresos["Mes"], errors="coerce")
        df_ingresos = df_ingresos.dropna(subset=["Mes"]).set_index("Mes")

        if "Ingresos" not in df_ingresos.columns or "Total necesidades" not in df_necesidades.columns:
            return None, "Faltan columnas necesarias.", pd.DataFrame(), 0

        df_comb = df_ingresos[["Ingresos"]].join(df_necesidades[["Total necesidades"]], how="outer").fillna(0)
        df_comb["Flujo utilizado"] = df_comb["Ingresos"] + df_comb["Total necesidades"]
        df_comb = df_comb.reset_index()[["Mes", "Flujo utilizado"]]

        if not any(df_comb["Flujo utilizado"] < 0) or not any(df_comb["Flujo utilizado"] > 0):
            return None, "Los flujos deben contener al menos un valor positivo y uno negativo.", df_comb, 0

        tir = npf.irr(df_comb["Flujo utilizado"].values)
        años = (df_comb["Mes"].max() - df_comb["Mes"].min()).days / 365.25
        return tir, None, df_comb, round(años, 2)

    except Exception as e:
        return None, f"Error al calcular la TIR de la promotora: {e}", pd.DataFrame(), 0