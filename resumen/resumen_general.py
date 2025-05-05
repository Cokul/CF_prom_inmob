#resumen/resumen_general.py

import pandas as pd
import streamlit as st
from indicadores.indicadores_rentabilidad import mostrar_indicadores_rentabilidad
from utils.u_tir import calcular_tir_proyecto, calcular_tir_promotora
from utils.generar_pdf_resumen import generar_pdf_resumen

def mostrar_resumen_general(datos):
    with st.expander("📋 Datos generales del proyecto", expanded=True):
        st.markdown("### 🏢 Información básica")
        st.markdown(f"**Nombre del proyecto**: {datos.get('nombre_proyecto', '')}")
        st.markdown(f"**Ubicación**: {datos.get('ubicacion', '')}")
        st.markdown(f"**Descripción**:\n\n{datos.get('descripcion_proyecto', '')}")
        fecha_comercial = datos.get("fecha_inicio_comercializacion")
        st.markdown(f"**📅 Fecha inicio comercialización**: {fecha_comercial.strftime('%Y-%m-%d') if fecha_comercial else '⚠️ No definida'}")

        st.markdown("### 📐 Superficies y unidades")
        st.markdown(f"- **Superficie del solar**: {datos.get('superficie_solar', 0):,.2f} m²")
        st.markdown(f"- **Superficie construida total**: {datos.get('superficie_construida_total', 0):,.2f} m²")
        st.markdown(f"- **Número de viviendas**: {datos.get('n_viviendas_ingresos', 0)}")
        st.markdown(f"- **Precio medio de las viviendas**: {datos.get('precio_medio_ingresos', 0):,.2f} €")

        st.markdown("### 🧱 Costes unitarios clave")
        st.markdown(f"- **Coste suelo por m²**: {datos.get('coste_suelo', 0) / datos.get('superficie_solar', 1):,.2f} €")
        st.markdown(f"- **Coste ejecución por m²**: {datos.get('coste_ejecucion_m2', 0):,.2f} €")

        st.markdown("### 🧾 Otros costes previstos")
        st.markdown(f"- **Coste financiero por vivienda**: {datos.get('coste_financiero_vivienda', 0.0):,.2f} €")
        st.markdown(f"- **% Costes comerciales sobre venta sin IVA**: {datos.get('porcentaje_costes_comerciales', 0.0):.2f}%")
        st.markdown(f"- **% Honorarios técnicos**: {datos.get('honorarios_tecnicos', 0.0):.2f}%")
        st.markdown(f"- **% Gastos de administración**: {datos.get('gastos_administracion', 0.0):.2f}%")
        st.markdown(f"- **% Otros costes indirectos**: {datos.get('otros_costes_indirectos', 0.0):.2f}%")

        st.markdown("### 💰 IVA aplicado")
        st.markdown(f"- **IVA Viviendas**: {datos.get('iva_viviendas', 0):.2f}%")
        st.markdown(f"- **IVA Ejecución**: {datos.get('iva_ejecucion', 0):.2f}%")
        st.markdown(f"- **IVA Otros**: {datos.get('iva_otros', 0):.2f}%")

        # Costes por vivienda
        n_viviendas = datos.get("n_viviendas_ingresos", 1) or 1
        precio_medio = datos.get("precio_medio_ingresos", 0)
        coste_suelo_total = datos.get("coste_suelo", 0)
        coste_ejecucion_total = datos.get("coste_total_ejecucion", 0)

        coste_suelo_vivienda = coste_suelo_total / n_viviendas
        coste_ejecucion_vivienda = coste_ejecucion_total / n_viviendas
        costes_tecnicos_vivienda = (datos.get("honorarios_tecnicos", 0.0) / 100) * coste_ejecucion_total / n_viviendas
        costes_administracion_vivienda = (datos.get("gastos_administracion", 0.0) / 100) * coste_ejecucion_total / n_viviendas
        costes_comerciales_vivienda = (datos.get("porcentaje_costes_comerciales", 0.0) / 100) * precio_medio
        costes_financieros_vivienda = datos.get("coste_financiero_vivienda", 0.0)

        coste_total = sum([
            coste_suelo_vivienda,
            coste_ejecucion_vivienda,
            costes_tecnicos_vivienda,
            costes_administracion_vivienda,
            costes_comerciales_vivienda,
            costes_financieros_vivienda
        ])
        margen_vivienda = precio_medio - coste_total
        margen_pct = (margen_vivienda / precio_medio * 100) if precio_medio else 0

        st.markdown("### 🏷️ Costes por vivienda (estimación)")
        st.markdown(f"- Coste de suelo por vivienda: {coste_suelo_vivienda:,.2f} €")
        st.markdown(f"- Coste de ejecución por vivienda: {coste_ejecucion_vivienda:,.2f} €")
        st.markdown(f"- Costes técnicos por vivienda: {costes_tecnicos_vivienda:,.2f} €")
        st.markdown(f"- Gastos de administración por vivienda: {costes_administracion_vivienda:,.2f} €")
        st.markdown(f"- Costes comerciales por vivienda: {costes_comerciales_vivienda:,.2f} €")
        st.markdown(f"- Costes financieros por vivienda: {costes_financieros_vivienda:,.2f} €")

        st.markdown(f"### 🧮 Coste total por vivienda: {coste_total:,.2f} €")
        st.markdown(f"### 💶 Margen estimado por vivienda: {margen_vivienda:,.2f} € ({margen_pct:.2f}%)")

        # Indicadores de Rentabilidad dentro del expander
        tir_proyecto, err_proy, _, _ = calcular_tir_proyecto(datos)
        tir_promotora, err_prom, _, _ = calcular_tir_promotora(datos)

        st.markdown("### 📈 Indicadores de Rentabilidad")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**TIR del Proyecto**")
            st.caption("Tasa Interna de Retorno del proyecto completo, considerando todos los ingresos y costes con IVA.")
            if err_proy:
                st.warning(err_proy)
            elif tir_proyecto is not None:
                if tir_proyecto >= 0.10:
                    color = "#d4edda"  # verde
                    leyenda = "✅ Óptima (≥10%)"
                elif tir_proyecto >= 0.05:
                    color = "#fff3cd"  # amarillo
                    leyenda = "⚠️ Aceptable (5%–10%)"
                else:
                    color = "#f8d7da"  # rojo
                    leyenda = "❌ Baja (<5%)"
                st.markdown(
                    f"<div style='background-color:{color};padding:10px;border-radius:5px;font-size:16px'><b>{tir_proyecto:.2%}</b></div>",
                    unsafe_allow_html=True
                )
                st.caption(leyenda)
            else:
                st.error("No calculable")

        with col2:
            st.markdown("**TIR de la Promotora**")
            st.caption("TIR sobre la inversión asumida por la promotora: costes no cubiertos por clientes (suelo, indirectos, financieros y déficit de cuenta especial).")
            if err_prom:
                st.warning(err_prom)
            elif tir_promotora is not None:
                if tir_promotora >= 0.10:
                    color = "#d4edda"
                    leyenda = "✅ Óptima (≥10%)"
                elif tir_promotora >= 0.05:
                    color = "#fff3cd"
                    leyenda = "⚠️ Aceptable (5%–10%)"
                else:
                    color = "#f8d7da"
                    leyenda = "❌ Baja (<5%)"
                st.markdown(
                    f"<div style='background-color:{color};padding:10px;border-radius:5px;font-size:16px'><b>{tir_promotora:.2%}</b></div>",
                    unsafe_allow_html=True
                )
                st.caption(leyenda)
            else:
                st.error("No calculable")

    # Guardar los indicadores clave para la comparativa
    datos["resumen"] = {
        "tir_proyecto": tir_proyecto,
        "tir_promotora": tir_promotora,
        "margen_unitario": margen_vivienda,
        "margen_pct": margen_pct / 100  # guardamos como decimal
    }
    
    # Descargar resumen en PDF
    st.download_button(
            label="📥 Descargar resumen en PDF",
            data=generar_pdf_resumen(datos),  # Esta función debe devolver un objeto BytesIO o similar
            file_name="resumen_general.pdf",
            mime="application/pdf"
        )

    # Mostrar la cuenta de resultados de la promoción (sin IVA)
    with st.expander("🧾 Cuenta de Resultados de la Promoción (sin IVA)", expanded=False):
        precio_medio = datos.get("precio_medio_ingresos", 0)
        num_viviendas = datos.get("n_viviendas_ingresos", 0)
        comisiones_venta = datos.get("porcentaje_costes_comerciales", 0)
        coste_ejecucion_m2 = datos.get("coste_ejecucion_m2", 0)
        superficie_total = datos.get("superficie_construida_total", 0)
        porcentaje_honorarios = datos.get("honorarios_tecnicos", 0)
        porcentaje_admin = datos.get("gastos_administracion", 0)
        gastos_financieros = datos.get("coste_financiero_vivienda", 0)
        coste_suelo = datos.get("coste_suelo", 0)

        ingresos_por_venta = precio_medio * num_viviendas
        total_comisiones = ingresos_por_venta * comisiones_venta / 100
        ingresos_netos = ingresos_por_venta - total_comisiones

        coste_ejecucion_total = coste_ejecucion_m2 * superficie_total
        coste_honorarios = coste_ejecucion_total * porcentaje_honorarios / 100
        coste_admin = coste_ejecucion_total * porcentaje_admin / 100
        coste_financiero = gastos_financieros * num_viviendas
        costes_no_ejecutivos = coste_honorarios + coste_admin + coste_financiero

        total_costes = coste_suelo + coste_ejecucion_total + costes_no_ejecutivos
        margen = ingresos_netos - total_costes

        margen_vivienda = margen / num_viviendas if num_viviendas else 0
        margen_m2 = margen / superficie_total if superficie_total else 0

        cuenta_resultados = pd.DataFrame({
            "Concepto": [
                "Ingresos por venta",
                "(-) Comisiones",
                "= Ingresos Netos",
                "Compra de terrenos",
                "Costes de ejecución",
                "Costes no ejecutivos",
                "= Total Costes",
                "= Margen",
                "Margen por vivienda",
                "Margen por m² construido"
            ],
            "Importe (€)": [
                ingresos_por_venta,
                -total_comisiones,
                ingresos_netos,
                -coste_suelo,
                -coste_ejecucion_total,
                -costes_no_ejecutivos,
                -total_costes,
                margen,
                margen_vivienda,
                margen_m2
            ]
        })

        st.dataframe(cuenta_resultados, use_container_width=True)