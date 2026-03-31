import pandas as pd
import numpy as np
import os
from datetime import datetime

def generate_bakery_data():
    """ Genera un dataset de 10 años con 25+ productos y lógica estacional avanzada """
    np.random.seed(42)
    
    # 1. Definición del Rango Temporal
    start_date = '2016-01-01'
    # Ajustado al tiempo actual: 2026-02-24
    end_date = datetime.now().strftime('%Y-%m-%d')
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
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
    
    data_rows = []
    
    for current_date in date_range:
        # Inflación Chilena: Ajuste anual acumulado (~5-7% promedio)
        years_passed = (current_date - date_range[0]).days / 365.25
        # Fórmula: $$ P_{final} = P_{base} \times (1 + r)^{t} $$
        inflation_factor = (1.06)**years_passed 
        
        for prod in products:
            vol_multiplier = 1.0
            
            # --- LÓGICA ESTACIONAL REALISTA ---
            # 1. Fiestas Patrias (Empanadas Sept 15-19)
            if current_date.month == 9 and 15 <= current_date.day <= 19:
                if prod['cat'] == 'Empanadas': vol_multiplier = 8.5
            
            # 2. Navidad y Fin de Año (Pan de Pascua y Tortas)
            if current_date.month == 12:
                if prod['id'] == 501: vol_multiplier = 50.0 # Pan de pascua aparece
                if prod['id'] == 504: vol_multiplier = 4.0  # Más tortas
            
            # 3. Invierno (Sopaipillas y Café en Junio-Agosto)
            if current_date.month in [6, 7, 8]:
                if prod['id'] == 505: vol_multiplier = 3.0
                if prod['cat'] == 'Cafetería': vol_multiplier = 1.5

            # 4. Fines de Semana (Pastelería y Tortas)
            if current_date.weekday() >= 5:
                if prod['cat'] == 'Pastelería': vol_multiplier = 2.5
                if prod['id'] == 504: vol_multiplier = 3.0

            # Simulación de volumen (Poisson para evitar ventas negativas)
            units = np.random.poisson(prod['daily_vol'] * vol_multiplier)
            
            if units > 0:
                price_clean = prod['base_price'] * inflation_factor
                # Ruido de mercado de ±2%
                price_with_noise = price_clean + np.random.normal(0, price_clean * 0.02)

                # --- NUEVA LÓGICA DE TIEMPO (H:M:S) ---
                # Generamos un offset aleatorio en segundos entre las 07:00:00 y las 21:00:00
                # 7 AM = 25,200 segundos | 9 PM = 75,600 segundos
                seconds_offset = np.random.randint(25200, 75600)
                sale_datetime = current_date + pd.to_timedelta(seconds_offset, unit='s')
                
                data_rows.append({
                    'date': sale_datetime,
                    'product_id': prod['id'],
                    'product_name': prod['name'],
                    'category': prod['cat'],
                    'raw_price': round(price_with_noise, 0),
                    'units_sold': units,
                    'unit_cost': round(price_clean * prod['cost_f'], 0)
                })

    df = pd.DataFrame(data_rows)
    
    # 3. INYECCIÓN DE ANOMALÍAS (3% Errores de precio)
    anomaly_idx = np.random.choice(df.index, size=int(len(df) * 0.03), replace=False)
    df.loc[anomaly_idx, 'raw_price'] = df.loc[anomaly_idx, 'raw_price'] * np.random.choice([10, 0.1, 5])
    
    # 4. INYECCIÓN DE NULOS ( <1% en campos críticos)
    # Fechas nulas (simula error de timestamp)
    null_date_idx = np.random.choice(df.index, size=int(len(df) * 0.005), replace=False)
    df.loc[null_date_idx, 'date'] = np.nan
    
    # IDs de producto nulos (simula error de escaneo/SKU)
    null_id_idx = np.random.choice(df.index, size=int(len(df) * 0.007), replace=False)
    df.loc[null_id_idx, 'product_id'] = np.nan

    # 4. Exportar
    if not os.path.exists('data'): os.makedirs('data')
    df.to_csv('data/raw_market_data.csv', index=False)
    
    print(f"Dataset 'MarketPulse' generado: {len(df)} registros.")
    print(f"Ejemplo de error inyectado: {df.loc[anomaly_idx[0], 'product_name']} a ${df.loc[anomaly_idx[0], 'raw_price']:,}")

if __name__ == "__main__":
    generate_bakery_data()