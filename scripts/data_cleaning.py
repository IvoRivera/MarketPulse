import pandas as pd
import numpy as np

def clean_market_data():
    # 1. Cargar datos
    df = pd.read_csv('data/raw_market_data.csv')
    print(f"Datos cargados: {len(df)} registros.")

    # 2. Manejo de Nulos (Imputación)
    # En lugar de borrar, llenamos las unidades vacías con la mediana
    null_count = df['units_sold'].isnull().sum()
    df['units_sold'] = df['units_sold'].fillna(df['units_sold'].median())
    print(f"Se imputaron {null_count} valores nulos en 'units_sold'.")

    # 3. Winsorización de Precios (Tratamiento de Outliers)
    # Calculamos los percentiles 5 y 95
    lower_bound = df['raw_price'].quantile(0.05)
    upper_bound = df['raw_price'].quantile(0.95)
    
    # Aplicamos el "recorte": lo que esté fuera de ese rango se ajusta al límite
    df['clean_price'] = df['raw_price'].clip(lower=lower_bound, upper=upper_bound)
    print(f"Winsorización aplicada: Límites [{lower_bound:.2f} - {upper_bound:.2f}]")

    # 4. Guardar el archivo limpio
    df.to_csv('data/clean_market_data.csv', index=False)
    print("Archivo data/clean_market_data.csv generado con éxito.")

if __name__ == "__main__":
    clean_market_data()