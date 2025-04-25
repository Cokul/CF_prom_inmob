import pandas as pd
import streamlit as st

def generar_tabla_flujo_caja(datos):
    st.markdown("## 💸 Flujo de Caja General")

    tablas_y_columnas = {
        "tabla_ingresos_con_iva": "Total",
        "tabla_comisiones_con_iva": "Total",
        "costes_mensuales_ejecucion_iva": "Total",
        "costes_indirectos_con_iva": "Total",
        "costes_financieros": "Coste financiero"
    }

    dfs = {}

    def cargar_df(clave, nombre_columna):
        if clave not in datos:
            st.error(f"❌ FALTA la tabla '{clave}' en datos.")
            return None
        try:
            df = pd.DataFrame(datos[clave])
        except Exception as e:
            st.error(f"❌ Error al convertir '{clave}' a DataFrame: {e}")
            return None
        if "Mes" not in df.columns:
            st.error(f"❌ La tabla '{clave}' no tiene columna 'Mes'.")
            return None
        if nombre_columna not in df.columns:
            st.error(f"❌ La tabla '{clave}' no tiene columna '{nombre_columna}'.")
            return None
        df = df[df["Mes"] != "Total"]
        df["Mes"] = pd.to_datetime(df["Mes"], errors="coerce")
        df = df.dropna(subset=["Mes"])
        df = df.set_index("Mes")
        return df[[nombre_columna]].rename(columns={nombre_columna: clave})

    for clave, columna in tablas_y_columnas.items():
        df = cargar_df(clave, columna)
        if df is None:
            st.warning("No se puede calcular el flujo de caja por errores anteriores.")
            return
        dfs[clave] = df

    if isinstance(datos.get("coste_suelo"), (int, float)):
        fecha = datos.get("fecha_adquisicion_suelo")
        if not fecha:
            st.error("❌ Falta la fecha de adquisición del suelo.")
            return
        try:
            mes = pd.to_datetime(fecha)
            df_suelo = pd.DataFrame({mes: [-datos["coste_suelo"]]}, index=[mes]).T
            df_suelo.columns = ["coste_suelo"]
            dfs["coste_suelo"] = df_suelo
        except Exception as e:
            st.error(f"❌ Error al procesar fecha de adquisición del suelo: {e}")
            return
    else:
        df = cargar_df("coste_suelo", "Coste suelo")
        if df is None:
            return
        dfs["coste_suelo"] = df

    df = dfs["tabla_ingresos_con_iva"].join([
        dfs["tabla_comisiones_con_iva"],
        dfs["coste_suelo"],
        dfs["costes_mensuales_ejecucion_iva"],
        dfs["costes_indirectos_con_iva"],
        dfs["costes_financieros"]
    ], how="outer").fillna(0).sort_index()

    df = df.rename(columns={
        "tabla_ingresos_con_iva": "Ingresos",
        "tabla_comisiones_con_iva": "Comisiones",
        "coste_suelo": "Coste suelo",
        "costes_mensuales_ejecucion_iva": "Coste ejecución",
        "costes_indirectos_con_iva": "Costes indirectos",
        "costes_financieros": "Coste financiero"
    })

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Ingresos netos"] = df["Ingresos"] + df["Comisiones"]
    df["Costes totales"] = df[["Comisiones", "Coste suelo", "Coste ejecución", "Costes indirectos", "Coste financiero"]].sum(axis=1)
    df["Flujo mensual"] = df["Ingresos netos"] + df["Costes totales"]
    df["Flujo acumulado"] = df["Flujo mensual"].cumsum()

    fila_total = pd.DataFrame({col: [df[col].sum()] for col in df.columns if col != "Flujo acumulado"}, index=["Total"])
    fila_total["Flujo acumulado"] = df["Flujo acumulado"].iloc[-1]
    df_final = pd.concat([df, fila_total])

    datos["flujo_caja"] = df_final.reset_index().rename(columns={"index": "Mes"}).to_dict(orient="records")

    with st.expander("📊 Flujo de Caja General", expanded=False):
        df_mostrar = df_final.copy()
        df_mostrar.index = [i.strftime("%Y-%m") if isinstance(i, pd.Timestamp) else str(i) for i in df_mostrar.index]
        st.dataframe(df_mostrar, use_container_width=True)

    with st.expander("🏦 Movimientos de la cuenta especial intervenida", expanded=False):
        df_ingresos = pd.DataFrame(datos["tabla_ingresos_con_iva"])
        df_ingresos = df_ingresos[df_ingresos["Mes"] != "Total"]
        df_ingresos["Mes"] = pd.to_datetime(df_ingresos["Mes"])
        ingresos_col = [c for c in ["Reserva", "Contrato", "Aplazado"] if c in df_ingresos.columns]
        for col in ingresos_col:
            df_ingresos[col] = pd.to_numeric(df_ingresos[col], errors="coerce").fillna(0)
        df_ingresos["Ingresos cuenta especial"] = df_ingresos[ingresos_col].sum(axis=1)
        df_ingresos = df_ingresos.set_index("Mes")[["Ingresos cuenta especial"]]

        df_coste_ejec = pd.DataFrame(datos["costes_mensuales_ejecucion_iva"])
        df_coste_ejec = df_coste_ejec[df_coste_ejec["Mes"] != "Total"]
        df_coste_ejec["Mes"] = pd.to_datetime(df_coste_ejec["Mes"])
        df_coste_ejec = df_coste_ejec.dropna(subset=["Mes"]).set_index("Mes")
        df_coste_ejec = df_coste_ejec[["Total"]].rename(columns={"Total": "Coste ejecución"})

        df_cuenta = df_ingresos.join(df_coste_ejec, how="outer").fillna(0).sort_index()
        for col in df_cuenta.columns:
            df_cuenta[col] = pd.to_numeric(df_cuenta[col], errors="coerce").fillna(0)
        df_cuenta["Flujo mensual"] = df_cuenta["Ingresos cuenta especial"] + df_cuenta["Coste ejecución"]

        saldo = 0
        saldos, deficits = [], []
        for _, row in df_cuenta.iterrows():
            saldo += row["Flujo mensual"]
            if saldo < 0:
                deficits.append(saldo)  # El déficit se guarda como negativo
                saldo = 0
            else:
                deficits.append(0)
            saldos.append(saldo)

        df_cuenta["Saldo acumulado"] = saldos
        df_cuenta["Déficit cuenta especial"] = deficits

        columnas = ["Ingresos cuenta especial", "Coste ejecución", "Flujo mensual", "Saldo acumulado", "Déficit cuenta especial"]
        df_cuenta = df_cuenta[columnas]
        fila_total = pd.DataFrame({col: [df_cuenta[col].sum()] for col in columnas if col != "Saldo acumulado"}, index=["Total"])
        fila_total["Saldo acumulado"] = df_cuenta["Saldo acumulado"].iloc[-1]
        df_cuenta_final = pd.concat([df_cuenta, fila_total])

        datos["movimientos_cuenta_especial"] = df_cuenta_final.reset_index().rename(columns={"index": "Mes"}).to_dict(orient="records")

        df_mostrar_cuenta = df_cuenta_final.copy()
        df_mostrar_cuenta.index = [i.strftime("%Y-%m") if isinstance(i, pd.Timestamp) else str(i) for i in df_mostrar_cuenta.index]
        st.dataframe(df_mostrar_cuenta, use_container_width=True)

    with st.expander("💰 Necesidades de financiación de la promoción", expanded=False):
        try:
            df_comisiones = pd.DataFrame(datos["tabla_comisiones_con_iva"])
            df_comisiones = df_comisiones[df_comisiones["Mes"] != "Total"]
            df_comisiones["Mes"] = pd.to_datetime(df_comisiones["Mes"])
            fases_pre_esc = [f for f in ["Reserva", "Contrato", "Aplazado"] if f in df_comisiones.columns]
            for col in fases_pre_esc:
                df_comisiones[col] = pd.to_numeric(df_comisiones[col], errors="coerce").fillna(0)
            df_comisiones["Comisiones pre-escritura"] = df_comisiones[fases_pre_esc].sum(axis=1)
            df_comisiones = df_comisiones.set_index("Mes")[["Comisiones pre-escritura"]]

            def cargar(tabla, columna):
                df = pd.DataFrame(datos[tabla])
                df = df[df["Mes"] != "Total"]
                df["Mes"] = pd.to_datetime(df["Mes"])
                df = df.dropna(subset=["Mes"]).set_index("Mes")
                df[columna] = pd.to_numeric(df[columna], errors="coerce").fillna(0)
                return df[[columna]].rename(columns={columna: tabla})

            df_indirectos = cargar("costes_indirectos_con_iva", "Total").rename(columns={"costes_indirectos_con_iva": "Costes indirectos"})
            df_financieros = cargar("costes_financieros", "Coste financiero").rename(columns={"costes_financieros": "Costes financieros"})

            df_deficit = pd.DataFrame(datos.get("movimientos_cuenta_especial", []))
            df_deficit = df_deficit[df_deficit["Mes"] != "Total"]
            df_deficit["Mes"] = pd.to_datetime(df_deficit["Mes"], errors="coerce")
            df_deficit = df_deficit.dropna(subset=["Mes"]).set_index("Mes")
            df_deficit = df_deficit[["Déficit cuenta especial"]]
            df_deficit["Déficit cuenta especial"] = pd.to_numeric(df_deficit["Déficit cuenta especial"], errors="coerce").fillna(0)

            # Añadir Coste del Suelo como nueva serie
            df_suelo = pd.DataFrame()

            if "flujo_caja" in datos:
                df_flujo = pd.DataFrame(datos["flujo_caja"])
                df_flujo = df_flujo[df_flujo["Mes"] != "Total"]
                df_flujo["Mes"] = pd.to_datetime(df_flujo["Mes"])
                df_flujo = df_flujo.set_index("Mes")
                df_flujo["Coste suelo"] = pd.to_numeric(df_flujo["Coste suelo"], errors="coerce").fillna(0)

                df_suelo = pd.DataFrame(index=pd.to_datetime(df_flujo.index.unique()), columns=["Coste suelo"])
                df_suelo["Coste suelo"] = df_flujo["Coste suelo"]
                df_suelo["Coste suelo"] = pd.to_numeric(df_suelo["Coste suelo"], errors="coerce").fillna(0)

            # Añadir el suelo a los demás costes
            df_suelo["Coste suelo"] = df_suelo["Coste suelo"].fillna(0)

            df_necesidades = df_comisiones.join([df_suelo, df_indirectos, df_financieros, df_deficit], how="outer").fillna(0)
            df_necesidades["Total necesidades"] = df_necesidades.sum(axis=1)
            df_necesidades["Acumulado"] = df_necesidades["Total necesidades"].cumsum()

            fila_total = pd.DataFrame(df_necesidades.sum(numeric_only=True)).T
            fila_total.index = ["Total"]
            fila_total["Acumulado"] = df_necesidades["Acumulado"].iloc[-1]
            df_necesidades_final = pd.concat([df_necesidades, fila_total])

            df_necesidades_final.index = [i.strftime("%Y-%m") if isinstance(i, pd.Timestamp) else str(i) for i in df_necesidades_final.index]

            st.dataframe(df_necesidades_final, use_container_width=True)

            datos["tabla_necesidades_financiacion"] = df_necesidades_final.reset_index().rename(columns={"index": "Mes"}).to_dict(orient="records")
        except Exception as e:
            st.error(f"❌ Error al generar la tabla de necesidades de financiación: {e}")
            
    with st.expander("📊 Resumen acumulado de la promoción", expanded=False):
        try:
            # Cargar todas las tablas necesarias
            df_ingresos = pd.DataFrame(datos["tabla_ingresos_con_iva"])
            df_flujo = pd.DataFrame(datos["flujo_caja"])
            df_necesidades = pd.DataFrame(datos["tabla_necesidades_financiacion"])
            df_cuenta = pd.DataFrame(datos["movimientos_cuenta_especial"])

            # Filtrar filas válidas y eliminar duplicados
            for df in [df_ingresos, df_flujo, df_necesidades, df_cuenta]:
                df.drop(df[df["Mes"] == "Total"].index, inplace=True)
                df["Mes"] = pd.to_datetime(df["Mes"])
                df.set_index("Mes", inplace=True)

            # Eliminar duplicados en los índices
            df_ingresos = df_ingresos[~df_ingresos.index.duplicated(keep="first")]
            df_flujo = df_flujo[~df_flujo.index.duplicated(keep="first")]
            df_necesidades = df_necesidades[~df_necesidades.index.duplicated(keep="first")]
            df_cuenta = df_cuenta[~df_cuenta.index.duplicated(keep="first")]

            # Crear índice completo con todos los meses presentes
            meses_completos = df_ingresos.index.union(df_flujo.index).union(df_necesidades.index).union(df_cuenta.index).sort_values()

            # Reindexar todos los dataframes al índice completo
            df_ingresos = df_ingresos.reindex(meses_completos).fillna(0)
            df_flujo = df_flujo.reindex(meses_completos).fillna(0)
            df_necesidades = df_necesidades.reindex(meses_completos).fillna(0)
            df_cuenta = df_cuenta.reindex(meses_completos).fillna(0)

            # Construcción del resumen
            df_resumen = pd.DataFrame(index=meses_completos)
            fases = [f for f in ["Reserva", "Contrato", "Aplazado", "Escritura"] if f in df_ingresos.columns]
            df_resumen["Ingresos acumulados"] = df_ingresos[fases].sum(axis=1).cumsum()
            df_resumen["Flujo total acumulado"] = df_flujo["Flujo acumulado"]
            df_resumen["Déficit cuenta especial acumulado"] = df_cuenta["Déficit cuenta especial"].cumsum()
            df_resumen["Necesidades financiación acumuladas"] = df_necesidades["Total necesidades"].cumsum()

            # Convertir fechas a string para mostrar
            df_resumen.reset_index(inplace=True)
            df_resumen["Mes"] = df_resumen["Mes"].dt.strftime("%Y-%m")
            st.dataframe(df_resumen, use_container_width=True)

            datos["tabla_resumen_acumulado"] = df_resumen.to_dict(orient="records")
        
        except Exception as e:
            st.error(f"Error al generar el resumen acumulado: {str(e)}")