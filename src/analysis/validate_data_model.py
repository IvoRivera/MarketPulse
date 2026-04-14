import pandas as pd
from pathlib import Path

# =========================
# CONFIG
# =========================
BASE_DIR = Path(__file__).resolve().parents[2]

FACT_PATH = BASE_DIR / "data/processed/data_model/fact_sales.csv"
DIM_PRODUCT_PATH = BASE_DIR / "data/processed/data_model/dim_product.csv"
DIM_DATE_PATH = BASE_DIR / "data/processed/data_model/dim_date.csv"
DIM_WEATHER_PATH = BASE_DIR / "data/processed/data_model/dim_weather.csv"


# =========================
# LOAD
# =========================
def load_tables():
    fact = pd.read_csv(FACT_PATH, parse_dates=["date"])
    dim_product = pd.read_csv(DIM_PRODUCT_PATH)
    dim_date = pd.read_csv(DIM_DATE_PATH, parse_dates=["date"])
    dim_weather = pd.read_csv(DIM_WEATHER_PATH, parse_dates=["date"])

    return fact, dim_product, dim_date, dim_weather


# =========================
# VALIDATIONS
# =========================
def validate_keys(fact, dim_product, dim_date, dim_weather):
    print("\n🔑 Validando llaves...")

    # product_id
    missing_products = fact[~fact["product_id"].isin(dim_product["product_id"])]
    print(f"Productos sin match: {len(missing_products)}")

    # date en dim_date
    missing_dates = fact[~fact["date"].isin(dim_date["date"])]
    print(f"Fechas sin match en dim_date: {len(missing_dates)}")

    # date en dim_weather
    missing_weather = fact[~fact["date"].isin(dim_weather["date"])]
    print(f"Fechas sin match en dim_weather: {len(missing_weather)}")


def validate_joins(fact, dim_product, dim_date, dim_weather):
    print("\n🔗 Probando joins...")

    df = fact.merge(dim_product, on="product_id", how="left") \
             .merge(dim_date, on="date", how="left") \
             .merge(dim_weather, on="date", how="left")

    print(f"Shape después de joins: {df.shape}")

    nulls = df.isna().sum().sum()
    print(f"Nulos después de joins: {nulls}")


def validate_aggregations(fact):
    print("\n📊 Validando métricas...")

    total_revenue = fact["revenue"].sum()
    total_units = fact["units_sold"].sum()

    print(f"Revenue total: {total_revenue:,.0f}")
    print(f"Units total: {total_units:,.0f}")


# =========================
# RUN
# =========================
def run_validation():
    fact, dim_product, dim_date, dim_weather = load_tables()

    validate_keys(fact, dim_product, dim_date, dim_weather)
    validate_joins(fact, dim_product, dim_date, dim_weather)
    validate_aggregations(fact)

    print("\n✅ Validación del modelo completada.")


if __name__ == "__main__":
    run_validation()