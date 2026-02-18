# Project Charter: MarketPulse MVP

## 1. Visión del Proyecto
Optimizar la rentabilidad de una PyME local mediante el análisis de la dispersión de precios y la identificación de valores atípicos (outliers) en las ventas.

## 2. Problema de Negocio
El negocio carece de visibilidad sobre si sus precios están alineados con el mercado y cómo afectan los valores extremos (errores o ventas excepcionales) al promedio de sus márgenes.

## 3. Objetivos (Scope Semanal)
- **Ingeniería de Datos:** Crear y limpiar un dataset de 10,000 registros usando Python.
- **Análisis Estadístico:** Aplicar Winsorización para normalizar la distribución de precios.
- **Business Intelligence:** Dashboard interactivo que identifique el top 5% de productos fuera de rango de precio.

## 4. Tecnologías
- **Python:** Pandas, NumPy (Limpieza y Estadística).
- **Power BI:** DAX (Medidas de tiempo y comparación), MAQ Box Plot (Visualización).
- **GitHub:** Control de versiones y documentación.

## 5. Criterios de Éxito
- Repositorio público con código reproducible.
- Dashboard funcional con filtros dinámicos de tiempo y categoría.
- README que explique un hallazgo de negocio real basado en los datos.