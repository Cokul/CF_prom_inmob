# utils/fechas.py

from datetime import datetime, date
import pandas as pd

def formatear_fecha(fecha: date) -> str:
    """Devuelve una fecha en formato dd/mm/aaaa"""
    return fecha.strftime("%d/%m/%Y") if fecha else ""

def sumar_meses(fecha, meses):
    """Devuelve una nueva fecha sumando X meses."""
    if not fecha:
        return None
    # Solución para PerformanceWarning: utilizar pandas DateOffset
    return fecha + pd.DateOffset(months=meses)

def calcular_fecha_fin(fecha_inicio, duracion_meses):
    """Devuelve la fecha de fin sumando los meses a la fecha de inicio."""
    return sumar_meses(fecha_inicio, duracion_meses)

def calcular_duracion_meses(fecha_inicio, fecha_fin):
    """Devuelve la duración en meses entre dos fechas."""
    if not fecha_inicio or not fecha_fin:
        return None
    return (fecha_fin.year - fecha_inicio.year) * 12 + (fecha_fin.month - fecha_inicio.month)

def convertir_fecha_excel(valor):
    """Convierte un valor tipo datetime o string en objeto date."""
    try:
        if isinstance(valor, str):
            return datetime.strptime(valor, "%Y-%m-%d").date()
        elif isinstance(valor, datetime):
            return valor.date()
        elif isinstance(valor, pd.Timestamp):
            return valor.to_pydatetime().date()
    except:
        return None

def generar_rango_mensual(fecha_inicio, fecha_fin):
    """
    Genera una lista de fechas (primer día de mes) entre fecha_inicio y fecha_fin, ambos incluidos.
    """
    if isinstance(fecha_inicio, str):
        fecha_inicio = pd.to_datetime(fecha_inicio)
    if isinstance(fecha_fin, str):
        fecha_fin = pd.to_datetime(fecha_fin)

    fechas = []
    actual = fecha_inicio.replace(day=1)
    while actual <= fecha_fin:
        fechas.append(actual)
        actual += pd.DateOffset(months=1)  # Usamos DateOffset para sumar meses
    return fechas

def convertir_columnas_fecha(df, columnas):
    """Convierte columnas a datetime64[ns] si existen."""
    for col in columnas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df[col] = df[col].astype("datetime64[ns]")  # <- forzar el tipo
    return df

def normalizar_fechas_editor(df, columnas_fecha=None):
    """
    Convierte columnas especificadas a datetime si no lo son.
    Si no se especifican columnas, convierte automáticamente todas las que se llamen 'Fecha ...'.
    """
    if columnas_fecha is None:
        columnas_fecha = [col for col in df.columns if col.lower().startswith("fecha")]

    for col in columnas_fecha:
        if col in df.columns:
            df.loc[:, col] = pd.to_datetime(df[col], errors="coerce")  # Usamos .loc[]

    return df