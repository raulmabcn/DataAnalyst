<div align="center">

# 🧱 Foundations · Fundamentos de Data Analytics

![Excel](https://img.shields.io/badge/Excel-Data%20Preparation-217346?logo=microsoftexcel&logoColor=white)
![Power Query](https://img.shields.io/badge/Power%20Query-ETL-217346)
![MySQL](https://img.shields.io/badge/MySQL-SQL-4479A1?logo=mysql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Visualization-F2C811?logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)

**De la hoja de cálculo al primer flujo completo de análisis de datos**

</div>

> Fase desarrollada íntegramente de forma individual por **Raúl Martínez Aparicio**.

---

## De un vistazo

| Preparación de datos | Consulta | Análisis | Comunicación |
|:---:|:---:|:---:|:---:|
| Excel · Power Query · Power Pivot | MySQL | Python · pandas | Power BI |

```mermaid
flowchart LR
    A["Excel<br/>limpieza y modelado"] --> B["SQL<br/>consulta relacional"]
    B --> C["Python<br/>automatización y análisis"]
    C --> D["Power BI<br/>visualización"]

    style A fill:#217346,color:#fff,stroke:#fff
    style B fill:#4479A1,color:#fff,stroke:#fff
    style C fill:#3776AB,color:#fff,stroke:#fff
    style D fill:#F2C811,color:#111,stroke:#fff
```

Esta primera fase construye una base transversal: importar y transformar datos, comprender un modelo relacional, consultar información con SQL, automatizar cálculos con Python y convertir los resultados en visualizaciones comprensibles.

---

## 🗂�?Estructura

<details>
<summary><b>Ver árbol de carpetas</b> (clic para desplegar)</summary>

```text
Foundations/
�?├── ApuntsCibernarium/              Material docente y documentación de consulta
�?├── MySql/
�?  ├── Exercices/                  Consultas, joins, subconsultas y examen
�?  ├── Samples/                    Bases de datos y conjuntos de práctica
�?  └── CheatSheets/                Referencias rápidas de SQL
�?├── PowerBi/
�?  ├── Exercices/                  Informes y dashboards desarrollados
�?  └── Samples/                    Ficheros de apoyo para visualización
�?├── Python/
�?  ├── Exercices/                  Notebooks, prácticas y evaluación
�?  ├── Samples/                    CSV y documentación de apoyo
�?  └── CheatSheet/                 Referencias de Python, pandas y Jupyter
�?└── README.md
```

</details>

Los contenidos de `ApuntsCibernarium`, `Samples`, `CheatSheets` y `CheatSheet` se conservan como material formativo o de consulta. Las soluciones y entregables personales se encuentran principalmente en las carpetas `Exercices`.

---

## 🧩 Bloques de aprendizaje

### Excel, Power Query y Power Pivot

- Preparación, limpieza y transformación de tablas.
- Uso de formatos condicionales y criterios de presentación.
- Introducción a flujos ETL con Power Query.
- Modelado y relaciones mediante Power Pivot.
- Elección del gráfico adecuado según el tipo de dato y la pregunta.

### MySQL

- Creación y exploración de bases de datos.
- Consultas `SELECT`, filtros, agregaciones y funciones SQL.
- Combinación de tablas mediante `JOIN`.
- Resolución de problemas con subconsultas.
- Prácticas sobre bases de datos de hospitales, bibliotecas, Juegos Olímpicos y Sakila.

### Python y pandas

- Variables, estructuras de control, colecciones y funciones.
- Lectura, filtrado, agrupación y transformación de ficheros CSV.
- Creación de métricas derivadas y tablas resumen.
- Cruce de información de hospitales, pacientes y especialidades.
- Detección de valores atípicos, rankings y análisis de correlación.

Entre los ejercicios aplicados se incluyen el análisis de cursos de Udemy, libros superventas y datos hospitalarios, además de funciones para estimar ocupación, satisfacción, carga de trabajo médico y eficiencia.

### Power BI

- Importación y transformación de fuentes.
- Construcción del modelo de datos.
- Creación de medidas e indicadores.
- Diseño de informes interactivos orientados a la lectura de negocio.

---

## 🛠�?Stack técnico

- **Hojas de cálculo y ETL:** Excel, Power Query y Power Pivot.
- **Base de datos:** MySQL y MySQL Workbench.
- **Programación:** Python.
- **Análisis:** pandas.
- **Entorno reproducible:** Jupyter Notebook y Google Colab.
- **Business intelligence:** Power BI.
- **Control de versiones:** Git y GitHub.

## 🧭 Cómo navegar esta fase

- **Para revisar SQL �?* comienza por `MySql/Exercices/` y continúa con los casos de `JOIN` y subconsultas.
- **Para revisar Python �?* abre los notebooks de `Python/Exercices/`; las tareas avanzan desde sintaxis básica hasta análisis con varias tablas.
- **Para revisar visualización �?* abre los `.pbix` de `PowerBi/Exercices/`.
- **Para consultar teoría �?* utiliza `ApuntsCibernarium/` y las carpetas de referencias rápidas.

---

<div align="center">

## Autoría

Proyecto formativo y ejercicios desarrollados por  
**Raúl Martínez Aparicio**

</div>
