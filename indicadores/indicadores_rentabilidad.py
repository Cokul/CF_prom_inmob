# indicadores/indicadores_rentabilidad.py

import pandas as pd
import streamlit as st
from utils.u_tir import calcular_tir_proyecto, calcular_tir_promotora

def mostrar_indicadores_rentabilidad(datos):
    st.markdown("### 📊 Indicadores de rentabilidad")

    with st.container():
        # Obtener TIRs y flujos
        tir_proyecto, err_proy, df_flujo_proy, años_proy = calcular_tir_proyecto(datos)
        tir_promotora, err_prom, df_flujo_prom, años_prom = calcular_tir_promotora(datos)

        col1, col2 = st.columns(2)

        # === TIR del Proyecto ===
        with col1:
            st.markdown("**📈 TIR del Proyecto**")
            st.caption("Tasa Interna de Retorno del proyecto completo (ingresos y costes con IVA).")

            if err_proy:
                st.warning(err_proy)
            elif tir_proyecto is not None and not pd.isna(tir_proyecto):
                badge = "✅" if tir_proyecto >= 0.10 else ("⚠️" if tir_proyecto >= 0.05 else "❌")
                st.metric(f"{badge} TIR Proyecto", f"{tir_proyecto * 100:.2f}%", help=f"Periodo: {años_proy:.2f} años")
                st.caption("**Leyenda de TIR:** ✅ >10% (óptima) • ⚠️ entre 5–10% (aceptable) • ❌ <5% (no interesa)")

                with st.expander("🔎 Ver flujos utilizados"):
                    df_mostrar = df_flujo_proy.copy()
                    df_mostrar["Mes"] = pd.to_datetime(df_mostrar["Mes"]).dt.strftime("%Y-%m")
                    st.dataframe(df_mostrar, use_container_width=True)
            else:
                st.warning("❌ No se ha podido calcular la TIR del proyecto.")

        # === TIR de la Promotora ===
        with col2:
            st.markdown("**🏗️ TIR de la Inversión Promotora**")
            st.caption("TIR sobre la inversión asumida por la promotora: suelo, indirectos, financieros y déficit.")

            if err_prom:
                st.warning(err_prom)
            elif tir_promotora is not None and not pd.isna(tir_promotora):
                badge = "✅" if tir_promotora >= 0.10 else ("⚠️" if tir_promotora >= 0.05 else "❌")
                st.metric(f"{badge} TIR Promotora", f"{tir_promotora * 100:.2f}%", help=f"Periodo: {años_prom:.2f} años")
                st.caption("**Leyenda de TIR:** ✅ >10% (óptima) • ⚠️ entre 5–10% (aceptable) • ❌ <5% (no interesa)")
                
                with st.expander("🔎 Ver flujos utilizados"):
                    df_mostrar = df_flujo_prom.copy()
                    df_mostrar["Mes"] = pd.to_datetime(df_mostrar["Mes"]).dt.strftime("%Y-%m")
                    st.dataframe(df_mostrar, use_container_width=True)
            else:
                st.warning("❌ No se ha podido calcular la TIR de la promotora.")