import pandas as pd
from pathlib import Path

# =========================
# CONFIG
# =========================
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = BASE_DIR / "data/processed/final_dataset.csv"
OUTPUT_DIR = BASE_DIR / "data/processed/data_model"


# =========================
# LOAD
# =========================
def load_data():
    print("📥 Cargando dataset final...")
    df = pd.read_csv(INPUT_PATH, parse_dates=["date"])
    print(f"Shape: {df.shape}")
    return df


# =========================
# DIMENSIONS
# =========================
def create_dim_product(df):
    print("📦 Creando dim_product...")
    dim = df[["product_id", "product_name", "category"]].drop_duplicates()

    # Tipos correctos
    dim = dim.astype({
        "product_id": "int64",
        "product_name": "string",
        "category": "string"
    })
    return dim


def create_dim_date(df):
    print("📅 Creando dim_date...")
    dim = df[["date", "year", "month", "day_of_week", "is_weekend"]].drop_duplicates()

    dim = dim.astype({
        "year": "int64",
        "month": "int64",
        "day_of_week": "string",
        "is_weekend": "bool"
    })
    return dim


def create_dim_weather(df):
    print("🌦 Creando dim_weather...")
    dim = df[[
        "date",
        "temperature",
        "precipitation",
        "is_rainy",
        "temp_category"
    ]].drop_duplicates()

    dim = dim.astype({
        "temperature": "float64",
        "precipitation": "float64",
        "is_rainy": "bool",
        "temp_category": "string"
    })
    return dim


# =========================
# FACT TABLE
# =========================
def create_fact_sales(df):
    print("🧾 Creando fact_sales...")

    fact = df[[
        "date",
        "product_id",
        "units_sold",
        "revenue",
        "clean_price",
        "unit_cost",
        "rolling_7d_units"
    ]]

    fact = fact.astype({
        "product_id": "int64",
        "units_sold": "int64",
        "revenue": "float64",
        "clean_price": "float64",
        "unit_cost": "float64",
        "rolling_7d_units": "float64"
    })
    return fact


# =========================
# SAVE
# =========================
def save_table(df, name):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"💾 Guardado: {path}")


# =========================
# PIPELINE
# =========================
def run_modeling():
    df = load_data()

    dim_product = create_dim_product(df)
    dim_date = create_dim_date(df)
    dim_weather = create_dim_weather(df)
    fact_sales = create_fact_sales(df)

    save_table(dim_product, "dim_product")
    save_table(dim_date, "dim_date")
    save_table(dim_weather, "dim_weather")
    save_table(fact_sales, "fact_sales")

    print("\n✅ Data modeling completado.")


if __name__ == "__main__":
    run_modeling()
