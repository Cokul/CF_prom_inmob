import pandas as pd
from dateutil.relativedelta import relativedelta
import streamlit as st


def generar_tablas_ingresos(datos):
    df_viv = pd.DataFrame(datos.get("viviendas", []))
    if df_viv.empty:
        st.warning("No hay datos de viviendas cargados.")
        return

    for col in ["Fecha venta", "Fecha escritura"]:
        if col in df_viv.columns:
            df_viv[col] = pd.to_datetime(df_viv[col], errors="coerce")

    fecha_ini_com = pd.to_datetime(datos.get("fecha_inicio_comercializacion"))
    fecha_fin_obra = pd.to_datetime(datos.get("fecha_fin_obra"))

    if pd.isna(fecha_ini_com) or pd.isna(fecha_fin_obra):
        st.warning("⚠️ Faltan fechas clave (inicio comercialización o fin de obra).")
        return

    iva = datos.get("iva_viviendas", 10.0) / 100
    pct_contrato = datos.get("fase_contrato_pct", 25.0) / 100
    pct_aplazado = datos.get("fase_aplazado_pct", 25.0) / 100
    reserva_con_iva = datos.get("fase_reserva", 10000.0)
    reserva_sin_iva_unit = reserva_con_iva / (1 + iva)

    pct_comision = datos.get("pct_comercializacion", 15.0) / 100
    iva_otros = datos.get("iva_otros", 21.0) / 100

    df_resultados = []
    unidades = []

    for i, row in df_viv.iterrows():
        precio = row.get("Precio venta", 0)
        f_reserva = row.get("Fecha venta")
        f_escritura = row.get("Fecha escritura")

        if pd.isna(f_reserva):
            f_escritura_tmp = f_escritura if not pd.isna(f_escritura) else fecha_fin_obra + relativedelta(months=3)
            f_limite = f_escritura_tmp - relativedelta(months=4)
            fechas_posibles = pd.date_range(start=fecha_ini_com, end=f_limite, freq="MS")
            f_reserva = fechas_posibles[min(i, len(fechas_posibles) - 1)]

        f_contrato = f_reserva + relativedelta(months=1)
        f_aplazado = f_contrato + relativedelta(months=3)

        if pd.isna(f_escritura):
            f_escritura_real = max(fecha_fin_obra + relativedelta(months=3), f_aplazado + relativedelta(months=1))
        else:
            f_escritura_real = max(pd.to_datetime(f_escritura), fecha_fin_obra + relativedelta(months=3), f_aplazado + relativedelta(months=1))

        if f_reserva > fecha_fin_obra:
            imp_res = reserva_sin_iva_unit
            imp_esc = precio - imp_res
            fases = {
                "Reserva": (f_reserva, imp_res, imp_res * (1 + iva)),
                "Escritura": (f_escritura_real, imp_esc, imp_esc * (1 + iva))
            }
        else:
            imp_res = reserva_sin_iva_unit
            imp_cont = round(precio * pct_contrato, 2)
            imp_aplz = round(precio * pct_aplazado, 2)
            imp_esc = round(precio - imp_res - imp_cont - imp_aplz, 2)
            fases = {
                "Reserva": (f_reserva, imp_res, imp_res * (1 + iva)),
                "Contrato": (f_contrato, imp_cont, imp_cont * (1 + iva)),
                "Aplazado": (f_aplazado, imp_aplz, imp_aplz * (1 + iva)),
                "Escritura": (f_escritura_real, imp_esc, imp_esc * (1 + iva))
            }

        for fase, (fecha, sin_iva, con_iva) in fases.items():
            mes = fecha.strftime("%Y-%m")
            df_resultados.append({
                "Mes": mes,
                "Fase": fase,
                "Importe sin IVA": round(sin_iva, 2),
                "Importe con IVA": round(con_iva, 2),
                "Comisión sin IVA": -round(sin_iva * pct_comision, 2),
                "Comisión con IVA": -round(sin_iva * pct_comision * (1 + iva_otros), 2)
            })

        unidades.append(f_reserva.strftime("%Y-%m"))

    df = pd.DataFrame(df_resultados)

    def tabla(df, valor):
        tabla = df.pivot_table(index="Mes", columns="Fase", values=valor, aggfunc="sum", fill_value=0)
        orden = ["Reserva", "Contrato", "Aplazado", "Escritura"]
        tabla = tabla.reindex(columns=[col for col in orden if col in tabla.columns])
        tabla["Total"] = tabla.sum(axis=1)
        total_row = pd.DataFrame(tabla.sum()).T
        total_row.index = ["Total"]
        tabla = pd.concat([tabla, total_row])
        tabla = tabla.reset_index().rename(columns={"index": "Mes"})  # Asegurar que la columna se llame 'Mes'
        return tabla

    df_unidades = pd.Series(unidades).value_counts().sort_index().rename_axis("Mes").reset_index(name="Unidades")
    total_uni = pd.DataFrame([{"Mes": "Total", "Unidades": df_unidades["Unidades"].sum()}])
    df_unidades = pd.concat([df_unidades, total_uni], ignore_index=True)

    tabla_sin_iva = tabla(df, "Importe sin IVA")
    tabla_con_iva = tabla(df, "Importe con IVA")
    tabla_comision_sin_iva = tabla(df, "Comisión sin IVA")
    tabla_comision_con_iva = tabla(df, "Comisión con IVA")

    st.markdown("## 🧾 Outputs de Ingresos")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Unidades vendidas",
        "💶 Ingresos sin IVA",
        "💶 Ingresos con IVA",
        "💸 Comisiones sin IVA",
        "💸 Comisiones con IVA"
    ])

    with tab1:
        st.dataframe(df_unidades, use_container_width=True)

    with tab2:
        st.dataframe(tabla_sin_iva, use_container_width=True)

    with tab3:
        st.dataframe(tabla_con_iva, use_container_width=True)

    with tab4:
        st.dataframe(tabla_comision_sin_iva, use_container_width=True)

    with tab5:
        st.dataframe(tabla_comision_con_iva, use_container_width=True)

    datos["tabla_unidades_vendidas"] = df_unidades.to_dict(orient="records")
    datos["tabla_ingresos_sin_iva"] = tabla_sin_iva.to_dict(orient="records")
    datos["tabla_ingresos_con_iva"] = tabla_con_iva.to_dict(orient="records")
    datos["tabla_comisiones_sin_iva"] = tabla_comision_sin_iva.to_dict(orient="records")
    datos["tabla_comisiones_con_iva"] = tabla_comision_con_iva.to_dict(orient="records")