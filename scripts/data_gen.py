import pandas as pd
import numpy as np
import os

def generate_market_data(records=10000):
    np.random.seed(42)
    
    data = {
        'date': pd.date_range(start='2025-01-01', periods=records, freq='h'),
        'product_id': np.random.randint(100, 110, size=records),
        'raw_price': np.random.normal(150, 20, size=records),
        'units_sold': np.random.randint(1, 50, size=records)
    }
    
    df = pd.DataFrame(data)
    
    # Inyectar Outliers (el "ruido" que limpiarás mañana)
    # Precios erróneos de "12 millones" o negativos
    outlier_indices = np.random.choice(df.index, size=50, replace=False)
    df.loc[outlier_indices, 'raw_price'] = df.loc[outlier_indices, 'raw_price'] * 1000
    
    # Valores nulos
    null_indices = np.random.choice(df.index, size=100, replace=False)
    df.loc[null_indices, 'units_sold'] = np.nan
    
    # Guardar
    if not os.path.exists('data'): os.makedirs('data')
    df.to_csv('data/raw_market_data.csv', index=False)
    print("✅ Archivo data/raw_market_data.csv generado con éxito.")

if __name__ == "__main__":
    generate_market_data()