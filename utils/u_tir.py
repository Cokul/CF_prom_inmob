import numpy_financial as npf
import pandas as pd

def calcular_tir_proyecto(datos):
    flujo = datos.get("flujo_caja", [])
    if not flujo:
        return None, "No se ha generado el flujo de caja."

    df = pd.DataFrame(flujo)
    df = df[df["Mes"] != "Total"]
    if "Mes" not in df.columns or "Flujo mensual" not in df.columns:
        return None, "Faltan columnas necesarias en el flujo de caja."

    flujos = pd.to_numeric(df["Flujo mensual"], errors="coerce").fillna(0).values

    try:
        tir = npf.irr(flujos)
        if pd.isna(tir):
            return None, "No se ha podido calcular la TIR del proyecto."
        return tir, None
    except Exception as e:
        return None, f"Error al calcular la TIR del proyecto: {e}"

def calcular_tir_promotora(datos):
    tabla_necesidades = datos.get("tabla_necesidades_financiacion")
    flujo_caja = datos.get("flujo_caja")

    if not tabla_necesidades or not flujo_caja:
        return None, "Faltan datos de necesidades de financiación o flujo de caja."

    try:
        df_necesidades = pd.DataFrame(tabla_necesidades)
        df_necesidades = df_necesidades[df_necesidades["Mes"] != "Total"]
        df_necesidades["Mes"] = pd.to_datetime(df_necesidades["Mes"])
        df_necesidades = df_necesidades.set_index("Mes")

        df_ingresos = pd.DataFrame(flujo_caja)
        df_ingresos = df_ingresos[df_ingresos["Mes"] != "Total"]
        df_ingresos["Mes"] = pd.to_datetime(df_ingresos["Mes"])
        df_ingresos = df_ingresos.set_index("Mes")

        if "Ingresos" not in df_ingresos.columns or "Total necesidades" not in df_necesidades.columns:
            return None, "Faltan columnas necesarias."

        df_comb = df_ingresos[["Ingresos"]].join(df_necesidades[["Total necesidades"]], how="outer").fillna(0)
        df_comb["Flujo neto"] = df_comb["Ingresos"] + df_comb["Total necesidades"]

        flujos = df_comb["Flujo neto"].values
        tir = npf.irr(flujos)

        if pd.isna(tir):
            return None, "No se ha podido calcular la TIR de la promotora."
        return tir, None

    except Exception as e:
        return None, f"Error al calcular la TIR de la promotora: {e}"
