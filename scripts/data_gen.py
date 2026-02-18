import pandas as pd
import numpy as np
import os

def generate_market_data(records=10000):
    np.random.seed(42)
    
    data = {
        'date': pd.date_range(start='2025-01-01', periods=records, freq='h'),
        'product_id': np.random.randint(100, 110, size=records),
        # Precios base realistas entre $5.000 y $50.000 CLP
        'raw_price': np.random.uniform(5000, 50000, size=records),
        'units_sold': np.random.randint(1, 20, size=records)
    }
    
    df = pd.DataFrame(data)
    
    # Inyectar Outliers sutiles (x10 en lugar de x1000)
    # Esto permite que el Box Plot muestre puntos fuera, pero sin romper el eje Y
    outlier_indices = np.random.choice(df.index, size=50, replace=False)
    df.loc[outlier_indices, 'raw_price'] = df.loc[outlier_indices, 'raw_price'] * 10
    
    # Valores nulos para limpiar después
    null_indices = np.random.choice(df.index, size=100, replace=False)
    df.loc[null_indices, 'units_sold'] = np.nan
    
    #guardar csv
    if not os.path.exists('data'): os.makedirs('data')
    df.to_csv('data/raw_market_data.csv', index=False)
    print("✅ Datos reseteados con éxito. Ahora son realistas.")

if __name__ == "__main__":
    generate_market_data()