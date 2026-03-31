import pandas as pd
from pathlib import Path

# =========================
# PATHS
# =========================
SALES_PATH = Path("data/processed/clean_market_data.csv")
WEATHER_PATH = Path("data/raw/weather_data.csv")
OUTPUT_PATH = Path("data/processed/final_dataset.csv")


# =========================
# CARGA DE DATOS
# =========================
def load_data():
    print("📥 Cargando datasets...")

    sales = pd.read_csv(SALES_PATH, parse_dates=["date"])
    weather = pd.read_csv(WEATHER_PATH, parse_dates=["date"])

    print(f"Ventas: {len(sales)} registros")
    print(f"Clima: {len(weather)} registros")

    return sales, weather


# =========================
# MERGE
# =========================
def merge_data(sales, weather):
    print("\n🔗 Uniendo ventas con clima...")

    df = pd.merge(sales, weather, on="date", how="left")

    missing_weather = df["temperature"].isna().sum()
    print(f"Registros sin clima: {missing_weather}")

    return df


# =========================
# FEATURE ENGINEERING
# =========================
def create_features(df):
    print("\n🧠 Creando variables nuevas...")

    # Día lluvioso (1/0)
    df["is_rainy"] = (df["precipitation"] > 0).astype(int)

    # Categoría de temperatura
    def temp_category(temp):
        if temp < 10:
            return "frío"
        elif temp < 20:
            return "templado"
        else:
            return "caluroso"

    df["temp_category"] = df["temperature"].apply(temp_category)

    # Ventas totales por fila
    df["revenue"] = df["clean_price"] * df["units_sold"]

    return df


# =========================
# GUARDADO
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
    df = merge_data(sales, weather)
    df = create_features(df)
    save_data(df)

    print("\n✅ Feature engineering completado.")


if __name__ == "__main__":
    run_pipeline()