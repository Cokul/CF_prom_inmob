import os
import json
import shutil
import streamlit as st
from datetime import datetime

def gestionar_proyecto_y_version():
    # Carpeta para proyectos
    CARPETA_PROYECTOS = "proyectos"
    os.makedirs(CARPETA_PROYECTOS, exist_ok=True)

    with st.sidebar.expander("📂 Gestión de Proyecto y Versión", expanded=True):
        st.markdown("### 📁 Proyecto")
        proyectos = sorted([f for f in os.listdir(CARPETA_PROYECTOS) if os.path.isdir(os.path.join(CARPETA_PROYECTOS, f))])
        proyecto_sel = st.selectbox("Selecciona un proyecto", ["Nuevo proyecto..."] + proyectos)

        if proyecto_sel == "Nuevo proyecto...":
            nuevo_nombre = st.text_input("Nombre del nuevo proyecto")
            if st.button("Crear proyecto") and nuevo_nombre:
                ruta_nuevo = os.path.join(CARPETA_PROYECTOS, nuevo_nombre)
                if not os.path.exists(ruta_nuevo):
                    os.makedirs(ruta_nuevo)
                    st.success(f"Proyecto '{nuevo_nombre}' creado.")
                    st.rerun()
                else:
                    st.warning("Ese nombre de proyecto ya existe.")
        else:
            ruta_proyecto = os.path.join(CARPETA_PROYECTOS, proyecto_sel)

            if st.button("🗑️ Eliminar proyecto completo", type="primary"):
                shutil.rmtree(ruta_proyecto)
                st.success(f"Proyecto '{proyecto_sel}' eliminado.")
                st.rerun()

            st.markdown("### 🧾 Versión")
            versiones = sorted([v.replace(".json", "") for v in os.listdir(ruta_proyecto) if v.endswith(".json")])
            version_sel = st.selectbox("Selecciona una versión", ["Nueva versión..."] + versiones)

            if version_sel == "Nueva versión...":
                nueva_version = st.text_input("Nombre de la nueva versión")
                if st.button("Crear versión"):
                    if nueva_version:
                        ruta_version = os.path.join(ruta_proyecto, nueva_version + ".json")
                        if not os.path.exists(ruta_version):
                            with open(ruta_version, "w", encoding="utf-8") as f:
                                json.dump({}, f, indent=2, default=str)
                            st.session_state["ruta_version_actual"] = ruta_version
                            st.success("Versión guardada correctamente.")
                            st.rerun()
                        else:
                            st.warning("Ese nombre de versión ya existe.")
            else:
                ruta_version = os.path.join(ruta_proyecto, version_sel + ".json")
                st.session_state["ruta_version_actual"] = ruta_version

                if st.button("📥 Cargar versión seleccionada"):
                    try:
                        with open(ruta_version, "r", encoding="utf-8") as f:
                            st.session_state["datos_proyecto"] = json.load(f)
                        fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta_version)).strftime("%Y-%m-%d %H:%M:%S")
                        st.success(f"Versión cargada: {version_sel} (guardada el {fecha_mod})")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error al cargar la versión: {e}")

                if st.button("🧬 Duplicar versión"):
                    nueva_version = f"{version_sel}_copia"
                    ruta_copia = os.path.join(ruta_proyecto, nueva_version + ".json")
                    shutil.copy(ruta_version, ruta_copia)
                    st.success(f"Versión duplicada como: {nueva_version}")
                    st.rerun()

                if st.button("🗑️ Eliminar esta versión"):
                    os.remove(ruta_version)
                    st.success(f"Versión '{version_sel}' eliminada.")
                    st.rerun()

                if st.button("💾 Guardar versión actual"):
                    with open(ruta_version, "w", encoding="utf-8") as f:
                        json.dump(st.session_state.get("datos_proyecto", {}), f, indent=2, default=str)
                    fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta_version)).strftime("%Y-%m-%d %H:%M:%S")
                    st.success(f"Versión guardada correctamente el {fecha_mod}")

                comentario = st.text_input("✏️ Comentario sobre esta versión", value=st.session_state.get("datos_proyecto", {}).get("comentario", ""))
                if comentario != st.session_state.get("datos_proyecto", {}).get("comentario", ""):
                    st.session_state["datos_proyecto"]["comentario"] = comentario
                    with open(ruta_version, "w", encoding="utf-8") as f:
                        json.dump(st.session_state["datos_proyecto"], f, indent=2, ensure_ascii=False, default=str)
                    st.success("Comentario guardado correctamente")

                st.markdown(f"**Versión activa:** `{version_sel}`  \n📅 **Última modificación:** {datetime.fromtimestamp(os.path.getmtime(ruta_version)).strftime('%Y-%m-%d %H:%M:%S')}")
                if st.session_state["datos_proyecto"].get("comentario"):
                    st.info(f"💬 {st.session_state['datos_proyecto']['comentario']}")