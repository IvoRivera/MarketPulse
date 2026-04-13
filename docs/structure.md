# 📁 MarketPulse – Estructura del Proyecto

## 🧱 Estructura General

```
marketpulse/
│
├── data/
│ ├── processed/
│ │ ├── clean_market_data.csv
│ │ ├── final_dataset.csv
│ │ └── sql_outputs/
│ │   ├── sales_by_day.csv
│ │   ├── top_products.csv
│ │   ├── rolling_avg.csv
│ │   └── product_ranking.csv
│ ├── raw/
│ │ ├── raw_market_data.csv
│ │ └── weather_data.csv
│
├── src/
│ ├── ingestion/
│ │ ├── data_generator.py
│ │ └── weather_api.py
│ │
│ ├── processing/
│ │ ├── data_cleaning.py
│ │ └── feature_engineering.py
│ │
| ├── analysis/
│ │   ├── eda.py
│ │   ├── run_sql.py
│ │   └── validate_sql_vs_python.py
│ │
│ ├── sql/
│ │ ├── sales_by_day.sql
│ │ ├── top_products.sql
│ │ ├── rolling_avg.sql
│ │ └── product_ranking.sql
│
├── tests/
│ └── test_data_quality.py
│
├── notebooks/
├── dashboards/
│ └── marketpulse.pbix
│
├── docs/
│ ├── charter.md
│ └── structure.md
│
├── README.md
├── requirements.txt
```

---
## 📂 Descripción por Carpeta

### `/data`

Contiene todos los datasets del proyecto organizados por etapa del pipeline.

#### `/raw`

Datos originales sin procesar. Representan la fuente de verdad inicial.

* **raw_market_data.csv**  
  Dataset sintético de ventas generado con lógica de negocio:  
  - estacionalidad  
  - inflación  
  - comportamiento por categoría  

* **weather_data.csv**  
  Datos climáticos históricos obtenidos desde API externa (Open-Meteo), alineados al rango temporal de ventas.

#### `/processed`

Datos transformados y listos para análisis.

* **clean_market_data.csv**  
  Dataset de ventas limpio:  
  - manejo de nulos  
  - corrección de tipos  
  - tratamiento de outliers (winsorización)  
  - generación de variables temporales  

* **final_dataset.csv**  
  Dataset enriquecido final:  
  - integración ventas + clima  
  - generación de features (revenue, clima, rolling metrics)  
  - listo para análisis, SQL y visualización  

#### `/processed/sql_outputs`

Resultados de consultas analíticas ejecutadas sobre el dataset final.

* **sales_by_day.csv**  
  Agregación diaria de ventas:  
  - revenue total  
  - unidades vendidas  

* **top_products.csv**  
  Ranking de productos:  
  - mayor revenue  
  - mayor volumen de ventas  

* **rolling_avg.csv**  
  Promedios móviles de ventas (7 días) por producto usando funciones de ventana.  

* **product_ranking.csv**  
  Ranking global y por categoría:  
  - uso de window functions  
  - comparación de desempeño entre productos  

---

### `/src`

Código principal del proyecto, organizado por etapas del pipeline ETL y análisis.

#### `/ingestion`

Responsable de la generación y obtención de datos.

* **data_generator.py**  
  Genera datos sintéticos de ventas con comportamiento realista:  
  - estacionalidad (festivos, fines de semana)  
  - inflación a lo largo del tiempo  
  - variabilidad por producto y categoría  
  - inyección controlada de anomalías  

* **weather_api.py**  
  Consume API de clima (Open-Meteo):  
  - detección automática de rango de fechas desde dataset de ventas  
  - extracción de temperatura y precipitación  
  - generación de dataset climático alineado temporalmente  

#### `/processing`

Encargado de la transformación y enriquecimiento de los datos.

* **data_cleaning.py**  
  Pipeline de limpieza:  
  - eliminación de registros inválidos  
  - imputación de valores  
  - detección de outliers (IQR)  
  - winsorización de precios  
  - generación de variables temporales  
  - métricas de calidad de datos  

* **feature_engineering.py**  
  Enriquecimiento del dataset:  
  - integración ventas + clima  
  - cálculo de revenue  
  - variables derivadas (lluvia, temperatura categórica, fin de semana)  
  - métricas móviles (rolling averages)  

#### `/analysis`

Capa analítica y de validación del pipeline.

* **eda.py**  
  Análisis exploratorio de datos:  
  - tendencias de ventas  
  - estacionalidad  
  - impacto del clima  

* **run_sql.py**  
  Ejecución de queries SQL con DuckDB:  
  - lectura de archivos `.sql`  
  - ejecución sobre dataset final  
  - exportación de resultados a `/data/processed/sql_outputs`  

* **validate_sql_vs_python.py**  
  Validación cruzada:  
  - comparación de resultados SQL vs pandas  
  - verificación de consistencia en métricas clave  
  - aseguramiento de integridad del pipeline  

---

### `/sql`

Contiene las consultas analíticas utilizadas para validación y análisis.

* **sales_by_day.sql** → Agregación diaria de ventas (revenue y unidades)  
* **top_products.sql** → Identificación de productos con mayor desempeño  
* **rolling_avg.sql** → Cálculo de promedios móviles usando window functions  
* **product_ranking.sql** → Ranking global y por categoría utilizando funciones de ventana  

---

### `/tests`

Validación automática del pipeline.

* **test_data_quality.py**  
  Tests con pytest para asegurar calidad de datos:  
  - dataset no vacío  
  - ausencia de nulos críticos  
  - revenue consistente  
  - coherencia de features generadas  

---

### `/notebooks`

Espacio para análisis exploratorio más detallado y narrativo en Jupyter.

---

### `/dashboards`

Visualización de datos.

* **MarketPulse_PBI.pbix**  
  Dashboard en Power BI con métricas de negocio e insights.

---

### `/docs`

Documentación del proyecto.

* **charter.md** → Definición del proyecto, objetivos, alcance y stack tecnológico  
* **structure.md** → Descripción de la arquitectura y organización del repositorio  

---

## 📄 Archivos Raíz

* **README.md**  
  Documento principal del proyecto:  
  - explicación del problema  
  - arquitectura  
  - tecnologías utilizadas  
  - resultados e insights  

* **requirements.txt**  
  Dependencias necesarias para ejecutar el proyecto.

---

## 🔄 Flujo del Pipeline

```
data_generator.py
↓
raw_market_data.csv
↓
data_cleaning.py
↓
clean_market_data.csv
↓
weather_api.py
↓
weather_data.csv
↓
feature_engineering.py
↓
final_dataset.csv
↓
SQL (DuckDB queries)
↓
sql_outputs/
↓
validate_sql_vs_python.py
↓
EDA / Power BI
```

---

## 🧠 Notas

* No modificar datos en `/raw`  
* Todo procesamiento ocurre en `/src/processing`  
* SQL se utiliza como capa analítica y de validación  
* Outputs SQL se almacenan en `/data/processed/sql_outputs`  
* Pipeline diseñado para ser reproducible, validable y escalable  