# inputs/in_ejecucion.py

import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from utils.excel_loader import cargar_excel_o_csv
from utils.fechas import calcular_fecha_fin, calcular_duracion_meses
from utils.fechas import convertir_columnas_fecha
from utils.fechas import normalizar_fechas_editor


def cargar_inputs_ejecucion(datos):
    with st.expander("\U0001F3D7️ Coste de ejecución", expanded=False):

        # Input manual de fecha de inicio de obra
        datos["fecha_inicio_obra"] = st.date_input(
            "\U0001F5D5️ Fecha de inicio de obra",
            value=datos.get("fecha_inicio_obra", date.today())
        )

        # Coste de ejecución por m²
        datos["coste_ejecucion_m2"] = st.number_input(
            "\U0001F4B6 Coste de ejecución por m² (€)",
            min_value=0.0,
            value=datos.get("coste_ejecucion_m2", 1600.0),
            step=50.0
        )

        # Superficie construida total
        datos["superficie_construida_total"] = st.number_input(
            "\U0001F4C0 Superficie construida total (m²)",
            min_value=0.0,
            value=datos.get("superficie_construida_total", 2000.0),
            step=10.0
        )

        # Inicialización
        usar_coste_excel = False
        archivo = st.file_uploader("\U0001F4C4 Cargar Excel de capítulos (con fechas y duración opcional)", type=["csv", "xlsx"])

        with open("assets/plantillas/plantilla_capitulos.xlsx", "rb") as file:
            st.download_button(
                label="\U0001F4E5 Descargar plantilla de capítulos de ejecución",
                data=file,
                file_name="plantilla_capitulos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        columnas_requeridas = ["Capítulo", "Coste", "Fecha inicio", "Duración (meses)"]

        if archivo:
            df = cargar_excel_o_csv(archivo)
            columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]

            if columnas_faltantes:
                st.error(f"❌ El archivo no tiene las columnas requeridas: {', '.join(columnas_faltantes)}")
            else:
                st.success("✅ Archivo cargado correctamente. Datos válidos.")
                usar_coste_excel = True

                # Calcular coste total de ejecución desde archivo
                datos["coste_total_ejecucion"] = round(df["Coste"].sum(), 2)
                st.markdown(f"**Coste total de ejecución (desde archivo)**: {datos['coste_total_ejecucion']:,.2f} €")

                # Guardar capítulos y actualizar datos
                datos["capitulos_obra"] = df.to_dict(orient="records")

        if not usar_coste_excel:
            # Si no se ha cargado el archivo, utilizamos los valores por defecto
            st.warning("Usando valores por defecto para capítulos de obra.")

            pesos_default = {
                'Actuaciones previas': 0.0008,
                'Demoliciones': 0.03554,
                'Acondicionamiento del terreno': 2.43289,
                'Cimentaciones': 2.36372,
                'Estructuras': 10.64831,
                'Fachadas y particiones': 8.71951,
                'Carpintería, cerrajería, vidrios y protecciones solares': 9.88736,
                'Remates y ayudas': 1.11051,
                'Instalaciones': 17.93712,
                'Aislamientos e impermeabilizaciones': 1.36965,
                'Cubiertas': 3.1591,
                'Revestimientos y trasdosados': 19.7394,
                'Señalización y equipamiento': 6.44508,
                'Urbanización interior de la parcela': 14.79113,
                'Gestión de residuos': 1.03846,
                'Control de calidad y ensayos': 0.05725,
                'Seguridad y salud': 0.26417
            }

            fechas_inicio_relativas = {
                'Actuaciones previas': 0,
                'Demoliciones': 0,
                'Acondicionamiento del terreno': 0,
                'Cimentaciones': 2,
                'Estructuras': 4,
                'Fachadas y particiones': 8,
                'Carpintería, cerrajería, vidrios y protecciones solares': 10,
                'Remates y ayudas': 12,
                'Instalaciones': 10,
                'Aislamientos e impermeabilizaciones': 4,
                'Cubiertas': 6,
                'Revestimientos y trasdosados': 12,
                'Señalización y equipamiento': 15,
                'Urbanización interior de la parcela': 13,
                'Gestión de residuos': 0,
                'Control de calidad y ensayos': 2,
                'Seguridad y salud': 0
            }

            duraciones_defecto = {
                'Actuaciones previas': 3,
                'Demoliciones': 3,
                'Acondicionamiento del terreno': 3,
                'Cimentaciones': 4,
                'Estructuras': 4,
                'Fachadas y particiones': 4,
                'Carpintería, cerrajería, vidrios y protecciones solares': 5,
                'Remates y ayudas': 6,
                'Instalaciones': 6,
                'Aislamientos e impermeabilizaciones': 3,
                'Cubiertas': 2,
                'Revestimientos y trasdosados': 5,
                'Señalización y equipamiento': 2,
                'Urbanización interior de la parcela': 4,
                'Gestión de residuos': 17,
                'Control de calidad y ensayos': 5,
                'Seguridad y salud': 17
            }

            planificacion = []
            for capitulo, peso in pesos_default.items():
                offset_meses = fechas_inicio_relativas.get(capitulo, 0)
                duracion = duraciones_defecto.get(capitulo, 6)
                inicio = datos["fecha_inicio_obra"] + relativedelta(months=offset_meses)
                planificacion.append({
                    "Capítulo": capitulo,
                    "Peso (%)": peso,
                    "Fecha inicio": inicio,
                    "Duración (meses)": duracion
                })

            df = pd.DataFrame(planificacion)
            datos["capitulos_obra"] = df.to_dict(orient="records")

            # Calculamos el coste total de ejecución con valores por defecto
            datos["coste_total_ejecucion"] = round(datos["superficie_construida_total"] * datos["coste_ejecucion_m2"], 2)
            st.markdown(f"**Coste total de ejecución (desde superficie y coste m²)**: {datos['coste_total_ejecucion']:,.2f} €")

        # Mostrar tabla editable
        df_temp = pd.DataFrame(datos["capitulos_obra"])
        df_temp = normalizar_fechas_editor(df_temp)  # ✅ Normalizar fechas
        df_planificacion = st.data_editor(
            pd.DataFrame(datos["capitulos_obra"]),
            column_config={
                "Capítulo": st.column_config.TextColumn("Capítulo"),
                "Peso (%)": st.column_config.NumberColumn("Peso (%)", step=0.01),
                "Coste": st.column_config.NumberColumn("Coste", step=100.0),
                "Fecha inicio": st.column_config.DateColumn("Fecha inicio"),
                "Duración (meses)": st.column_config.NumberColumn("Duración (meses)", step=1),
            },
            num_rows="dynamic",
            use_container_width=True
        )

        datos["capitulos_obra"] = df_planificacion.to_dict(orient="records")
        
        # ✅ NUEVO BLOQUE: actualizar coste_total_ejecucion si hay columna Coste
        if "Coste" in df_planificacion.columns:
            try:
                datos["coste_total_ejecucion"] = round(df_planificacion["Coste"].sum(), 2)
                st.markdown(f"**Coste total de ejecución (desde tabla)**: {datos['coste_total_ejecucion']:,.2f} €")
            except Exception as e:
                st.warning(f"No se pudo calcular el coste total desde tabla: {e}")

        # Calcular fechas de fin por capítulo
        df_planificacion["Fin"] = df_planificacion.apply(
            lambda row: row["Fecha inicio"] + relativedelta(months=row["Duración (meses)"]),
            axis=1
        )

        fechas_inicio = df_planificacion["Fecha inicio"]
        fechas_fin = df_planificacion["Fin"]

        if not fechas_inicio.empty and not fechas_fin.empty:
            fecha_inicio = min(fechas_inicio)
            fecha_fin = max(fechas_fin)
            datos["fecha_inicio_obra"] = fecha_inicio
            datos["fecha_fin_obra"] = fecha_fin
            datos["plazo_meses_obra"] = calcular_duracion_meses(fecha_inicio, fecha_fin)

            st.markdown(f"\U0001F5D5️ **Inicio de obra**: {fecha_inicio.strftime('%Y-%m-%d')}")
            st.markdown(f"\U0001F4C6 **Fin de obra**: {fecha_fin.strftime('%Y-%m-%d')}")
            st.markdown(f"⏳ **Duración estimada de la obra**: {datos['plazo_meses_obra']} meses")