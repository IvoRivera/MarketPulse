import pandas as pd
import numpy as np
from pathlib import Path

# =========================
# CONFIGURACIÓN
# =========================
RAW_PATH = Path("data/raw/raw_market_data.csv")
OUTPUT_PATH = Path("data/processed/clean_market_data.csv")


# =========================
# CARGA DE DATOS
# =========================
def load_data(path: Path) -> pd.DataFrame:
    """
    Carga el dataset crudo.
    """
    print("📥 Cargando datos...")
    df = pd.read_csv(path, parse_dates=["date"])
    print(f"Registros cargados: {len(df)}")
    return df


# =========================
# LIMPIEZA DE NULOS
# =========================
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Manejo de valores nulos y críticos.
    """
    print("\n🧹 Manejo de valores nulos...")

    initial_count = len(df)

    # Eliminamos registros sin información crítica
    df = df.dropna(subset=["date", "product_id"])

    # Imputaciones
    df["raw_price"] = df["raw_price"].fillna(df["raw_price"].median())
    df["units_sold"] = df["units_sold"].fillna(0)

    dropped = initial_count - len(df)
    print(f"Registros eliminados: {dropped}")

    return df


# =========================
# FEATURE ENGINEERING BASE
# =========================
def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera variables temporales útiles para análisis.
    """
    print("\n🧠 Generando variables de tiempo...")

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day_of_week"] = df["date"].dt.day_name()

    return df


# =========================
# DETECCIÓN DE OUTLIERS
# =========================
def diagnostic_outliers(df: pd.DataFrame, year_sample: int = 2025):
    """
    Diagnóstico simple de outliers por producto.
    """
    print("\n🔍 Diagnóstico de outliers...")

    sample = df[df["year"] == year_sample]

    for prod_id in sample["product_id"].unique():
        subset = sample[sample["product_id"] == prod_id]
        prices = subset["raw_price"]

        q1, q3 = prices.quantile([0.25, 0.75])
        iqr = q3 - q1

        upper = q3 + 1.5 * iqr
        lower = q1 - 1.5 * iqr

        outliers = ((prices > upper) | (prices < lower)).sum()
        pct = (outliers / len(prices)) * 100

        product_name = subset["product_name"].iloc[0]

        print(f"{product_name}: {pct:.2f}% outliers")


# =========================
# WINSORIZACIÓN
# =========================
def winsorize_series(series: pd.Series) -> pd.Series:
    """
    Aplica winsorización al 1% - 99%.
    """
    lower = series.quantile(0.01)
    upper = series.quantile(0.99)
    return series.clip(lower, upper)


def apply_winsorization(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica limpieza de precios agrupado por año y producto.
    """
    print("\n⚙️ Aplicando winsorización...")

    df["clean_price"] = (
        df.groupby(["year", "product_id"])["raw_price"]
        .transform(winsorize_series)
    )

    return df


# =========================
# TIPADO Y NORMALIZACIÓN
# =========================
def normalize_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajusta tipos de datos y formatos.
    """
    print("\n🔧 Normalizando tipos...")

    df["raw_price"] = df["raw_price"].round(0).astype(int)
    df["clean_price"] = df["clean_price"].round(0).astype(int)
    df["units_sold"] = df["units_sold"].astype(int)

    return df


# =========================
# MÉTRICAS DE CALIDAD
# =========================
def compute_quality_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera métricas de impacto de limpieza.
    """
    print("\n📊 Calculando métricas de calidad...")

    df["price_diff"] = df["raw_price"] - df["clean_price"]

    total_error = df["price_diff"].abs().sum()
    print(f"Distorsión total corregida: ${total_error:,} CLP")

    return df


# =========================
# GUARDADO
# =========================
def save_data(df: pd.DataFrame, path: Path):
    """
    Guarda dataset procesado.
    """
    print("\n💾 Guardando dataset limpio...")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Archivo guardado en: {path}")


# =========================
# PIPELINE PRINCIPAL
# =========================
def run_pipeline():
    """
    Ejecuta todo el pipeline de limpieza.
    """
    df = load_data(RAW_PATH)
    df = handle_missing_values(df)
    df = add_time_features(df)

    diagnostic_outliers(df)

    df = apply_winsorization(df)
    df = normalize_types(df)
    df = compute_quality_metrics(df)

    save_data(df, OUTPUT_PATH)

    print("\n✅ Pipeline completado con éxito.")


# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    run_pipeline()

