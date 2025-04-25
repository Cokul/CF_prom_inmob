import pandas as pd
import streamlit as st
#from indicadores.tir import calcular_tir_proyecto
from utils.u_tir import calcular_tir_promotora, calcular_tir_proyecto


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
        superficie_construida = datos.get("superficie_construida_total", 0)
        n_viviendas = datos.get("n_viviendas_ingresos", 1) or 1  # evitar división por cero
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
        #tir, error = calcular_tir_proyecto(datos)
        #if error:
        #    st.warning(error)
        #elif tir is not None:
        #    st.metric("📈 TIR del proyecto", f"{tir:.2%}")
        
        tir_proyecto, err_proy = calcular_tir_proyecto(datos)
        tir_promotora, err_prom = calcular_tir_promotora(datos)

        st.markdown("### 📊 Indicadores de rentabilidad")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📈 TIR del Proyecto**")
            st.caption("Tasa Interna de Retorno del proyecto completo, considerando todos los ingresos y costes con IVA.")
            if err_proy:
                st.warning(err_proy)
            elif tir_proyecto is not None and not pd.isna(tir_proyecto):
                st.metric("TIR Proyecto", f"{tir_proyecto * 100:.2f}%")
            else:
                st.warning("❌ No se ha podido calcular la TIR del proyecto.")

        with col2:
            st.markdown("**🏗️ TIR de la Inversión Promotora**")
            st.caption("TIR sobre la inversión asumida por la promotora: costes no cubiertos por clientes (suelo, indirectos, financieros y déficit de cuenta especial).")
            if err_prom:
                st.warning(err_prom)
            elif tir_promotora is not None and not pd.isna(tir_promotora):
                st.metric("TIR Promotora", f"{tir_promotora * 100:.2f}%")
            else:
                st.warning("❌ No se ha podido calcular la TIR de la promotora.")
            
        
