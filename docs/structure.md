# 📁 MarketPulse – Estructura del Proyecto

## 🧱 Estructura General

```
marketpulse/
│
├── data/
│   ├── raw/
│   │   └── raw_market_data.csv
│   ├── processed/
│
├── src/
│   ├── ingestion/
│   │   └── data_generator.py
|   |   └── weater_api.py
│   ├── processing/
│   │   └── data_cleaning.py
│   ├── analysis/
│   │   └── eda.py
│
├── notebooks/
├── dashboards/
│   └── marketpulse.pbix
│
├── docs/
│   └── charter.md
│
├── README.md
├── requirements.txt
```

---

## 📂 Descripción por Carpeta

### `/data`

Contiene los datasets del proyecto separados por estado del pipeline.

* **raw/** → datos originales sin procesar
* **processed/** → datos limpios listos para análisis

---

### `/src`

Código principal del proyecto, organizado por etapas del pipeline.

#### `/ingestion`

* `data_generator.py`
  Genera datos sintéticos de ventas (10 años) simulando estacionalidad y comportamiento de negocio.

  *`weather_api.py`
  Integración de api del tiempo, comportamiento de ventas según clima.

---

#### `/processing`

* `data_cleaning.py`
  Limpia y transforma los datos:

  * Manejo de nulos
  * Corrección de tipos
  * Eliminación de outliers / errores
  * Generación de dataset limpio

* `feature_engineering.py`
  Integración de datos externos y generación de variables derivadas para análisis de comportamiento de ventas

---

#### `/analysis`

* `eda.py`
  Análisis exploratorio:

  * Tendencias
  * Estacionalidad
  * Patrones de ventas
  * Generación de insights iniciales

---

### `/notebooks`

Espacio para análisis exploratorio en Jupyter (EDA más visual y narrativo).

---

### `/dashboards`

* `marketpulse.pbix`
  Dashboard en Power BI con visualizaciones de negocio.

---

### `/docs`

* `charter.md`
  Definición del proyecto, objetivos y alcance.

---

## 📄 Archivos Raíz

* `README.md`
  Descripción general del proyecto (para reclutadores)

* `requirements.txt`
  Dependencias del proyecto

---

## 🔄 Flujo del Pipeline

```
data_generator.py
        ↓
raw_market_data.csv
        ↓
data_cleaning.py
        ↓
processed data
        ↓
eda.py / notebooks
        ↓
Power BI dashboard
```

---

## 🧠 Notas

* Mantener separación clara entre `raw` y `processed`
* No modificar datos en `raw`
* Todo procesamiento debe ocurrir en `/src/processing`
* Este documento debe actualizarse si cambia la estructura
