# Project Charter: MarketPulse

## 1. Visión del Proyecto

Construir un **pipeline de datos end-to-end** que permita a una panadería analizar su rendimiento histórico y entender los factores que impactan sus ventas, integrando datos internos con fuentes externas.

El objetivo es simular un caso real donde el negocio pasa de decisiones intuitivas a decisiones basadas en datos.

---

## 2. Problema de Negocio

Las pequeñas empresas de retail no cuentan con sistemas robustos de datos, lo que genera:

* Datos inconsistentes (errores de registro, outliers)
* Falta de visibilidad sobre tendencias de ventas
* Decisiones basadas en intuición (ej: precios, stock, promociones)

Esto impide responder preguntas clave como:

* ¿Cuándo vendo más y por qué?
* ¿Qué factores externos afectan mis ventas?
* ¿Qué productos generan mayor valor?

---

## 3. Objetivos del Proyecto

### 🧱 Ingeniería de Datos

* Construir un pipeline en Python que:

  * Genere y procese datos históricos (10 años)
  * Limpie y valide datos automáticamente
  * Estructure datos en formato analítico

### 🔗 Integración de Datos

* Enriquecer el dataset con variables externas como:

  * Clima o feriados
* Unificar datos en un modelo analítico

### 📊 Análisis

* Identificar:

  * Tendencias de ventas
  * Estacionalidad
  * Impacto de variables externas

### 📈 Visualización

* Desarrollar un dashboard en Power BI que permita:

  * Monitorear KPIs clave
  * Explorar patrones de negocio
  * Apoyar la toma de decisiones

---

## 4. Stack Tecnológico

* **Python** → ETL (generación, limpieza, transformación)
* **APIs externas** → enriquecimiento de datos
* **AWS (S3)** → almacenamiento de datos
* **Power BI** → visualización
* **GitHub** → versionado y documentación

---

## 5. Criterios de Éxito

* Pipeline reproducible de datos (raw → processed)
* Integración de al menos una fuente externa
* Dataset limpio y validado
* Dashboard funcional con insights claros
* Proyecto documentado y entendible en GitHub

---

## 6. Resultado Esperado

Un proyecto de portafolio que demuestre:

* Manejo de datos end-to-end
* Capacidad de integrar múltiples fuentes
* Generación de insights de negocio
* Uso de herramientas reales del stack de datos
