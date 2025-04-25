import pandas as pd
from io import BytesIO
import streamlit as st

def cargar_excel_o_csv(archivo, columnas_requeridas=None, convertir_fechas=None):
    """
    Carga un archivo Excel o CSV y devuelve un DataFrame validado.

    Args:
        archivo: objeto subido con st.file_uploader
        columnas_requeridas: lista de nombres de columnas obligatorias
        convertir_fechas: lista de nombres de columnas que deben convertirse a fecha

    Returns:
        df (DataFrame) o None si hay error
    """
    try:
        if archivo.name.endswith(".csv"):
            df = pd.read_csv(archivo, encoding="utf-8", sep=";", decimal=",")
        else:
            df = pd.read_excel(archivo)

        # Validación de columnas
        if columnas_requeridas:
            if not all(col in df.columns for col in columnas_requeridas):
                st.error(f"❌ El archivo debe contener las columnas: {', '.join(columnas_requeridas)}")
                return None

        # Conversión de fechas
        if convertir_fechas:
            for col in convertir_fechas:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

        return df

    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
        return None
    
def exportar_excel(df, nombre_archivo="archivo.xlsx"):
    """
    Devuelve un botón de descarga de un DataFrame como archivo Excel.

    Args:
        df: DataFrame a exportar.
        nombre_archivo: nombre sugerido para el archivo descargado.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Hoja1")
    output.seek(0)

    st.download_button(
        label="⬇️ Descargar Excel",
        data=output,
        file_name=nombre_archivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def exportar_excel_con_portada(diccionario_df, datos_generales, nombre_archivo="resumen_promocion.xlsx"):
    """
    Exporta varios DataFrames en un único archivo Excel con portada resumen en la primera hoja.

    Args:
        diccionario_df: dict con nombre_hoja como clave y DataFrame como valor.
        datos_generales: dict con los datos clave del proyecto.
        nombre_archivo: nombre sugerido para el archivo descargado.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # 🧾 Hoja de portada
        portada = pd.DataFrame({
            "Dato": [
                "Nombre del Proyecto",
                "Ubicación",
                "Nº Viviendas",
                "Precio Medio Venta (€)",
                "Coste del Suelo/m²",
                "Coste Ejecución/m²",
                "Superficie Construida (m²)",
            ],
            "Valor": [
                datos_generales.get("nombre_proyecto", "—"),
                datos_generales.get("ubicacion", "—"),
                datos_generales.get("n_viviendas_ingresos", "—"),
                datos_generales.get("precio_medio_ingresos", "—"),
                datos_generales.get("coste_suelo_m2", "—"),
                datos_generales.get("coste_ejecucion_m2", "—"),
                datos_generales.get("superficie_construida_total", "—"),
            ]
        })
        portada.to_excel(writer, index=False, sheet_name="Resumen")

        # 🔄 Añadir cada DataFrame en su hoja
        for nombre_hoja, df in diccionario_df.items():
            df.to_excel(writer, index=False, sheet_name=nombre_hoja[:31])

    output.seek(0)

    st.download_button(
        label="⬇️ Descargar Excel con resumen",
        data=output,
        file_name=nombre_archivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )