# Project Charter: MarketPulse

## 1. Visión del Proyecto

Construir un **pipeline de datos end-to-end profesional** que simule un entorno real de ingeniería de datos, permitiendo a una panadería analizar su rendimiento histórico mediante la integración de datos internos y fuentes externas.

El proyecto evoluciona desde un flujo básico de datos hacia una **arquitectura moderna**, incluyendo orquestación, modelado y despliegue en la nube.

---

## 2. Problema de Negocio

Las pequeñas empresas de retail enfrentan:

* Datos inconsistentes y dispersos
* Falta de integración entre fuentes internas y externas
* Ausencia de sistemas analíticos estructurados
* Decisiones basadas en intuición

Esto impide responder preguntas clave como:

* ¿Qué factores impactan las ventas?
* ¿Cómo influye el clima en el rendimiento?
* ¿Qué productos generan mayor valor?

---

## 3. Objetivos del Proyecto

### 🧱 Ingeniería de Datos

* Construir un pipeline ETL en Python que:

  * Genere datos históricos
  * Integre APIs externas
  * Limpie y valide datos
  * Modele datos en formato analítico (star schema)

---

### ⚙️ Arquitectura y Backend

* Estructurar el pipeline como sistema productivo:

  * Modularización (extract / transform / load)
  * Configuración externa (config.yaml)
  * Logging y manejo de errores
* Contenerizar con Docker
* Orquestar con Airflow (DAG)

---

### ☁️ Cloud & Data Platform

* Almacenar datos en AWS S3 (raw, processed, curated)
* Consultar datos con Athena
* Aplicar SQL para validación y análisis

---

### 📊 Análisis y Visualización

* Generar insights de negocio:

  * tendencias
  * estacionalidad
  * impacto de variables externas
* Construir dashboard en Power BI

---

## 4. Stack Tecnológico

* **Python** → ETL / procesamiento
* **SQL** → validación y análisis
* **Docker** → contenerización
* **Airflow** → orquestación de pipelines
* **AWS (S3 + Athena)** → almacenamiento y consulta
* **Power BI** → visualización
* **GitHub** → versionado

---

## 5. Criterios de Éxito

* Pipeline ejecutable end-to-end
* Integración de múltiples fuentes (ventas + clima)
* Modelo dimensional implementado
* Pipeline orquestado con Airflow
* Contenerización con Docker
* Datos disponibles en AWS
* Queries SQL funcionando sobre datos reales
* Dashboard con insights claros
* Documentación completa

---

## 6. Resultado Esperado

Un proyecto de portafolio que demuestre:

* Construcción de pipelines de datos reales
* Integración de APIs y múltiples fuentes
* Modelado de datos (star schema)
* Uso de herramientas modernas del stack de datos
* Capacidad de trabajar con cloud, orquestación y backend

---

## 7. Enfoque del Proyecto

Este proyecto no busca ser un simple ejercicio analítico, sino:

> Simular el trabajo de un Data Engineer en un entorno real

Priorizando:

* reproducibilidad
* escalabilidad
* claridad arquitectónica
* alineación con el mercado laboral
