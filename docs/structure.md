# 📁 MarketPulse – Estructura del Proyecto

## 🧱 Estructura General

```
marketpulse/
│
├── data/
│ ├── raw/
│ │ ├── raw_market_data.csv
│ │ └── weather_data.csv
│ ├── processed/
│ │ ├── clean_market_data.csv
│ │ ├── final_dataset.csv
│ │ └── sql_outputs/
│ │ ├── sales_by_day.csv
│ │ ├── top_products.csv
│ │ └── rolling_avg.csv
│
├── src/
│ ├── ingestion/
│ │ ├── data_generator.py
│ │ └── weather_api.py
│ ├── processing/
│ │ ├── data_cleaning.py
│ │ └── feature_engineering.py
│ ├── analysis/
│ │ ├── eda.py
│ │ └── run_sql.py
│ ├── sql/
│ │ ├── sales_by_day.sql
│ │ ├── top_products.sql
│ │ └── rolling_avg.sql
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

Contiene los datasets del proyecto separados por estado del pipeline.

* **raw/** → datos originales sin procesar (ventas + clima)
* **processed/** → datos limpios y enriquecidos listos para análisis

---

### `/src`

Código principal del proyecto, organizado por etapas del pipeline.

#### `/ingestion`

* `data_generator.py`
  Genera datos sintéticos de ventas con lógica de negocio:

  * estacionalidad
  * inflación
  * comportamiento por categoría

* `weather_api.py`
  Obtiene datos climáticos históricos y los adapta dinámicamente al rango del dataset de ventas.

---

#### `/processing`

* `data_cleaning.py`
  Pipeline de limpieza:

  * manejo de nulos
  * validación de datos
  * detección y tratamiento de outliers
  * generación de variables temporales

* `feature_engineering.py`
  Enriquecimiento del dataset:

  * integración ventas + clima
  * generación de features (clima, revenue, categorías)

---

#### `/analysis`

* `eda.py`
  Análisis exploratorio:

  * tendencias
  * estacionalidad
  * impacto de variables externas

---

### `/notebooks`

Espacio para análisis exploratorio más narrativo (EDA).

---

### `/dashboards`

* `marketpulse.pbix`
  Dashboard en Power BI.

---

### `/docs`

* `charter.md`
  Definición del proyecto, objetivos y alcance.

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
SQL (DuckDB)
↓
sql_outputs/
↓
EDA / Power BI
```

---

## 🧠 Notas

* No modificar datos en `/raw`
* Todo procesamiento ocurre en `/src/processing`
* SQL se utiliza para validación y análisis paralelo
* Outputs analíticos se almacenan en `/data/processed/sql_outputs`
* Pipeline diseñado para ser reproducible y validable