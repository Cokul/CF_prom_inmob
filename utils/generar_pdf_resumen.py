from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


def generar_pdf_resumen(datos):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    def escribir_linea(texto, y, size=10, bold=False):
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(2 * cm, y, texto)

    y = height - 2 * cm

    escribir_linea("Resumen General del Proyecto", y, size=14, bold=True)
    y -= 1.2 * cm

    # Información básica
    escribir_linea("🏢 Información básica", y, bold=True)
    y -= 0.6 * cm
    escribir_linea(f"Nombre del proyecto: {datos.get('nombre_proyecto', '')}", y); y -= 0.5 * cm
    escribir_linea(f"Ubicación: {datos.get('ubicacion', '')}", y); y -= 0.5 * cm
    escribir_linea(f"Fecha inicio comercialización: {datos.get('fecha_inicio_comercializacion')}", y); y -= 0.8 * cm

    # Superficies y unidades
    escribir_linea("📐 Superficies y unidades", y, bold=True); y -= 0.6 * cm
    escribir_linea(f"Superficie del solar: {datos.get('superficie_solar', 0):,.2f} m²", y); y -= 0.5 * cm
    escribir_linea(f"Superficie construida: {datos.get('superficie_construida_total', 0):,.2f} m²", y); y -= 0.5 * cm
    escribir_linea(f"Número de viviendas: {datos.get('n_viviendas_ingresos', 0)}", y); y -= 0.8 * cm

    # Costes clave
    escribir_linea("🧱 Costes unitarios clave", y, bold=True); y -= 0.6 * cm
    suelo = datos.get("coste_suelo", 0)
    sup_solar = datos.get("superficie_solar", 1)
    coste_suelo_m2 = suelo / sup_solar if sup_solar else 0
    escribir_linea(f"Coste suelo por m²: {coste_suelo_m2:,.2f} €", y); y -= 0.5 * cm
    escribir_linea(f"Coste ejecución por m²: {datos.get('coste_ejecucion_m2', 0):,.2f} €", y); y -= 0.8 * cm

    # IVA
    escribir_linea("💰 IVA aplicado", y, bold=True); y -= 0.6 * cm
    escribir_linea(f"IVA Viviendas: {datos.get('iva_viviendas', 0)}%", y); y -= 0.5 * cm
    escribir_linea(f"IVA Ejecución: {datos.get('iva_ejecucion', 0)}%", y); y -= 0.5 * cm
    escribir_linea(f"IVA Otros: {datos.get('iva_otros', 0)}%", y); y -= 1.0 * cm

    # TIRs
    escribir_linea("📈 Indicadores de Rentabilidad", y, bold=True); y -= 0.6 * cm
    tir_p = datos.get("resumen", {}).get("tir_proyecto")
    tir_r = datos.get("resumen", {}).get("tir_promotora")
    if tir_p is not None:
        escribir_linea(f"TIR del Proyecto: {tir_p:.2%}", y); y -= 0.5 * cm
    if tir_r is not None:
        escribir_linea(f"TIR de la Promotora: {tir_r:.2%}", y); y -= 0.5 * cm

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer