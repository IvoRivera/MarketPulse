import pandas as pd
import numpy as np

def clean_market_data():
    # 1. Cargar datos
    df = pd.read_csv('data/raw_market_data.csv')
    print(f"Datos cargados: {len(df)} registros.")

    # 2. Manejo de Nulos (Imputación)
    # Llenamos nulos con la mediana y forzamos a entero (no existen 0.5 unidades)
    null_count = df['units_sold'].isnull().sum()
    df['units_sold'] = df['units_sold'].fillna(df['units_sold'].median()).astype(int)
    print(f"Se imputaron {null_count} valores nulos en 'units_sold'.")

    # 3. Winsorización de Precios (Tratamiento de Outliers)
    lower_bound = df['raw_price'].quantile(0.05)
    upper_bound = df['raw_price'].quantile(0.95)
    
    # Aplicamos el "recorte"
    df['clean_price'] = df['raw_price'].clip(lower=lower_bound, upper=upper_bound)
    
    # --- REDONDEO Y TIPOS DE DATOS ---
    # Redondeamos a 0 decimales y convertimos a entero para representar CLP correctamente
    df['raw_price'] = df['raw_price'].round(0).astype(int)
    df['clean_price'] = df['clean_price'].round(0).astype(int)
    # ----------------------------------------------------

    print(f"Winsorización aplicada: Límites [{int(lower_bound)} - {int(upper_bound)}]")
    print("Precios y unidades convertidos a números enteros.")

    # 4. Guardar el archivo limpio
    df.to_csv('data/clean_market_data.csv', index=False)
    print("Archivo data/clean_market_data.csv generado con éxito.")

if __name__ == "__main__":
    clean_market_data()