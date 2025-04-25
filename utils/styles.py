import streamlit as st

# Estilos personalizados para la aplicación
def aplicar_estilos():
    st.markdown("""
        <style>
            /* Estilo general */
            body {
                font-family: 'Arial', sans-serif;
                font-size: 14px;
                color: #333;
                background-color: #F8F8F8;  /* Fondo más claro */
            }

            /* Estilo para los encabezados */
            h1, h2, h3 {
                font-family: 'Arial', sans-serif;
                font-weight: bold;
                color: #1D3557;
            }

            h1 {
                font-size: 32px;
                margin-bottom: 10px;  /* Más espacio entre el título y el contenido */
            }

            h2 {
                font-size: 28px;
                margin-bottom: 8px;
            }

            h3 {
                font-size: 24px;
                margin-bottom: 6px;
            }

            /* Estilo para el texto de sección */
            .section-header {
                font-size: 18px;
                font-weight: bold;
                color: #1D3557;
                padding-top: 10px;
                margin-bottom: 10px;
            }

            /* Estilo para los botones personalizados */
            .stButton button {
                background-color: #1D3557;
                color: white;
                font-weight: bold;
                border-radius: 5px; /* Bordes redondeados */
                padding: 10px 20px;
            }

            .stButton button:hover {
                background-color: #457B9D;
                cursor: pointer;
            }

            /* Estilo para los elementos expandidos (st.expander) */
            .stExpander {
                background-color: #f1f1f1;
                border-radius: 8px;
                padding: 15px;
                margin-top: 15px;
                border: 1px solid #ddd;
            }

            /* Estilo para las tooltips */
            .stTooltip {
                background-color: #333;
                color: white;
                font-size: 12px;
                padding: 5px;
            }

            /* Títulos en la barra lateral */
            .sidebar .sidebar-content h1 {
                color: #1D3557;
            }

            /* Estilo para las pestañas */
            .stTab {
                font-size: 14px;
                font-weight: bold;
                background-color: #F1FAEE;
                color: #1D3557;
                padding: 10px;
                border-radius: 5px;
                margin-right: 10px;
            }

            .stTab:hover {
                background-color: #E4F1F5;
                cursor: pointer;
            }

            /* Resaltado de inputs y botones */
            .stTextInput, .stNumberInput, .stSelectbox, .stMultiselect, .stDateInput {
                border: 2px solid #1D3557;
                border-radius: 4px;
                padding: 8px;
                margin-top: 5px;
            }

            .stTextInput:focus, .stNumberInput:focus, .stSelectbox:focus, .stMultiselect:focus, .stDateInput:focus {
                border-color: #457B9D;
            }

            /* Estilo para los contenedores de los inputs */
            .stTextInput, .stNumberInput, .stSelectbox, .stMultiselect, .stDateInput {
                margin-bottom: 15px;  /* Más espacio entre los inputs */
            }

            /* Modificar la barra lateral */
            .sidebar {
                background-color: #F1FAEE;
                padding: 15px;
            }

            /* Mejorar los iconos */
            .stSidebarHeader {
                font-size: 18px;
                font-weight: bold;
                color: #1D3557;
            }

            /* Botones en la barra lateral */
            .stSidebar .stButton button {
                background-color: #457B9D;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 10px 15px;
                width: 100%;
                margin-bottom: 10px;
            }

            .stSidebar .stButton button:hover {
                background-color: #1D3557;
                cursor: pointer;
            }

            /* Estilos generales para la barra lateral */
            .stSidebar .stSelectbox, .stSidebar .stTextInput {
                margin-top: 5px;
                margin-bottom: 15px;
                width: 100%;
            }

            /* Modificar el estilo de las tablas */
            .stDataFrame table {
                border-collapse: collapse;
                width: 100%;
            }

            .stDataFrame table, .stDataFrame th, .stDataFrame td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }

            .stDataFrame th {
                background-color: #F1FAEE;
                font-weight: bold;
            }

            /* Botones flotantes */
            .stButton.button-small {
                background-color: #E4F1F5;
                font-size: 12px;
                color: #1D3557;
            }
        </style>
    """, unsafe_allow_html=True)