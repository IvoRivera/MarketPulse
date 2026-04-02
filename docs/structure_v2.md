# 📁 MarketPulse – Estructura del Proyecto

## 🧱 Estructura General

```
marketpulse/
│
├── data/
│   ├── raw/
│   │   ├── raw_market_data.csv
│   │   └── weather_data.csv
│   ├── processed/
│   │   ├── clean_market_data.csv
│   │   └── enriched_dataset.csv
│   ├── curated/
│   │   ├── fact_sales.parquet
│   │   ├── dim_date.parquet
│   │   ├── dim_product.parquet
│   │   └── dim_weather.parquet
│
├── src/
│   ├── extract/
│   │   ├── data_generator.py
│   │   └── weather_api.py
│   │
│   ├── transform/
│   │   ├── data_cleaning.py
│   │   ├── feature_engineering.py
│   │   └── data_modeling.py
│   │
│   ├── load/
│   │   └── load_to_s3.py
│   │
│   ├── sql/
│   │   └── analytics_queries.sql
│   │
│   ├── main.py
│
├── airflow/
│   └── dags/
│       └── marketpulse_dag.py
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── notebooks/
├── dashboards/
│   └── marketpulse.pbix
│
├── docs/
│   └── charter.md
│
├── config.yaml
├── requirements.txt
├── README.md
```

---

## 📂 Descripción por Carpeta

### `/data`

Datasets organizados por capa del pipeline:

* **raw/** → datos originales (ventas + clima)
* **processed/** → datos limpios y enriquecidos
* **curated/** → modelo analítico (star schema)

---

### `/src`

Código principal del pipeline con estructura ETL.

#### `/extract`

* `data_generator.py` → generación de datos sintéticos
* `weather_api.py` → consumo de API externa

---

#### `/transform`

* `data_cleaning.py` → limpieza y validación
* `feature_engineering.py` → enriquecimiento (ventas + clima)
* `data_modeling.py` → construcción de modelo dimensional:

  * fact_sales
  * dimensiones

---

#### `/load`

* `load_to_s3.py` → carga de datos a AWS S3

---

#### `/sql`

* `analytics_queries.sql` → validaciones y análisis con SQL:

  * agregaciones
  * window functions
  * validación de pipeline

---

#### `main.py`

Orquestador local del pipeline:

extract → transform → load

---

### `/airflow`

* `marketpulse_dag.py` → DAG que orquesta el pipeline completo

---

### `/docker`

* `Dockerfile` → entorno del pipeline
* `docker-compose.yml` → levanta servicios (pipeline + Airflow)

---

## 🔄 Flujo del Pipeline

```
[Extract]
data_generator + weather_api
        ↓
[Raw]
data/raw/
        ↓
[Transform]
data_cleaning + feature_engineering
        ↓
[Processed]
enriched_dataset.csv
        ↓
[Modeling]
data_modeling.py
        ↓
[Curated]
star schema (fact + dims)
        ↓
[Load]
S3 (AWS)
        ↓
[Athena / SQL]
queries analíticas
        ↓
[BI]
Power BI Dashboard
```

---

## ⚙️ Orquestación

* Pipeline ejecutable con `main.py`
* Orquestación profesional con Airflow (DAG)
* Contenerización con Docker

---

## 🧠 Notas

* Pipeline diseñado para ser reproducible y escalable
* Separación clara por capas (raw → processed → curated)
* SQL utilizado para validación y análisis
* Arquitectura alineada a prácticas reales de Data Engineering
