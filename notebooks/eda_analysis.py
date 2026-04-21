# %% [1] Importaciones y Configuración Inicial
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import skew, kurtosis
import os

if not os.path.exists('reports'): os.makedirs('reports') 
print("Entorno listo.")

# %% [2] Carga de Datos y Auditoría de Integridad
# Ruta dinámica para robustez del proyecto
base_path = Path(__file__).resolve().parent.parent 
data_path = base_path / "data" / "raw_market_data.csv"

df_raw = pd.read_csv(data_path, parse_dates=['date'])
initial_count = len(df_raw)

# %% [2.1] Auditoría de Salud del Dato (Nulos + Cardinalidad)
print("🔍 REPORTE DE SALUD ESTRUCTURAL:")
print("-" * 30)

# Resumen de Nulos
null_report = df_raw.isnull().sum()
null_pct = (null_report / initial_count) * 100

# Resumen de Cardinalidad (Valores únicos)
cardinality = df_raw.nunique()

# Consolidamos en un solo DataFrame de Auditoría
audit_df = pd.DataFrame({
    'Tipo': df_raw.dtypes,
    'Nulos': null_report,
    '% Nulos': null_pct.round(2),
    'Unicos': cardinality
})
print(audit_df)

# %% [2.2] LIMPIEZA DE INTEGRIDAD REFERENCIAL
# Solo eliminamos lo estrictamente necesario para que los gráficos no fallen
df = df_raw.dropna(subset=['date', 'product_id']).copy()
dropped_count = initial_count - len(df)
print(f"\n{len(df)} registros listos para análisis visual.")
print(f"Se omitieron {dropped_count} registros ({ (dropped_count/initial_count)*100:.2f}%) para este EDA.")


# %% [3] Bloque: Perfilado de Integridad Robusto (Z-Score con MAD)
# 0. Ingeniería de fechas (Semana ISO) para estacionalidad
df['year'] = df['date'].dt.isocalendar().year
df['week'] = df['date'].dt.isocalendar().week
df['hour'] = df['date'].dt.hour
df['day_name'] = df['date'].dt.day_name()

# 1. Calculamos la Mediana
stats_ref = df.groupby(['product_id', 'year', 'week'])['raw_price']
df['mediana_semanal'] = stats_ref.transform('median')

# 2. Reemplazamos STD por MAD (Median Absolute Deviation)
# El MAD es la mediana de las distancias absolutas a la mediana.
def get_mad(x):
    return (x - x.median()).abs().median()

df['mad_semanal'] = stats_ref.transform(get_mad)

# 3. Calculamos el Z-Score Robusto
# Usamos el factor 0.6745 para que sea comparable a una desviación estándar normal
# Reemplazamos mad=0 por NaN para evitar divisiones por cero
df['z_score'] = (0.6745 * (df['raw_price'] - df['mediana_semanal'])) / df['mad_semanal'].replace(0, np.nan)
df['z_score'] = df['z_score'].fillna(0).abs()

# 4. Ranking de calidad
reporte_calidad = df.groupby(['category', 'product_name']).agg(
    total_registros=('raw_price', 'count'),
    alertas_criticas=('z_score', lambda x: (x > 3.0).sum()), # Ahora el 3.0 será real
    pct_ruido=('z_score', lambda x: (x > 3.0).mean() * 100),
    desvio_maximo_z=('z_score', 'max')
).sort_values(by='pct_ruido', ascending=False)

print("AUDITORÍA DE CALIDAD ROBUSTA (Top 10 productos con ruido real):")
print(reporte_calidad.head(10))

# %% [4] Bloque: Validación Visual de Anomalías
# 1. Identificamos los productos más "sucios" del bloque anterior automáticamente
# Tomamos los 3 primeros nombres del índice de tu reporte_calidad
productos_criticos = reporte_calidad.head(3).index.get_level_values('product_name').tolist()

# 2. Filtramos el DataFrame para estos productos y marcamos el umbral
df_viz = df[df['product_name'].isin(productos_criticos)].copy()
df_viz['es_anomalia'] = df_viz['z_score'] > 3.0

# 3. Gráfico de Dispersión: La "Nube" vs los "Disparos"
plt.figure(figsize=(14, 7))
sns.scatterplot(
    data=df_viz, 
    x='date', y='raw_price', 
    hue='es_anomalia', 
    palette={True: '#e74c3c', False: '#3498db'}, # Rojo para error, Azul para correcto
    alpha=0.6,
    edgecolor=None
)

plt.title(f'Validación Visual de Integridad: {", ".join(productos_criticos)}')
plt.xlabel('Eje Temporal (10 años)')
plt.ylabel('Precio Crudo ($ CLP)')
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(title='¿Detectado como Outlier?')
plt.show()

# 4. Boxplot de "Impacto en Escala"
# Esto demuestra cómo el outlier "estira" la realidad del producto
g = sns.FacetGrid(df_viz, col="product_name", sharey=False, height=5)
g.map_dataframe(sns.boxplot, x="es_anomalia", y="raw_price", palette='Set1', hue="es_anomalia", legend=False)
g.set_axis_labels("¿Es Outlier?", "Precio ($)")
g.set_titles("Análisis: {col_name}")
plt.tight_layout()
plt.show()

# 5. Visualización de Z-Score (La verdadera separación)
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df_viz,
    x='product_name',
    y='z_score',
    hue='product_name',
    palette='Set1',
    legend=False
)
plt.title('Separación Estadística Pura (Z-Score Robusto)')
plt.ylabel('Desviaciones respecto a la Mediana Semanal')
plt.axhline(3, color='red', linestyle='--', label='Umbral de Limpieza')
plt.legend()

plt.show()
# %%
