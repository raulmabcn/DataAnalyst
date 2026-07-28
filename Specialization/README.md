<div align="center">

# 🚀 Specialization · Data Analytics

![MySQL](https://img.shields.io/badge/MySQL-Relational%20Data-4479A1?logo=mysql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL-47A248?logo=mongodb&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![REST API](https://img.shields.io/badge/REST-APIs-6E40C9)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboards-F2C811?logo=powerbi&logoColor=black)

**De la consulta de datos al desarrollo de soluciones analíticas integradas**

</div>

> Fase desarrollada íntegramente de forma individual por **Raúl Martínez Aparicio**.

---

## De un vistazo

| Modelado relacional | Datos NoSQL | Programación y análisis | Integración y visualización |
|:---:|:---:|:---:|:---:|
| MySQL · esquema en estrella | MongoDB · agregaciones | Python · pandas | APIs REST · Power BI |

```mermaid
flowchart LR
    S1["SQL<br/>consulta y manipulación"] --> S2["Modelado<br/>esquema en estrella"]
    S2 --> S3["MongoDB<br/>consulta documental"]
    S3 --> S4["Python + pandas<br/>análisis"]
    S4 --> S5["APIs + Power BI<br/>integración y comunicación"]

    style S1 fill:#4479A1,color:#fff,stroke:#fff
    style S2 fill:#355C7D,color:#fff,stroke:#fff
    style S3 fill:#47A248,color:#fff,stroke:#fff
    style S4 fill:#3776AB,color:#fff,stroke:#fff
    style S5 fill:#F2C811,color:#111,stroke:#fff
```

La especialización amplía los fundamentos mediante casos progresivos: una base transaccional de ventas sirve para practicar SQL, integridad referencial y modelado dimensional; después se incorporan MongoDB, análisis con Python, visualización y consumo de datos externos mediante APIs.

---

## 🗂�?Estructura

<details>
<summary><b>Ver árbol de carpetas</b> (clic para desplegar)</summary>

```text
Specialization/
�?├── BasicNotionsSQL/                Consultas, joins y subconsultas
├── TableManiputaltionSQL/          DDL, DML, integridad y vistas
├── DatabaseCreationSQL/            Esquema en estrella y carga por SQL
├── MongodbQueries/                 Consultas, agregaciones y geodatos
�?├── PythonBasics/                   Funciones, validación y automatización
├── PythonPandas/                   Transformación y análisis tabular
├── PythonVisualData/               Visualización e interpretación
├── PythonAPIsREST/                 Consumo de APIs y exportación
�?├── PowerBiDataAnalysisIntro/       Introducción al análisis en Power BI
├── PowerBiAnailisVendas/           Análisis de ventas en Power BI
├── Bridge/                         Ejercicios de transición
├── ToolBox/                        Utilidades y referencias SQL
└── README.md
```

</details>

---

## 🧱 Sprints SQL · Del dato transaccional al modelo analítico

**Caso de trabajo:** transacciones comerciales relacionadas con compañías, usuarios, tarjetas de crédito y productos.

### Nociones básicas

- Exploración de tablas de hechos y dimensiones.
- Consultas con filtros, agregaciones, `JOIN` y subconsultas.
- Análisis de ventas por empresa, país y fecha.
- Clasificación de compañías según su volumen de transacciones.

### Manipulación de tablas

- Creación y modificación de tablas con restricciones.
- Gestión de claves primarias y foráneas.
- Altas, actualizaciones y eliminaciones de registros.
- Creación de la vista `VistaMarketing` con información de compañías y compra media.
- Uso de transacciones y recuperación de cambios.

### Creación de base de datos

- Diseño de un **esquema en estrella** con `transaction` como tabla de hechos.
- Integración de dimensiones de usuario, compañía, tarjeta y producto.
- Carga y transformación realizadas mediante código SQL.
- Cálculo del estado de las tarjetas según sus últimas transacciones.
- Resolución de la relación entre transacciones y múltiples productos.

---

## 🍃 MongoDB · Consulta documental y geoespacial

- Exploración de colecciones de películas, comentarios, usuarios y cines.
- Filtros por fecha, género, idioma, premios y puntuación IMDb.
- Agregaciones para contar comentarios por dominio y cines por código postal.
- Preparación de coordenadas anidadas para su consumo desde Power BI.
- Representación de la ubicación de cines mediante MongoDB Atlas Charts y Power BI.

---

## 🐍 Python · Programación, análisis y visualización

### Fundamentos y automatización

- Validación de entradas y tratamiento de errores.
- Funciones para IMC, conversión de temperaturas y procesamiento de texto.
- Manipulación de diccionarios, colecciones y ficheros.
- Generación configurable de contraseñas.
- Procesamiento de resultados deportivos y cálculo de clasificaciones.

### pandas

- Limpieza, tipado, transformación y enriquecimiento de DataFrames.
- Tablas resumen, tablas dinámicas y métricas salariales.
- Unión de datos, tratamiento de fechas y exportación automatizada.
- Generación de gráficos según el tipo de variable.
- Aproximación heurística a una ruta entre ciudades a partir de una matriz de distancias.

### Visualización

- Selección de gráficos para variables numéricas y categóricas.
- Uso de histogramas, diagramas de dispersión, mapas de calor, `pairplot` y `jointplot`.
- Estudio de distribuciones, valores atípicos y correlaciones.
- Comparación del comportamiento de compra entre regiones y países.
- Implementación de versiones equivalentes en Python y Power BI.

---

## 🌐 APIs REST

- Peticiones `GET`, `POST`, `PATCH` y `DELETE` con `requests`.
- Comprobación de códigos de estado y manejo de respuestas JSON.
- Conversión de respuestas a DataFrames de pandas.
- Exploración de JSONPlaceholder y de una API pública seleccionada.
- Consulta del catálogo Open Data BCN y exportación de recursos a CSV.

## 🛠�?Stack técnico

- **Bases de datos:** MySQL, MySQL Workbench y MongoDB.
- **Programación:** Python.
- **Análisis:** pandas y NumPy.
- **Visualización:** Matplotlib, Seaborn, MongoDB Atlas Charts y Power BI.
- **Integración:** REST APIs, JSON y CSV.
- **Entorno:** Jupyter Notebook y Google Colab.
- **Control de versiones:** Git y GitHub.

## 🧭 Cómo navegar esta fase

- **Ruta SQL �?* `BasicNotionsSQL �?TableManiputaltionSQL �?DatabaseCreationSQL`.
- **Ruta NoSQL �?* abre `MongodbQueries/MongodbQueries.pdf` junto con el script `.js`.
- **Ruta Python �?* `PythonBasics �?PythonPandas �?PythonVisualData �?PythonAPIsREST`.
- **Vista de negocio �?* abre los informes `.pbix` de las carpetas Power BI.
- Los `.pdf` documentan los enunciados, la ejecución y los resultados; los `.sql`, `.js` e `.ipynb` contienen la implementación.

---

<div align="center">

## Autoría

Proyecto formativo y entregables desarrollados por  
**Raúl Martínez Aparicio**

</div>
