from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


def generar_pdf_resumen(datos):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 2 * cm

    def escribir(texto, y, size=10, bold=False):
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(2 * cm, y, texto)

    def salto_linea(y, salto=0.5):
        return y - salto * cm

    def div(num, den):
        return num / den if den else 0

    # === Página 1: Resumen general ===
    escribir("Resumen General del Proyecto", y, size=14, bold=True); y = salto_linea(y, 1.2)

    # Información básica
    escribir("🏢 Información básica", y, bold=True); y = salto_linea(y)
    escribir(f"Nombre del proyecto: {datos.get('nombre_proyecto', '')}", y); y = salto_linea(y)
    escribir(f"Ubicación: {datos.get('ubicacion', '')}", y); y = salto_linea(y)
    escribir(f"Descripción: {datos.get('descripcion_proyecto', '')}", y); y = salto_linea(y)
    fecha_com = datos.get("fecha_inicio_comercializacion")
    escribir(f"Fecha inicio comercialización: {fecha_com.strftime('%Y-%m-%d') if fecha_com else 'No definida'}", y); y = salto_linea(y, 0.8)

    # Superficies y unidades
    escribir("📐 Superficies y unidades", y, bold=True); y = salto_linea(y)
    superficie_solar = datos.get("superficie_solar", 0)
    superficie_total = datos.get("superficie_construida_total", 0)
    n_viviendas = datos.get("n_viviendas_ingresos", 1) or 1
    precio_medio = datos.get("precio_medio_ingresos", 0)
    escribir(f"Superficie del solar: {superficie_solar:,.2f} m²", y); y = salto_linea(y)
    escribir(f"Superficie construida total: {superficie_total:,.2f} m²", y); y = salto_linea(y)
    escribir(f"Número de viviendas: {n_viviendas}", y); y = salto_linea(y)
    escribir(f"Precio medio de las viviendas: {precio_medio:,.2f} €", y); y = salto_linea(y, 0.8)

    # Costes clave
    escribir("🧱 Costes unitarios clave", y, bold=True); y = salto_linea(y)
    escribir(f"Coste suelo por m²: {div(datos.get('coste_suelo', 0), superficie_solar):,.2f} €", y); y = salto_linea(y)
    escribir(f"Coste ejecución por m²: {datos.get('coste_ejecucion_m2', 0):,.2f} €", y); y = salto_linea(y, 0.8)

    # Otros costes
    escribir("🧾 Otros costes previstos", y, bold=True); y = salto_linea(y)
    escribir(f"Coste financiero por vivienda: {datos.get('coste_financiero_vivienda', 0):,.2f} €", y); y = salto_linea(y)
    escribir(f"% Costes comerciales: {datos.get('porcentaje_costes_comerciales', 0):.2f}%", y); y = salto_linea(y)
    escribir(f"% Honorarios técnicos: {datos.get('honorarios_tecnicos', 0):.2f}%", y); y = salto_linea(y)
    escribir(f"% Administración: {datos.get('gastos_administracion', 0):.2f}%", y); y = salto_linea(y)
    escribir(f"% Otros costes indirectos: {datos.get('otros_costes_indirectos', 0):.2f}%", y); y = salto_linea(y, 0.8)

    # IVA
    escribir("💰 IVA aplicado", y, bold=True); y = salto_linea(y)
    escribir(f"IVA Viviendas: {datos.get('iva_viviendas', 0):.2f}%", y); y = salto_linea(y)
    escribir(f"IVA Ejecución: {datos.get('iva_ejecucion', 0):.2f}%", y); y = salto_linea(y)
    escribir(f"IVA Otros: {datos.get('iva_otros', 0):.2f}%", y); y = salto_linea(y, 1.0)

    # Margen y TIR
    escribir("💶 Margen estimado por vivienda", y, bold=True); y = salto_linea(y)
    margen_unit = datos.get("resumen", {}).get("margen_unitario", 0)
    margen_pct = datos.get("resumen", {}).get("margen_pct", 0) * 100
    escribir(f"Margen por vivienda: {margen_unit:,.2f} € ({margen_pct:.2f}%)", y); y = salto_linea(y, 0.8)

    escribir("📈 Indicadores de Rentabilidad", y, bold=True); y = salto_linea(y)
    tir_p = datos.get("resumen", {}).get("tir_proyecto")
    tir_r = datos.get("resumen", {}).get("tir_promotora")
    if tir_p is not None:
        escribir(f"TIR del Proyecto: {tir_p:.2%}", y); y = salto_linea(y)
    if tir_r is not None:
        escribir(f"TIR de la Promotora: {tir_r:.2%}", y); y = salto_linea(y)

    # === Página 2: Cuenta de Resultados ===
    c.showPage()
    y = height - 2 * cm
    escribir("🧾 Cuenta de Resultados de la Promoción (sin IVA)", y, size=14, bold=True); y = salto_linea(y, 1.0)

    # Datos base
    suelo = datos.get("coste_suelo", 0)
    ejec_m2 = datos.get("coste_ejecucion_m2", 0)
    sup_total = superficie_total
    ejec_total = ejec_m2 * sup_total
    honor = ejec_total * datos.get("honorarios_tecnicos", 0) / 100
    admin = ejec_total * datos.get("gastos_administracion", 0) / 100
    financieros = datos.get("coste_financiero_vivienda", 0) * n_viviendas
    comerciales = precio_medio * datos.get("porcentaje_costes_comerciales", 0) / 100 * n_viviendas

    ingresos = precio_medio * n_viviendas
    ingresos_netos = ingresos - comerciales
    costes_no_ejec = honor + admin + financieros
    total_costes = suelo + ejec_total + costes_no_ejec
    margen_total = ingresos_netos - total_costes
    margen_viv = div(margen_total, n_viviendas)
    margen_m2 = div(margen_total, sup_total)

    # Tabla
    bloques = [
        ("Ingresos por venta", ingresos),
        ("(-) Comisiones", -comerciales),
        ("= Ingresos Netos", ingresos_netos),
        ("Compra de terrenos", -suelo),
        ("Costes de ejecución", -ejec_total),
        ("Costes no ejecutivos", -costes_no_ejec),
        ("= Total Costes", -total_costes),
        ("= Margen", margen_total),
        ("Margen por vivienda", margen_viv),
        ("Margen por m² construido", margen_m2),
    ]

    for concepto, valor in bloques:
        escribir(f"{concepto}: {valor:,.2f} €", y); y = salto_linea(y)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer