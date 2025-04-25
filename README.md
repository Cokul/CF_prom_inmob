# pres_prom_inmob_v2
# Aplicación de Flujos de Caja para Promociones Inmobiliarias

Esta aplicación está diseñada para gestionar y calcular los flujos de caja de una promoción inmobiliaria. Permite cargar y gestionar proyectos, crear versiones, importar datos desde archivos Excel, calcular los costes de ejecución, y generar informes detallados. Todo esto con una interfaz amigable utilizando **Streamlit**.

## Características

- **Gestión de proyectos y versiones**: Permite crear, duplicar y eliminar proyectos y versiones.
- **Carga de datos desde Excel**: Permite cargar datos de los capítulos de ejecución desde un archivo Excel (CSV también soportado).
- **Cálculo de costes de ejecución**: Basado en una serie de capítulos de obra con coste, fechas de inicio y duración. 
- **Generación de informes**: Calcula y presenta el flujo de caja mensual, los costes mensuales, y los costes totales. Incluye un resumen y la planificación de cada capítulo.
- **Soporte para IVA**: Cálculo de costes con y sin IVA, con soporte configurable para el tipo de IVA de la ejecución.
- **Interfaz interactiva**: Interfaz web construida con Streamlit que permite la entrada de datos y la visualización de resultados en tiempo real.
- **Estilo visual personalizado**: Diseño optimizado para mejorar la usabilidad y la presentación de la información.

## Requisitos

- Python 3.8+
- Streamlit
- pandas==1.4.0
- numpy==1.26.3
- numpy-financial==1.0.0
- plotly==6.0.1
- python_dateutil==2.9.0.post0
- streamlit==1.44.1
- openpyxl==3.1.2.

Puedes instalar todas las dependencias utilizando el siguiente comando:
    pip install -r requirements.txt

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/tu-usuario/presupuestos-promociones.git
    cd presupuestos-promociones
    ```

2. Crea un entorno virtual:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Corre la aplicación:

    ```bash
    streamlit run streamlit_app.py
    ```

## Uso

1. **Gestión de Proyectos y Versiones**: 
    - Crea un nuevo proyecto e introduce los datos básicos como la fecha de inicio, coste por m², y superficie total construida.
    - Puedes guardar y cargar versiones del proyecto para mantener el historial.

2. **Cargar Archivos Excel**:
    - Puedes cargar un archivo de Excel con la planificación de capítulos de obra. Asegúrate de que el archivo tenga las columnas: `Capítulo`, `Coste`, `Fecha inicio`, y `Duración (meses)`.

3. **Cálculo de Costes**:
    - Al cargar el archivo o introducir los datos manualmente, la aplicación calculará el coste total de ejecución, los costes mensuales y la planificación por capítulo.
    - Los costes se calculan con y sin IVA, dependiendo de la configuración.

4. **Generación de Informes**:
    - Una vez que todos los datos estén cargados, puedes visualizar los resultados en tablas detalladas.
    - Los informes muestran la planificación de capítulos, los costes mensuales con y sin IVA, y el coste total de ejecución.

5. **Pantalla de Inicio**: 
    - La aplicación comienza con una pantalla de bienvenida que ofrece una visión general de los proyectos y versiones disponibles.

## Personalización

Puedes ajustar varios parámetros, como los valores predeterminados de costes, el tipo de IVA, y otros detalles, directamente en el código. Si necesitas realizar cambios o personalizaciones, consulta los archivos en la carpeta `inputs` y `outputs`.

## Contribuciones

Si deseas contribuir a este proyecto, por favor, abre un *issue* o un *pull request*.

## Licencia

Este proyecto está licenciado bajo la MIT License - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para más información o soporte, puedes contactarme a través de [tu correo o canal de contacto].
