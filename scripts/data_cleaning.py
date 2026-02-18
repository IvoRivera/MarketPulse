import pandas as pd
import numpy as np

def clean_bakery_data():
    # 1. Cargar datos crudos
    df = pd.read_csv('data/raw_market_data.csv', parse_dates=['date'])
    df['year'] = df['date'].dt.year
    print(f"Iniciando pipeline para {len(df)} registros (2016-2026).")

    # --- BLOQUE DE DIAGNÓSTICO (Data Profiling) ---
    print("\nDIAGNÓSTICO PRE-LIMPIEZA:")
    # Analizamos una muestra (ej. el último año completo) para entender la dispersión
    sample_year = 2025
    diagnostic_sample = df[df['year'] == sample_year]
    
    for prod_id in diagnostic_sample['product_id'].unique():
        p_name = diagnostic_sample[diagnostic_sample['product_id'] == prod_id]['product_name'].iloc[0]
        prices = diagnostic_sample[diagnostic_sample['product_id'] == prod_id]['raw_price']
        
        # Cálculo de IQR (Interquartile Range)
        q1, q3 = prices.quantile([0.25, 0.75])
        iqr = q3 - q1
        upper_fence = q3 + 1.5 * iqr
        lower_fence = q1 - 1.5 * iqr
        
        outliers_count = ((prices > upper_fence) | (prices < lower_fence)).sum()
        pct_outliers = (outliers_count / len(prices)) * 100
        
        print(f"  • {p_name}: {outliers_count} anomalías detectadas ({pct_outliers:.1f}%)")
    # -----------------------------------------------

    # 2. Winsorización Agrupada (Tratamiento de Anomalías)
    # Ajustamos el percentil basado en el diagnóstico anterior (usaremos 1.5% para cubrir el error)
    def apply_winsor(group):
        # Al usar 0.01 y 0.99, cubrimos un 2% total de limpieza, ideal para el 1.5% de error inyectado
        lower = group.quantile(0.01)
        upper = group.quantile(0.99)
        return group.clip(lower=lower, upper=upper)

    print("\nAplicando Winsorización agrupada por año y producto...")
    df['clean_price'] = df.groupby(['year', 'product_id'])['raw_price'].transform(apply_winsor)

    # 3. Refinamiento y Tipado (Estándar Chile CLP)
    df['raw_price'] = df['raw_price'].round(0).astype(int)
    df['clean_price'] = df['clean_price'].round(0).astype(int)
    df['units_sold'] = df['units_sold'].astype(int)

    # 4. Métricas de Impacto para Power BI
    df['price_diff'] = df['raw_price'] - df['clean_price']
    total_error = df['price_diff'].abs().sum()
    
    # 5. Guardado de Producción
    df.to_csv('data/clean_market_data.csv', index=False)
    
    print(f"\nLimpieza completada.")
    print(f"Máximo original: ${df['raw_price'].max():,} | Máximo limpio: ${df['clean_price'].max():,}")
    print(f"Distorsión total corregida: ${total_error:,} CLP.")

if __name__ == "__main__":
    clean_bakery_data()