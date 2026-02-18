# Project Charter: MarketPulse MVP

## 1. Visión del Proyecto
Implementar un pipeline de Integridad de Datos y un sistema de Inteligencia de Precios que permita a una PyME del sector retail (Panadería) transicionar de una fijación de precios basada en la intuición a una estrategia basada en evidencia histórica y proyecciones de rentabilidad

## 2. Problema de Negocio
En el contexto de alta inflación en Chile (2016-2026), los comercios locales pierden margen de ganancia por dos factores críticos: la incapacidad de ajustar precios de forma proporcional al aumento de costos y la distorsión de KPIs financieros debido a errores humanos en el registro de ventas (outliers operativos).

## 3. Objetivos (Scope Semanal)
- **Ingeniería de Datos:** Ingeniería de Datos: Desarrollar un pipeline en Python que gestione un histórico de 10 años (~18,000+ registros), simulando ciclos económicos y estacionalidad cultural chilena.
- **Aseguramiento de Calidad:** Automatizar la detección de anomalías mediante Winsorización, eliminando el impacto de errores de digitación en el cálculo de márgenes.
- **Análisis de Valor:** Cuantificar la Elasticidad de Precio y el crecimiento YoY (Año a Año) para identificar los "motores de ingresos" del negocio.

## 4. Tecnologías
- **Python:** Generación de datos sintéticos con tendencia inflacionaria y limpieza estadística.
- **Power BI:** Implementación de Time Intelligence para análisis de una década y parámetros What-if para simulación de escenarios.
- **GitHub:** Gestión del ciclo de vida del proyecto y documentación técnica (README).

## 5. Criterios de Éxito
- Scripts que generen y limpien el dataset de 10 años en menos de un minuto.
- Dashboard con tres pestañas funcionales (Vista Gerencial, Integridad de Datos y Simulador de Estrategia).
- Un informe que detalle cómo la limpieza de datos reveló una "fuga de margen" o una oportunidad de precio no aprovechada durante las Fiestas Patrias.