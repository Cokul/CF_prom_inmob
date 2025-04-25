import streamlit as st

def cargar_inputs_generales(datos):
    with st.expander("🏢 Datos generales del proyecto", expanded=False):
        datos["nombre_proyecto"] = st.text_input("Nombre del proyecto", value=datos.get("nombre_proyecto", ""))
        datos["ubicacion"] = st.text_input("Ubicación", value=datos.get("ubicacion", ""))
        datos["descripcion_proyecto"] = st.text_area("Descripción del proyecto (opcional)", value=datos.get("descripcion_proyecto", ""), height=100)

    with st.expander("💰 IVA aplicado", expanded=False):
        datos["iva_viviendas"] = st.number_input("IVA Viviendas (%)", min_value=0.0, max_value=100.0, value=datos.get("iva_viviendas", 10.0))
        datos["iva_ejecucion"] = st.number_input("IVA Ejecución (%)", min_value=0.0, max_value=100.0, value=datos.get("iva_ejecucion", 0.0))
        datos["iva_otros"] = st.number_input("IVA Otros (%)", min_value=0.0, max_value=100.0, value=datos.get("iva_otros", 21.0))
