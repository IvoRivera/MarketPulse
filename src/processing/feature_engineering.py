import pandas as pd
from pathlib import Path

# =========================
# CONFIG
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]
SALES_PATH = BASE_DIR / "data/processed/clean_market_data.csv"
WEATHER_PATH = BASE_DIR / "data/raw/weather_data.csv"
OUTPUT_PATH = BASE_DIR / "data/processed/final_dataset.csv"

# =========================
# LOAD
# =========================
def load_data():
    print("📥 Cargando datasets...")

    sales = pd.read_csv(SALES_PATH, parse_dates=["date"])
    weather = pd.read_csv(WEATHER_PATH, parse_dates=["date"])

    print(f"Ventas: {sales.shape[0]} registros, {sales.shape[1]} columnas")
    print(f"Clima: {weather.shape[0]} registros, {weather.shape[1]} columnas")

    return sales, weather


# =========================
# PREPARACIÓN
# =========================
def prepare_data(sales, weather):
    print("\n🔧 Preparando datos para merge...")

    # Asegurar formato comparable
    sales["date"] = pd.to_datetime(sales["date"]).dt.date
    weather["date"] = pd.to_datetime(weather["date"]).dt.date

    return sales, weather


# =========================
# MERGE
# =========================
def merge_data(sales, weather):
    print("\n🔗 Uniendo ventas con clima...")

    df = pd.merge(sales, weather, on="date", how="left")

    missing_weather = df["temperature"].isna().sum()
    print(f"Registros sin clima: {missing_weather}")

    print(f"Dataset final: {df.shape}")
    return df


# =========================
# FEATURE ENGINEERING
# =========================
def create_features(df):
    print("\n🧠 Creando variables nuevas...")

    # Revenue
    df["revenue"] = df["clean_price"] * df["units_sold"]

    # Día lluvioso (1/0)
    df["is_rainy"] = (df["precipitation"] > 0).astype(int)

    # Categoría de temperatura
    def temp_category(temp):
        if pd.isna(temp):
            return None
        elif temp < 10:
            return "frío"
        elif temp < 20:
            return "templado"
        else:
            return "caluroso"

    df["temp_category"] = df["temperature"].apply(temp_category)

    # Fin de semana (si existe columna day_of_week)
    if "day_of_week" in df.columns:
        df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])

    # Rolling promedio 7 días por producto
    if "product_id" in df.columns:
        df = df.sort_values("date")
        df["rolling_7d_units"] = (
            df.groupby("product_id")["units_sold"]
            .transform(lambda x: x.rolling(7, min_periods=1).mean())
        )

    return df


# =========================
# VALIDACIÓN
# =========================
def validate_data(df):
    print("\n🔍 Validando dataset...")

    nulls = df.isna().sum()
    if nulls.sum() > 0:
        print("\nValores nulos por columna:")
        print(nulls[nulls > 0])

    print(f"\nShape final: {df.shape}")


# =========================
# SAVE
# =========================
def save_data(df):
    print("\n💾 Guardando dataset final...")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Dataset final guardado en: {OUTPUT_PATH}")


# =========================
# PIPELINE
# =========================
def run_pipeline():
    sales, weather = load_data()
    sales, weather = prepare_data(sales, weather)
    df = merge_data(sales, weather)
    df = create_features(df)
    validate_data(df)
    save_data(df)

    print("\n✅ Feature engineering completado.")


if __name__ == "__main__":
    run_pipeline()


