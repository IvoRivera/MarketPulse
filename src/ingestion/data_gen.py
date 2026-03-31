import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime

# =========================
# CONFIGURACIÓN 
# ========================= 

# 1. Cofiguración temporal inicial y salida

OUTPUT_PATH = Path("data/raw/raw_market_data.csv") 
START_DATE = "2016-01-01" 
END_DATE = datetime.now().strftime("%Y-%m-%d") 
DATE_RANGE = pd.date_range(start=START_DATE, end=END_DATE, freq='D')

np.random.seed(42)


def get_product_catalog():

# ========================= 
# CATÁLOGO DE PRODUCTOS
# =========================
    """ Definicion de un catalogo para generar un dataset de 10 años con 25+ productos y lógica estacional avanzada """
    
    # 2. Catálogo Extendido (25 productos en 5 categorías)
    # Incluimos 'cost_factor' para posterior análisis de margen de contribución
    products = [
        # Categoría: Panes (Venta por kg)
        {'id': 101, 'cat': 'Panes', 'name': 'Marraqueta', 'base_price': 1400, 'daily_vol': 90, 'cost_f': 0.4},
        {'id': 102, 'cat': 'Panes', 'name': 'Hallulla', 'base_price': 1400, 'daily_vol': 80, 'cost_f': 0.4},
        {'id': 103, 'cat': 'Panes', 'name': 'Pan Integral', 'base_price': 1800, 'daily_vol': 30, 'cost_f': 0.45},
        {'id': 104, 'cat': 'Panes', 'name': 'Pan de Molde', 'base_price': 2200, 'daily_vol': 25, 'cost_f': 0.35},
        {'id': 105, 'cat': 'Panes', 'name': 'Baguette', 'base_price': 1100, 'daily_vol': 20, 'cost_f': 0.5},
        
        # Categoría: Pastelería (Venta por unidad)
        {'id': 201, 'cat': 'Pastelería', 'name': 'Berlín Crema', 'base_price': 1200, 'daily_vol': 40, 'cost_f': 0.3},
        {'id': 202, 'cat': 'Pastelería', 'name': 'Alfajor Maicena', 'base_price': 1000, 'daily_vol': 50, 'cost_f': 0.25},
        {'id': 203, 'cat': 'Pastelería', 'name': 'Kuchen de Manzana', 'base_price': 2500, 'daily_vol': 15, 'cost_f': 0.4},
        {'id': 204, 'cat': 'Pastelería', 'name': 'Donas', 'base_price': 1100, 'daily_vol': 45, 'cost_f': 0.3},
        {'id': 205, 'cat': 'Pastelería', 'name': 'Pastel de Milhojas', 'base_price': 1800, 'daily_vol': 20, 'cost_f': 0.35},
        
        # Categoría: Empanadas (Venta por unidad)
        {'id': 301, 'cat': 'Empanadas', 'name': 'Pino Horno', 'base_price': 2200, 'daily_vol': 25, 'cost_f': 0.4},
        {'id': 302, 'cat': 'Empanadas', 'name': 'Queso Horno', 'base_price': 2000, 'daily_vol': 20, 'cost_f': 0.35},
        {'id': 303, 'cat': 'Empanadas', 'name': 'Pino Frita', 'base_price': 1800, 'daily_vol': 15, 'cost_f': 0.4},
        {'id': 304, 'cat': 'Empanadas', 'name': 'Queso Frita', 'base_price': 1600, 'daily_vol': 18, 'cost_f': 0.35},
        {'id': 305, 'cat': 'Empanadas', 'name': 'Napolitana', 'base_price': 2100, 'daily_vol': 12, 'cost_f': 0.4},

        # Categoría: Bebidas y Cafetería
        {'id': 401, 'cat': 'Cafetería', 'name': 'Café Espresso', 'base_price': 1500, 'daily_vol': 35, 'cost_f': 0.15},
        {'id': 402, 'cat': 'Cafetería', 'name': 'Capuchino', 'base_price': 2200, 'daily_vol': 30, 'cost_f': 0.2},
        {'id': 403, 'cat': 'Cafetería', 'name': 'Jugo Natural', 'base_price': 2500, 'daily_vol': 15, 'cost_f': 0.3},
        {'id': 404, 'cat': 'Cafetería', 'name': 'Bebida 500ml', 'base_price': 1200, 'daily_vol': 40, 'cost_f': 0.4},
        {'id': 405, 'cat': 'Cafetería', 'name': 'Té / Infusión', 'base_price': 1000, 'daily_vol': 10, 'cost_f': 0.1},

        # Categoría: Rotisería y Temporada
        {'id': 501, 'cat': 'Rotisería', 'name': 'Pan de Pascua', 'base_price': 4500, 'daily_vol': 0, 'cost_f': 0.3},
        {'id': 502, 'cat': 'Rotisería', 'name': 'Mermelada Casera', 'base_price': 3200, 'daily_vol': 8, 'cost_f': 0.5},
        {'id': 503, 'cat': 'Rotisería', 'name': 'Galletas Mantequilla', 'base_price': 2800, 'daily_vol': 12, 'cost_f': 0.3},
        {'id': 504, 'cat': 'Rotisería', 'name': 'Torta Selva Negra', 'base_price': 15000, 'daily_vol': 3, 'cost_f': 0.4},
        {'id': 505, 'cat': 'Rotisería', 'name': 'Sopaipillas (bolsa)', 'base_price': 2500, 'daily_vol': 10, 'cost_f': 0.3}
    ]

