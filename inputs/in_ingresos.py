import streamlit as st
import pandas as pd
from datetime import date
from utils.excel_loader import cargar_excel_o_csv
from utils.fechas import formatear_fecha
from utils.fechas import convertir_columnas_fecha
from utils.fechas import normalizar_fechas_editor

def cargar_inputs_ingresos(datos):
    with st.expander("🏠 Viviendas y calendario de ingresos", expanded=False):
        # 📅 Fecha de inicio de comercialización
        fecha_ini = datos.get("fecha_inicio_comercializacion", date.today())
        datos["fecha_inicio_comercializacion"] = st.date_input(
            "📅 Fecha de inicio de comercialización",
            value=fecha_ini
        )

        st.markdown("### 📤 Cargar desde archivo")

        archivo_viviendas = st.file_uploader("Subir archivo Excel o CSV con viviendas", type=["csv", "xlsx"])
        columnas_requeridas = ["Código", "Precio venta", "Fecha venta", "Fecha escritura"]
        with open("assets/plantillas/plantilla_viviendas.xlsx", "rb") as file:
            st.download_button(
                label="📥 Descargar plantilla de viviendas",
                data=file,
                file_name="plantilla_viviendas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Paso 1: Inicializar datos si no existen
        if "viviendas" not in datos:
            datos["viviendas"] = [
                {
                    "Código": f"VIV-{i+1}",
                    "Precio venta": 200000.0,
                    "Fecha venta": date.today(),
                    "Fecha escritura": None
                }
                for i in range(datos.get("n_viviendas", 1))
            ]

        # Paso 2: Si se sube archivo, lo usamos
        if archivo_viviendas:
            try:
                df = cargar_excel_o_csv(archivo_viviendas)

                if not all(col in df.columns for col in columnas_requeridas):
                    st.error(f"El archivo debe contener las columnas: {', '.join(columnas_requeridas)}")
                    return

                # Asegurar que las fechas son tipo date
                for col in ["Fecha venta", "Fecha escritura"]:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

                datos["viviendas"] = df[columnas_requeridas].to_dict(orient="records")
                st.success("Archivo cargado correctamente.")
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

        # Paso 3: Mostrar tabla editable
        df = pd.DataFrame(datos["viviendas"])
        df = normalizar_fechas_editor(df)  # ✅ Esta línea es la única añadida
        df_editado = st.data_editor(
            df,
            column_config={
                "Código": st.column_config.TextColumn("Código"),
                "Precio venta": st.column_config.NumberColumn("Precio venta (€)", step=1000.0),
                "Fecha venta": st.column_config.DateColumn("Fecha venta"),
                "Fecha escritura": st.column_config.DateColumn("Fecha escritura"),
            },
            num_rows="dynamic",
            use_container_width=True
        )

        # Paso 4: Guardar edición
        datos["viviendas"] = df_editado.to_dict(orient="records")

        # Paso 5: Calcular totales
        precios = [v["Precio venta"] for v in datos["viviendas"] if v["Precio venta"] > 0]
        datos["n_viviendas_ingresos"] = len(precios)
        datos["precio_medio_ingresos"] = round(sum(precios) / len(precios), 2) if precios else 0

        st.markdown(f"**Número de viviendas**: {datos['n_viviendas_ingresos']}")
        st.markdown(f"**Precio medio de venta**: {datos['precio_medio_ingresos']:,} €")

    # Bloque de fases
    with st.expander("💸 Fases de ingreso por vivienda", expanded=False):
        datos["fase_reserva"] = st.number_input(
            "Reserva (€ IVA incluido)",
            min_value=0.0,
            value=datos.get("fase_reserva", 10000.0),
            step=500.0
        )
        datos["fase_contrato_pct"] = st.number_input(
            "Contrato (%)",
            min_value=0.0,
            max_value=100.0,
            value=datos.get("fase_contrato_pct", 25.0)
        )
        datos["fase_aplazado_pct"] = st.number_input(
            "Aplazado (%)",
            min_value=0.0,
            max_value=100.0,
            value=datos.get("fase_aplazado_pct", 25.0)
        )

        iva_viv = datos.get("iva_viviendas", 10.0)
        precio_medio = datos.get("precio_medio_ingresos", 200000.0)

        if precio_medio > 0:
            reserva_sin_iva = datos["fase_reserva"] / (1 + iva_viv / 100)
            escritura_pct = 100.0 - datos["fase_contrato_pct"] - datos["fase_aplazado_pct"] - (reserva_sin_iva / precio_medio) * 100
        else:
            escritura_pct = 0.0

        escritura_pct = round(max(escritura_pct, 0.0), 2)
        datos["fase_escritura_pct"] = escritura_pct

        st.markdown(f"**Escritura (%)**: {escritura_pct:.2f} (calculado automáticamente, neto de reserva sin IVA)")
