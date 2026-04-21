# 📁 MarketPulse – Estructura del Proyecto

## 🧱 Estructura General

```
marketpulse/
│
├── data/
│ ├── raw/                   # Ignorado por Git
│ │ ├── raw_market_data.csv
│ │ └── weather_data.csv
│ │
│ ├── processed/             # Ignorado por Git
│ │ ├── clean_market_data.csv
│ │ ├── final_dataset.csv
│ │ └── sql_outputs/
│ │   ├── sales_by_day.csv
│ │   ├── top_products.csv
│ │   ├── rolling_avg.csv
│ │   └── product_ranking.csv
│ │
│ └── sample_data.csv        # Único dataset versionado (demo)
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
│ ├── sql/
│ │ ├── sales_by_day.sql
│ │ ├── top_products.sql
│ │ ├── rolling_avg.sql
│ │ └── product_ranking.sql
│ │
│ ├── analysis/
│ │ └── run_sql.py           # SOLO ejecución productiva
│ │
│ └── main.py                # Entrypoint del pipeline
│
├── tests/
│ ├── test_data_quality.py
│ └── test_sql_reconciliation.py
│
├── notebooks/
│ └── 01_eda.ipynb
│
├── dashboards/
│ └── marketpulse_dashboard.pbix
│
├── docs/
│ ├── charter.md
│ ├── structure.md
│ └── screenshots/
│     └── dashboard_overview.png
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
```

---
## 📂 Descripción por Carpeta

### `/data`

Contiene los datasets del proyecto organizados por etapa del pipeline.

⚠️ **Importante:**  
Las carpetas `/raw` y `/processed` están excluidas del control de versiones (`.gitignore`).  
Solo `sample_data.csv` se versiona para permitir reproducibilidad en entornos externos.

#### `/raw`

Datos originales sin procesar. Representan la fuente de verdad inicial del pipeline.

- **raw_market_data.csv**  
    Dataset sintético de ventas generado con lógica de negocio:
    - estacionalidad
    - inflación
    - comportamiento por categoría
    - inyección controlada de anomalías
- **weather_data.csv**  
    Datos climáticos históricos obtenidos desde API externa (Open-Meteo), alineados temporalmente con las ventas.

---

#### `/processed`

Datos transformados y listos para consumo analítico.

- **clean_market_data.csv**  
    Dataset de ventas limpio:
    - manejo de nulos
    - corrección de tipos
    - detección y tratamiento de outliers
    - generación de variables temporales
- **final_dataset.csv**  
    Dataset enriquecido final:
    - integración ventas + clima
    - cálculo de métricas (revenue, indicadores climáticos)
    - generación de features (rolling metrics, flags de negocio)
    - listo para análisis en SQL y visualización

---

#### `/processed/sql_outputs`

Resultados de consultas analíticas ejecutadas sobre el dataset final.

- **sales_by_day.csv**  
    Agregación diaria de ventas:
    - revenue total
    - unidades vendidas
- **top_products.csv**  
    Ranking de productos:
    - mayor revenue
    - mayor volumen de ventas
- **rolling_avg.csv**  
    Promedios móviles de ventas (7 días) por producto usando funciones de ventana
- **product_ranking.csv**  
    Ranking global y por categoría:
    - uso de window functions
    - comparación de desempeño entre productos

---

#### `/sample_data.csv`

Subconjunto reducido del dataset final (100–500 filas) utilizado para:

- facilitar la ejecución del proyecto sin necesidad de regenerar datos
- permitir revisión por parte de recruiters
- demostrar reproducibilidad del pipeline

---

### `/src`

Código fuente principal del proyecto, organizado por etapas del pipeline ETL.

---

#### `/ingestion`

Responsable de la generación y obtención de datos.

- **data_generator.py**  
    Genera datos sintéticos de ventas con comportamiento realista:
    - estacionalidad (festivos, fines de semana)
    - inflación a lo largo del tiempo
    - variabilidad por producto y categoría
    - inyección controlada de anomalías