# =========================
# LÓGICA DE NEGOCIO
# =========================
def get_seasonal_multiplier(date, product):
    """
    Define reglas de negocio para estacionalidad.
    """
    multiplier = 1.0

    # Fiestas Patrias
    if date.month == 9 and 15 <= date.day <= 19:
        if product['cat'] == 'Empanadas':
            multiplier = 8.5

    # Navidad
    if date.month == 12:
        if product['id'] == 501:
            multiplier = 50.0
        if product['id'] == 504:
            multiplier = 4.0

    # Invierno
    if date.month in [6, 7, 8]:
        if product['id'] == 505:
            multiplier = 3.0
        if product['cat'] == 'Cafetería':
            multiplier = 1.5

    # Fin de semana
    if date.weekday() >= 5:
        if product['cat'] == 'Pastelería':
            multiplier = 2.5
        if product['id'] == 504:
            multiplier = 3.0

    return multiplier


# =========================
# GENERACIÓN PRINCIPAL
# =========================
def generate_data():
    print("🏭 Generando datos sintéticos...")

    products = get_product_catalog()
    dates = pd.date_range(start=START_DATE, end=END_DATE, freq='D')

    rows = []

    for current_date in dates:
        years_passed = (current_date - dates[0]).days / 365.25
        inflation_factor = (1.06) ** years_passed

        for product in products:
            multiplier = get_seasonal_multiplier(current_date, product)

            units = np.random.poisson(product['daily_vol'] * multiplier)

            if units > 0:
                base_price = product['base_price'] * inflation_factor
                noisy_price = base_price + np.random.normal(0, base_price * 0.02)

                seconds_offset = np.random.randint(25200, 75600)
                timestamp = current_date + pd.to_timedelta(seconds_offset, unit='s')

                rows.append({
                    "date": timestamp,
                    "product_id": product['id'],
                    "product_name": product['name'],
                    "category": product['cat'],
                    "raw_price": round(noisy_price, 0),
                    "units_sold": units,
                    "unit_cost": round(base_price * product['cost_f'], 0)
                })

    df = pd.DataFrame(rows)
    print(f"Registros generados: {len(df)}")

    return df


# =========================
# ANOMALÍAS CONTROLADAS
# =========================
def inject_anomalies(df):
    print("⚠️ Inyectando anomalías...")

    # Precios erróneos
    idx = np.random.choice(df.index, size=int(len(df) * 0.03), replace=False)
    df.loc[idx, "raw_price"] *= np.random.choice([0.1, 5, 10])

    # Nulos
    df.loc[np.random.choice(df.index, size=int(len(df) * 0.005), replace=False), "date"] = np.nan
    df.loc[np.random.choice(df.index, size=int(len(df) * 0.007), replace=False), "product_id"] = np.nan

    return df


# =========================
# GUARDADO
# =========================
def save_data(df):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"💾 Dataset guardado en {OUTPUT_PATH}")


# =========================
# PIPELINE
# =========================
def run_pipeline():
    df = generate_data()
    df = inject_anomalies(df)
    save_data(df)
    print("✅ Generación completada.")


if __name__ == "__main__":
    run_pipeline()

