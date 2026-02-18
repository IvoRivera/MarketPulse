import pandas as pd
import numpy as np
import os
from datetime import datetime

def generate_bakery_data():
    """ Genera un dataset realista de 10 años para una panadería """
    np.random.seed(42)
    
    # 1. Definición del Rango Temporal (10 años)
    start_date = '2016-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    records = len(date_range)
    
    # 2. Catálogo de Productos (Precios base en CLP y volumen diario promedio)
    products = [
        {'id': 101, 'name': 'Pan Marraqueta (kg)', 'base_price': 1100, 'daily_vol': 85},
        {'id': 102, 'name': 'Pan Hallulla (kg)', 'base_price': 1050, 'daily_vol': 75},
        {'id': 103, 'name': 'Empanada de Pino', 'base_price': 1200, 'daily_vol': 15},
        {'id': 104, 'name': 'Pastel de Hoja', 'base_price': 1500, 'daily_vol': 10},
        {'id': 105, 'name': 'Pan de Pascua', 'base_price': 3500, 'daily_vol': 0} # Estacional
    ]
    
    data_rows = []
    
    for current_date in date_range:
        # Cálculo de Inflación: tendencia alcista progresiva
        # n = años transcurridos desde el inicio
        years_passed = (current_date - date_range[0]).days / 365.25
        inflation_factor = 1 + (0.07 * years_passed) + (0.01 * (years_passed ** 1.6))
        
        for prod in products:
            # --- Lógica de Estacionalidad ---
            vol_multiplier = 1.0
            
            # Fiestas Patrias (Chile): Explosión de empanadas en Septiembre
            if current_date.month == 9 and 15 <= current_date.day <= 19:
                if prod['id'] == 103: vol_multiplier = 7.0
            
            # Navidad: Aparición del Pan de Pascua en Diciembre
            if current_date.month == 12:
                if prod['id'] == 105: vol_multiplier = 45.0
                
            # Fines de semana: Aumento en pastelería
            if current_date.weekday() >= 5: # Sábado o Domingo
                if prod['id'] == 104: vol_multiplier = 3.5
            
            # Generación de volumen de ventas (Distribución de Poisson)
            units = np.random.poisson(prod['daily_vol'] * vol_multiplier)
            
            if units > 0:
                # El precio final incluye inflación y una pequeña variación diaria
                price_clean = prod['base_price'] * inflation_factor
                price_with_noise = price_clean + np.random.normal(0, price_clean * 0.03)
                
                data_rows.append({
                    'date': current_date,
                    'product_id': prod['id'],
                    'product_name': prod['name'],
                    'raw_price': round(price_with_noise, 0),
                    'units_sold': units
                })

    df = pd.DataFrame(data_rows)
    
    # 3. Inyección de Anomalías (Errores de digitación manual)
    # 1.5% de los datos tendrán precios x10 o x0.1 (errores de balanza/caja)
    anomaly_idx = np.random.choice(df.index, size=int(len(df) * 0.015), replace=False)
    df.loc[anomaly_idx, 'raw_price'] = df.loc[anomaly_idx, 'raw_price'] * np.random.choice([10, 0.1])
    
    # 4. Exportar Dataset
    if not os.path.exists('data'): os.makedirs('data')
    df.to_csv('data/raw_market_data.csv', index=False)
    
    print(f"Dataset generado: {len(df)} registros.")
    print(f"Rango: {start_date} a {end_date}")

if __name__ == "__main__":
    generate_bakery_data()