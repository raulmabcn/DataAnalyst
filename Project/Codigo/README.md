# EUT Catalunya 2003, 2011 y 2024 - Version 2.0

Proyecto reproducible para armonizar y analizar las Encuestas de Empleo del
Tiempo de 2003, 2011 y 2024.

## Orden de ejecucion

1. `Notebooks/00_load_raw.ipynb`: transforma los microdatos originales en tres
   ficheros armonizados anuales.
2. `Notebooks/01_load_clean.ipynb`: valida, concatena y prepara el conjunto de
   analisis de los tres años.
3. `Notebooks/02_statistical_analysis.ipynb`: estudia relaciones y cambios con
   doce figuras numeradas.

## Estructura

- `RawDataSets`: microdatos y documentacion originales, separados por ano.
- `CleanDataSets`: datos armonizados anuales, conjunto preparado y
  diccionario de variables.
- `PythonCommon`: funciones compartidas de carga, validacion y estadistica.
- `PythonGraphs`: módulos de cálculo y representación sin carga de datos ni escritura automática.

Todos los componentes usan rutas relativas a la raiz.


## Arquitectura Python

Los notebooks cargan los datos una sola vez. PythonCommon/eut_statistics.py centraliza los cálculos ponderados y PythonCommon/graph_style.py los órdenes visuales. Los módulos de PythonGraphs sólo reciben tablas o datos y devuelven tablas o figuras; importarlos no genera archivos ni ejecuta análisis.