- **weather_api.py**  
    Consume API de clima (Open-Meteo):
    - detección automática del rango de fechas
    - extracción de temperatura y precipitación
    - generación de dataset climático alineado

---

#### `/processing`

Encargado de la transformación, limpieza y enriquecimiento de los datos.

- **data_cleaning.py**  
    Pipeline de limpieza:
    - eliminación de registros inválidos
    - imputación de valores
    - detección de outliers (IQR)
    - winsorización de precios
    - generación de variables temporales
    - métricas de calidad de datos
- **feature_engineering.py**  
    Enriquecimiento del dataset:
    - integración ventas + clima
    - cálculo de revenue
    - variables derivadas (lluvia, temperatura categórica, fin de semana)
    - métricas móviles (rolling averages)

---

#### `/analysis`

Capa analítica productiva del pipeline.

- **run_sql.py**  
    Ejecución de queries SQL con DuckDB:
    - lectura de archivos `.sql`
    - ejecución sobre dataset final
    - exportación de resultados a `/data/processed/sql_outputs`

---

#### `/sql`

Consultas analíticas utilizadas para exploración y validación.

- **sales_by_day.sql** → Agregación diaria de ventas
- **top_products.sql** → Identificación de productos con mayor desempeño
- **rolling_avg.sql** → Promedios móviles con window functions
- **product_ranking.sql** → Ranking global y por categoría

---

#### `main.py`

Entrypoint del pipeline completo.

Permite ejecutar de forma secuencial:

- generación de datos
- limpieza
- integración con clima
- feature engineering

👉 Ejecutable mediante:

python -m src.main

---

### `/tests`

Validación automática del pipeline y consistencia analítica.

- **test_data_quality.py**  
    Tests de calidad de datos:
    - dataset no vacío
    - ausencia de nulos críticos
    - consistencia de métricas
    - integridad de features
- **test_sql_reconciliation.py**  
    Validación cruzada entre Python (pandas) y SQL (DuckDB):
    - comparación de agregaciones
    - verificación de métricas clave
    - consistencia entre capas analíticas

---

### `/notebooks`

Espacio para análisis exploratorio (EDA) separado del código productivo.

- **01_eda.ipynb**  
    Análisis exploratorio del dataset:
    - tendencias de ventas
    - estacionalidad
    - impacto del clima
    - validación visual de hipótesis

---

### `/dashboards`

Visualización de datos.

- **marketpulse_dashboard.pbix**  
    Dashboard en Power BI que incluye:
    - KPIs principales (revenue, unidades, ticket promedio)
    - tendencias temporales
    - top productos
    - impacto del clima
    - comparación semana vs fin de semana

---

### `/docs`

Documentación del proyecto.

- **charter.md** → definición del problema, objetivos y alcance
- **structure.md** → descripción de arquitectura y organización del repositorio

#### `/screenshots`

Capturas del dashboard para revisión rápida sin necesidad de Power BI.

- **dashboard_overview.png** → vista general con KPIs e insights

---

## 📄 Archivos Raíz

- **README.md**  
    Documento principal del proyecto:
    - contexto de negocio
    - arquitectura del pipeline
    - stack tecnológico
    - insights y conclusiones
- **requirements.txt**  
    Dependencias necesarias para ejecutar el proyecto  
    (pandas, numpy, duckdb, pytest, etc.)

---

## 🔄 Flujo del Pipeline

El pipeline completo puede ejecutarse desde:

python -m src.main

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
run_sql.py (DuckDB)
↓
sql_outputs/
↓
tests (validación)
↓
EDA / Power BI
```

---

## 🧠 Notas

* `/data/raw` y `/data/processed` están excluidos de Git  
* `sample_data.csv` permite reproducibilidad del proyecto  
* Todo procesamiento ocurre en `/src/processing`  
* SQL se utiliza como capa analítica y de validación  
* Validaciones críticas se encuentran en `/tests`  
* EDA se realiza en notebooks, separado del código productivo  
* El pipeline puede ejecutarse desde `src/main.py`  
* Screenshots permiten evaluación rápida sin necesidad de ejecutar el dashboard  