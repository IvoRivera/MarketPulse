# 📊 MarketPulse — Data Engineering & Analytics Pipeline

---

## 📌 Resumen Ejecutivo

**MarketPulse** es un pipeline end-to-end de *data engineering y analytics* que simula el comportamiento de ventas de un negocio de alimentos durante 10 años, incorporando condiciones realistas como estacionalidad, inflación y errores de calidad de datos.

A diferencia de un análisis tradicional, el proyecto no parte de datos “limpios”, sino que introduce anomalías controladas (errores de precios, valores nulos) y construye un pipeline robusto para su detección, corrección y validación.

El resultado es una capa analítica confiable, validada en múltiples niveles y lista para consumo en herramientas BI.

---

## 🎯 Objetivo

Construir un pipeline reproducible y validable que permita:

- Simular datos de ventas con comportamiento realista (estacionalidad, inflación, ruido).
- Introducir y corregir problemas de calidad de datos.
- Integrar variables externas (clima) como factor explicativo.
- Validar consistencia entre distintas capas analíticas (Python vs SQL).
- Modelar datos para consumo analítico (Power BI).

---

## 🏗️ Arquitectura del sistema

El pipeline sigue una arquitectura por capas:

Data Generation (Source)
↓
Raw Layer (datos con ruido)
↓
Cleaning Layer (normalización y outliers)
↓
Feature Engineering (variables derivadas + clima)
↓
Analytics Layer (SQL - DuckDB)
↓
Validation Layer (pytest + SQL vs pandas)
↓
BI Layer (Power BI)


---

## ⚙️ Stack Tecnológico

- **Python (pandas, numpy)** → procesamiento y transformación  
- **DuckDB** → análisis SQL y validación cruzada  
- **Pytest** → validación de calidad de datos  
- **Power BI** → modelado dimensional y visualización  
- **Open-Meteo API** → integración de datos climáticos  

---

## 🧪 Ingeniería de Datos y Calidad

El foco del proyecto está en la **calidad y confiabilidad del dato**:

### 🔹 Generación de datos con anomalías
- Inyección controlada de errores:
  - precios multiplicados/divididos incorrectamente  
  - valores nulos  
- Simulación de condiciones reales de captura de datos

### 🔹 Pipeline de limpieza
- Eliminación de registros inválidos  
- Detección de outliers mediante IQR  
- Winsorización para corregir valores extremos  
- Normalización de tipos  

👉 Se corrigieron más de **$1.1M CLP en distorsión de precios**.

### 🔹 Validación automatizada
- Tests con **pytest**:
  - dataset no vacío  
  - no nulos en columnas críticas  
  - revenue consistente  
- Validación cruzada:
  - **Python (pandas) vs SQL (DuckDB)**  
  - consistencia total en métricas agregadas  

---

## 📊 Métricas del Dataset

- 📅 **Horizonte temporal:** 2016–2026  
- 📦 **Registros:** ~88,000 transacciones  
- 💰 **Revenue total:** $8,284,207,708 CLP  
- 📦 **Unidades vendidas:** 2,861,772  
- 🧾 **Ticket promedio:** ~$3,070  
- 🌧️ **Días con lluvia:** 3,757  

---

## 📈 Insights de Negocio

### 1. Estabilidad y crecimiento
- Ingresos mensuales entre **60M y 80M CLP en 2024**
- Crecimiento sostenido sin alta volatilidad  

👉 Negocio estable y predecible.

---

### 2. Impacto del clima
- 🌤️ Templado → ~60% del revenue  
- ☀️ Caluroso → ~28%  
- ❄️ Frío → menor contribución  

👉 El clima actúa como driver directo de la demanda.

---

### 3. Estructura del negocio

| Tipo de producto | Rol |
|------------------|-----|
| Panes            | Volumen alto y flujo constante |
| Pastelería       | Bajo volumen, alto ingreso por unidad |

👉 Modelo híbrido: **volumen + margen**

---

### 4. Patrón de consumo
- 🗓️ 65% ventas en días laborales  
- 🎉 35% en fines de semana  

👉 Consumo principalmente cotidiano.

---

## 🧠 Modelo de Datos

Se implementa un modelo tipo **star schema**:

- **fact_sales** → métricas de ventas  
- **dim_product** → información de productos  
- **dim_date** → calendario  
- **dim_weather** → condiciones climáticas  

👉 Optimizado para consumo en BI y análisis SQL.

---

## 📊 Dashboard

Incluye:

- KPIs (revenue, unidades, ticket promedio)  
- Tendencia temporal  
- Top productos  
- Impacto del clima  
- Comparación semana vs fin de semana

### Vista general
![Dashboard Overview](docs/img/dashboard_overview.png)

📁 `/dashboards/MarketPulse_PBI.pbix`

---

## 🧪 Validación

El sistema asegura consistencia en múltiples niveles:

- ✔ Tests automatizados (pytest)  
- ✔ Validación SQL vs pandas  
- ✔ Integridad del modelo dimensional  
- ✔ Sin nulos tras joins  

👉 Pipeline confiable y reproducible.

---

## 🏗️ Estructura del proyecto

/ingestion → generación y obtención de datos
/processing → limpieza y transformación
/analysis → SQL + validación
/sql → queries analíticas
/tests → calidad de datos
/dashboards → visualización

📄 Ver detalle: `/docs/structure.md`

---

## 🧠 Conclusiones

Este proyecto demuestra que:

### 🔹 1. Los datos no son confiables por defecto  
La inyección de errores y su posterior corrección refleja escenarios reales de producción.

---

### 🔹 2. La validación es tan importante como el análisis  
Sin consistencia entre herramientas (SQL vs Python), los insights no son confiables.

---

### 🔹 3. El negocio tiene una estructura clara  
- Volumen → productos básicos  
- Margen → productos premium  

---

### 🔹 4. Factores externos importan  
El clima impacta directamente la demanda y debe considerarse en decisiones operativas.

---

## 🚀 Próximos pasos

- Forecasting (series de tiempo)  
- Migración a cloud (S3 + Athena / BigQuery)  
- Orquestación del pipeline  
- Segmentación más avanzada  

---