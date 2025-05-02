import pandas as pd
import streamlit as st

# Función para generar la tabla de flujo de caja general
def generar_tabla_flujo_caja(datos):
    st.markdown("## 💸 Flujo de Caja General")
    st.markdown("#### Importes IVA incluido")  # Texto añadido

    # Cargar los datos de ingresos con IVA
    if "tabla_ingresos_con_iva" not in datos:
        st.error("❌ Faltan datos de ingresos con IVA.")
        return

    df_ingresos = pd.DataFrame(datos["tabla_ingresos_con_iva"])

    # Filtrar cualquier fila que contenga el valor 'Total' en la columna 'Mes'
    df_ingresos = df_ingresos[df_ingresos["Mes"] != "Total"]

    # Aseguramos que las fechas son correctas
    df_ingresos["Mes"] = pd.to_datetime(df_ingresos["Mes"], errors='coerce').dt.strftime('%Y-%m')

    # Verificamos si hay algún valor que no se pudo convertir a fecha
    if df_ingresos["Mes"].isnull().any():
        st.error("❌ Hay datos en la columna 'Mes' que no son fechas válidas.")
        return

    # Filtrar solo la columna 'Total' de los ingresos con IVA
    df_ingresos = df_ingresos[["Mes", "Total"]]

    # Renombrar la columna "Total" a "Ingresos"
    df_ingresos = df_ingresos.rename(columns={"Total": "Ingresos"})

    # Cargar el coste del suelo con IVA
    if "coste_suelo_con_iva" not in datos:
        st.error("❌ Faltan datos de coste de suelo con IVA.")
        return

    coste_suelo_con_iva = -datos["coste_suelo_con_iva"]  # El coste del suelo es negativo
    fecha_suelo = pd.to_datetime(datos["fecha_adquisicion_suelo"]).strftime('%Y-%m')

    # Crear un DataFrame para el coste de suelo
    df_suelo = pd.DataFrame({
        "Mes": [fecha_suelo],
        "Suelo": [coste_suelo_con_iva]  # Renombrado de "Coste suelo con IVA" a "Suelo"
    })

    # Crear un DataFrame para el coste de suelo
    df_suelo = pd.DataFrame({
        "Mes": [fecha_suelo],
        "Suelo": [coste_suelo_con_iva]  # Renombrado de "Coste suelo con IVA" a "Suelo"
    })

    # Cargar comisiones con IVA (de los datos de out_ingresos.py)
    if "tabla_comisiones_con_iva" not in datos:
        st.error("❌ Faltan datos de comisiones con IVA.")
        return

    df_comisiones = pd.DataFrame(datos["tabla_comisiones_con_iva"])

    # Filtrar cualquier fila que contenga el valor 'Total' en la columna 'Mes'
    df_comisiones = df_comisiones[df_comisiones["Mes"] != "Total"]

    # Filtrar solo las columnas necesarias (Mes y Total de Comisiones)
    df_comisiones = df_comisiones[["Mes", "Total"]]

    # Renombrar la columna "Total" a "Comisiones"
    df_comisiones = df_comisiones.rename(columns={"Total": "Comisiones"})

    # Cargar los costes de ejecución
    if "costes_mensuales_ejecucion_iva" not in datos:
        st.error("❌ Faltan datos de costes de ejecución.")
        return

    df_costes_ejecucion = pd.DataFrame(datos["costes_mensuales_ejecucion_iva"])

    # Filtrar cualquier fila que contenga el valor 'Total' en la columna 'Mes'
    df_costes_ejecucion = df_costes_ejecucion[df_costes_ejecucion["Mes"] != "Total"]

    # Filtrar solo la columna 'T. Costes' de los costes de ejecución
    df_costes_ejecucion = df_costes_ejecucion[["Mes", "T. Costes"]]

    # Renombrar la columna "T. Costes" a "Coste ejecución"
    df_costes_ejecucion = df_costes_ejecucion.rename(columns={"T. Costes": "Coste ejecución"})

    # Cargar los costes indirectos
    if "costes_indirectos_con_iva" not in datos:
        st.error("❌ Faltan datos de costes indirectos.")
        return

    df_costes_indirectos = pd.DataFrame(datos["costes_indirectos_con_iva"])

    # Filtrar cualquier fila que contenga el valor 'Total' en la columna 'Mes'
    df_costes_indirectos = df_costes_indirectos[df_costes_indirectos["Mes"] != "Total"]

    # Filtrar solo la columna 'Total' de los costes indirectos
    df_costes_indirectos = df_costes_indirectos[["Mes", "Total"]]

    # Renombrar la columna "Total" a "Costes Indirectos"
    df_costes_indirectos = df_costes_indirectos.rename(columns={"Total": "Costes Indirectos"})

    # Asegurar que las fechas son correctas para los costes indirectos
    df_costes_indirectos["Mes"] = pd.to_datetime(df_costes_indirectos["Mes"]).dt.strftime('%Y-%m')

    # Cargar los costes financieros
    if "costes_financieros" not in datos:
        st.error("❌ Faltan datos de costes financieros.")
        return

    df_costes_financieros = pd.DataFrame(datos["costes_financieros"])

    # Filtrar cualquier fila que contenga el valor 'Total' en la columna 'Mes'
    df_costes_financieros = df_costes_financieros[df_costes_financieros["Mes"] != "Total"]

    # Filtrar solo la columna 'Coste financiero'
    df_costes_financieros = df_costes_financieros[["Mes", "Coste financiero"]]

    # Renombrar la columna "Coste financiero" a "Costes Financieros"
    df_costes_financieros = df_costes_financieros.rename(columns={"Coste financiero": "Costes Financieros"})

    # Unir los DataFrames de ingresos, coste de suelo, comisiones, costes de ejecución, costes indirectos y costes financieros
    df_combined = pd.merge(df_ingresos, df_suelo, on="Mes", how="outer")
    df_combined = pd.merge(df_combined, df_comisiones, on="Mes", how="outer")
    df_combined = pd.merge(df_combined, df_costes_ejecucion, on="Mes", how="outer")
    df_combined = pd.merge(df_combined, df_costes_indirectos, on="Mes", how="outer")
    df_combined = pd.merge(df_combined, df_costes_financieros, on="Mes", how="outer")

    # Asegurarse de que solo las columnas numéricas sean sumadas
    df_final = df_combined.groupby("Mes", as_index=False).sum(numeric_only=True)

    # Reordenar las columnas para que el orden sea Mes, Ingresos, Comisiones, Suelo, Coste ejecución, Costes Indirectos y Costes Financieros
    df_final = df_final[["Mes", "Ingresos", "Comisiones", "Suelo", "Coste ejecución", "Costes Indirectos", "Costes Financieros"]]

    # Añadir columna de Flujo Neto (sumando los valores anteriores)
    df_final["Flujo Neto"] = df_final["Ingresos"] + df_final["Comisiones"] + df_final["Suelo"] + df_final["Coste ejecución"] + df_final["Costes Indirectos"] + df_final["Costes Financieros"]

    # Añadir columna de Flujo Neto Acumulado
    df_final["Flujo Neto Acumulado"] = df_final["Flujo Neto"].cumsum()

    # Añadir fila de total
    fila_total = pd.DataFrame({
        "Mes": ["Total"], 
        "Ingresos": [df_final["Ingresos"].sum()],
        "Comisiones": [df_final["Comisiones"].sum()],
        "Suelo": [df_final["Suelo"].sum()],
        "Coste ejecución": [df_final["Coste ejecución"].sum()],
        "Costes Indirectos": [df_final["Costes Indirectos"].sum()],
        "Costes Financieros": [df_final["Costes Financieros"].sum()],
        "Flujo Neto": [df_final["Flujo Neto"].sum()],
        "Flujo Neto Acumulado": [df_final["Flujo Neto Acumulado"].iloc[-1]]
    })

    # Concatenar la fila de total al final de la tabla
    df_final = pd.concat([df_final, fila_total], ignore_index=True)

    # Asegurar que existe la columna 'Flujo mensual' para el cálculo de la TIR
    df_final["Flujo mensual"] = df_final["Flujo Neto"]

    # Guardar la tabla de flujo de caja en 'datos' para su posterior uso
    datos["flujo_caja"] = df_final.to_dict(orient="records")
    st.session_state["flujo_caja"] = df_final

    st.success("Flujo de caja general con ingresos, comisiones, coste del suelo, costes de ejecución, costes indirectos y costes financieros mostrado correctamente.")

    # Mostrar la tabla final dentro de un expander
    with st.expander("📊 Flujo de Caja General", expanded=False):
        df_mostrar = df_final.copy()
        df_mostrar.index = [i.strftime("%Y-%m") if isinstance(i, pd.Timestamp) else str(i) for i in df_mostrar.index]
        st.dataframe(df_mostrar, use_container_width=True)

    # Añadir los tres nuevos expanders vacíos
    with st.expander("🏦 Movimientos de la cuenta especial intervenida", expanded=False):
        if "tabla_ingresos_con_iva" not in datos or "costes_mensuales_ejecucion_iva" not in datos:
            st.error("❌ Faltan datos necesarios.")
            return

        df_ingresos = pd.DataFrame(datos["tabla_ingresos_con_iva"])
        df_costes_ejec = pd.DataFrame(datos["costes_mensuales_ejecucion_iva"])

        df_ingresos = df_ingresos[df_ingresos["Mes"] != "Total"]
        df_costes_ejec = df_costes_ejec[df_costes_ejec["Mes"] != "Total"]

        for df in [df_ingresos, df_costes_ejec]:
            df["Mes_dt"] = pd.to_datetime(df["Mes"], errors="coerce")
            if df["Mes_dt"].isnull().any():
                st.error("❌ Hay fechas inválidas en los datos.")
                return
            df["Mes"] = df["Mes_dt"].dt.strftime("%Y-%m")
            df.drop(columns=["Mes_dt"], inplace=True)

        ingresos_col = [col for col in ["Reserva", "Contrato", "Aplazado"] if col in df_ingresos.columns]
        for col in ingresos_col:
            df_ingresos[col] = pd.to_numeric(df_ingresos[col], errors="coerce").fillna(0)
        df_ingresos["Ingresos cuenta especial"] = df_ingresos[ingresos_col].sum(axis=1)
        df_ingresos = df_ingresos[["Mes", "Ingresos cuenta especial"]].groupby("Mes", as_index=False).sum()

        df_costes_ejec = df_costes_ejec[["Mes", "T. Costes"]].rename(columns={"T. Costes": "Coste ejecución"})
        df_costes_ejec = df_costes_ejec.groupby("Mes", as_index=False).sum()

        df_cuenta = pd.merge(df_ingresos, df_costes_ejec, on="Mes", how="outer").fillna(0)
        df_cuenta["Flujo mensual"] = df_cuenta["Ingresos cuenta especial"] + df_cuenta["Coste ejecución"]

        saldo_acumulado = []
        deficit = []
        saldo = 0

        for flujo in df_cuenta["Flujo mensual"]:
            saldo_temp = saldo + flujo
            if saldo_temp >= 0:
                saldo = saldo_temp
                saldo_acumulado.append(saldo)
                deficit.append(0)
            else:
                saldo = 0
                saldo_acumulado.append(0)
                deficit.append(saldo_temp)

        df_cuenta["Saldo acumulado"] = saldo_acumulado
        df_cuenta["Déficit cuenta especial"] = deficit
        df_cuenta["Mes"] = df_cuenta["Mes"].astype(str)

        # Crear fila de totales correctamente alineada
        columnas_orden = ["Mes", "Ingresos cuenta especial", "Coste ejecución", "Flujo mensual", "Saldo acumulado", "Déficit cuenta especial"]

        fila_total = pd.DataFrame([{
            "Mes": "Total",
            "Ingresos cuenta especial": df_cuenta["Ingresos cuenta especial"].sum(),
            "Coste ejecución": df_cuenta["Coste ejecución"].sum(),
            "Flujo mensual": df_cuenta["Flujo mensual"].sum(),
            "Saldo acumulado": df_cuenta["Saldo acumulado"].iloc[-1],
            "Déficit cuenta especial": df_cuenta["Déficit cuenta especial"].sum()
        }])[columnas_orden]

        df_cuenta = pd.concat([df_cuenta, fila_total], ignore_index=True)

        st.dataframe(df_cuenta, use_container_width=True)
        st.success("Movimientos de la cuenta especial intervenida mostrados correctamente.")

        # Guardar para uso posterior
        datos["movimientos_cuenta_especial"] = df_cuenta.to_dict(orient="records")

    # Necesidades de financiación
    with st.expander("📊 Necesidades de financiación", expanded=False):
        try:
            # 1. Comisiones pre-escritura
            df_comisiones = pd.DataFrame(datos["tabla_comisiones_con_iva"])
            df_comisiones = df_comisiones[df_comisiones["Mes"] != "Total"]
            df_comisiones["Mes"] = pd.to_datetime(df_comisiones["Mes"], errors="coerce")
            df_comisiones = df_comisiones.dropna(subset=["Mes"])

            fases_pre_esc = [f for f in ["Reserva", "Contrato", "Aplazado"] if f in df_comisiones.columns]
            for col in fases_pre_esc:
                df_comisiones[col] = pd.to_numeric(df_comisiones[col], errors="coerce").fillna(0)

            df_comisiones["Comisiones pre-escritura"] = df_comisiones[fases_pre_esc].sum(axis=1)
            df_comisiones = df_comisiones[["Mes", "Comisiones pre-escritura"]].groupby("Mes").sum()

            # 2. Coste suelo con IVA
            if "coste_suelo_con_iva" not in datos or "fecha_adquisicion_suelo" not in datos:
                st.error("❌ Faltan datos del suelo.")
                return

            fecha_suelo = pd.to_datetime(datos["fecha_adquisicion_suelo"])
            coste_suelo = -datos["coste_suelo_con_iva"]
            df_suelo = pd.DataFrame({"Coste suelo": [coste_suelo]}, index=[fecha_suelo])

            # 3. Costes indirectos
            df_indirectos = pd.DataFrame(datos["costes_indirectos_con_iva"])
            df_indirectos = df_indirectos[df_indirectos["Mes"] != "Total"]
            df_indirectos["Mes"] = pd.to_datetime(df_indirectos["Mes"], errors="coerce")
            df_indirectos = df_indirectos.dropna(subset=["Mes"])
            df_indirectos["Costes indirectos"] = pd.to_numeric(df_indirectos["Total"], errors="coerce").fillna(0)
            df_indirectos = df_indirectos[["Mes", "Costes indirectos"]].groupby("Mes").sum()

            # 4. Costes financieros
            df_financieros = pd.DataFrame(datos["costes_financieros"])
            df_financieros = df_financieros[df_financieros["Mes"] != "Total"]
            df_financieros["Mes"] = pd.to_datetime(df_financieros["Mes"], errors="coerce")
            df_financieros = df_financieros.dropna(subset=["Mes"])
            df_financieros["Costes financieros"] = pd.to_numeric(df_financieros["Coste financiero"], errors="coerce").fillna(0)
            df_financieros = df_financieros[["Mes", "Costes financieros"]].groupby("Mes").sum()

            # 5. Déficit cuenta especial
            df_deficit = pd.DataFrame(datos.get("movimientos_cuenta_especial", []))
            if "Mes" not in df_deficit.columns:
                df_deficit = df_deficit.rename(columns={"Unnamed: 0": "Mes"})
            df_deficit["Mes"] = pd.to_datetime(df_deficit["Mes"], errors="coerce")
            df_deficit = df_deficit.dropna(subset=["Mes"])
            df_deficit["Déficit cuenta especial"] = pd.to_numeric(df_deficit["Déficit cuenta especial"], errors="coerce").fillna(0)
            df_deficit = df_deficit[["Mes", "Déficit cuenta especial"]].groupby("Mes").sum()

            # 6. Unión de todos los bloques
            dfs = [df_comisiones, df_suelo, df_indirectos, df_financieros, df_deficit]
            df_necesidades = pd.concat(dfs, axis=1).fillna(0).sort_index()

            # 7. Cálculos de totales y acumulado
            df_necesidades["Total necesidades"] = df_necesidades.sum(axis=1)
            df_necesidades["Acumulado"] = df_necesidades["Total necesidades"].cumsum()

            # 8. Fila de totales
            fila_total = pd.DataFrame([{
                "Comisiones pre-escritura": df_necesidades["Comisiones pre-escritura"].sum(),
                "Coste suelo": df_necesidades["Coste suelo"].sum(),
                "Costes indirectos": df_necesidades["Costes indirectos"].sum(),
                "Costes financieros": df_necesidades["Costes financieros"].sum(),
                "Déficit cuenta especial": df_necesidades["Déficit cuenta especial"].sum(),
                "Total necesidades": df_necesidades["Total necesidades"].sum(),
                "Acumulado": df_necesidades["Acumulado"].iloc[-1]
            }], index=["Total"])

            df_necesidades_final = pd.concat([df_necesidades, fila_total])
            df_necesidades_final.index = [i.strftime("%Y-%m") if isinstance(i, pd.Timestamp) else str(i) for i in df_necesidades_final.index]

            # 9. Mostrar y guardar
            st.dataframe(df_necesidades_final, use_container_width=True)
            datos["tabla_necesidades_financiacion"] = df_necesidades_final.reset_index().rename(columns={"index": "Mes"}).to_dict(orient="records")
            st.success("Tabla de necesidades de financiación mostrada correctamente.")

        except Exception as e:
            st.error(f"❌ Error al generar la tabla de necesidades de financiación: {e}")

    with st.expander("📈 Resumen Acumulado", expanded=False):
        try:
            # 1. Ingresos acumulados
            df_ingresos = pd.DataFrame(datos["tabla_ingresos_con_iva"])
            df_ingresos = df_ingresos[df_ingresos["Mes"] != "Total"]
            df_ingresos["Mes"] = pd.to_datetime(df_ingresos["Mes"], errors="coerce")
            df_ingresos = df_ingresos.dropna(subset=["Mes"])
            df_ingresos["Total"] = pd.to_numeric(df_ingresos["Total"], errors="coerce").fillna(0)
            df_ingresos = df_ingresos.sort_values("Mes")
            df_ingresos["Ingresos acumulados"] = df_ingresos["Total"].cumsum()
            df_ingresos = df_ingresos[["Mes", "Ingresos acumulados"]].set_index("Mes")

            # 2. Flujo total acumulado
            df_flujo = pd.DataFrame(datos["flujo_caja"])
            df_flujo = df_flujo[df_flujo["Mes"] != "Total"]
            df_flujo["Mes"] = pd.to_datetime(df_flujo["Mes"], errors="coerce")
            df_flujo = df_flujo.dropna(subset=["Mes"])
            df_flujo["Flujo total acumulado"] = pd.to_numeric(df_flujo["Flujo Neto Acumulado"], errors="coerce").fillna(0)
            df_flujo = df_flujo[["Mes", "Flujo total acumulado"]].set_index("Mes")

            # 3. Déficit cuenta especial acumulado
            df_deficit = pd.DataFrame(datos["movimientos_cuenta_especial"])
            if "Mes" not in df_deficit.columns:
                df_deficit = df_deficit.rename(columns={"Unnamed: 0": "Mes"})
            df_deficit["Mes"] = pd.to_datetime(df_deficit["Mes"], errors="coerce")
            df_deficit = df_deficit.dropna(subset=["Mes"])
            df_deficit["Déficit cuenta especial"] = pd.to_numeric(df_deficit["Déficit cuenta especial"], errors="coerce").fillna(0)
            df_deficit = df_deficit.sort_values("Mes")
            df_deficit["Déficit cuenta especial acumulado"] = df_deficit["Déficit cuenta especial"].cumsum()
            df_deficit = df_deficit[["Mes", "Déficit cuenta especial acumulado"]].set_index("Mes")

            # 4. Necesidades financiación acumuladas
            df_necesidades = pd.DataFrame(datos["tabla_necesidades_financiacion"])
            df_necesidades = df_necesidades[df_necesidades["Mes"] != "Total"]
            df_necesidades["Mes"] = pd.to_datetime(df_necesidades["Mes"], errors="coerce")
            df_necesidades = df_necesidades.dropna(subset=["Mes"])
            df_necesidades["Acumulado"] = pd.to_numeric(df_necesidades["Acumulado"], errors="coerce").fillna(0)
            df_necesidades = df_necesidades[["Mes", "Acumulado"]].rename(columns={"Acumulado": "Necesidades financiación acumuladas"}).set_index("Mes")

            # 5. Unir todas las tablas y aplicar forward fill
            df_resumen = pd.concat([df_ingresos, df_flujo, df_deficit, df_necesidades], axis=1)
            df_resumen = df_resumen.sort_index().fillna(method="ffill").fillna(0)
            df_resumen.index = [i.strftime("%Y-%m") for i in df_resumen.index]

            # 6. Mostrar y guardar
            st.dataframe(df_resumen, use_container_width=True)
            datos["tabla_resumen_acumulado"] = df_resumen.reset_index().rename(columns={"index": "Mes"}).to_dict(orient="records")
            st.success("Resumen acumulado generado correctamente.")

        except Exception as e:
            st.error(f"❌ Error al generar el resumen acumulado: {e}")