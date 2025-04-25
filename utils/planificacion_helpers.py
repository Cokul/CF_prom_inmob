# utils/planificacion_helpers.py

import pandas as pd
from dateutil.relativedelta import relativedelta
import streamlit as st

@st.cache_data
def preparar_planificacion_costes(datos):
    df_capitulos = pd.DataFrame(datos.get("capitulos_obra", []))
    if df_capitulos.empty:
        return pd.DataFrame()

    df_capitulos["Fecha inicio"] = pd.to_datetime(df_capitulos["Fecha inicio"], errors="coerce")
    df_capitulos["Duración (meses)"] = pd.to_numeric(df_capitulos["Duración (meses)"], errors="coerce").fillna(1).astype(int)
    df_capitulos["Fecha fin"] = df_capitulos.apply(
        lambda row: row["Fecha inicio"] + relativedelta(months=int(row["Duración (meses)"])),
        axis=1
    )
    return df_capitulos