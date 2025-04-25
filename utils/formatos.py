def formatear_miles(valor):
    """Formatea un número con separador de miles y sin decimales."""
    try:
        return f"{float(round(valor, 2)):,}".replace(",", ".")
    except:
        return "—"

def formatear_moneda(valor, decimales=2):
    """Formatea un número como moneda en euros."""
    try:
        formato = f"{{:,.{decimales}f}} €"
        return formato.format(valor).replace(",", "_").replace(".", ",").replace("_", ".")
    except:
        return "—"

def porcentaje(valor, decimales=2):
    """Convierte un decimal a porcentaje."""
    try:
        return f"{round(valor * 100, decimales)}%"
    except:
        return "—"