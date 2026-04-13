import pandas as pd
from pathlib import Path

# =========================
# PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parents[2]

FINAL_DATA = BASE_DIR / "data/processed/final_dataset.csv"
SQL_OUTPUTS = BASE_DIR / "data/processed/sql_outputs"


# =========================
# UTIL
# =========================
def compare_dataframes(df1, df2, cols):
    diff = {}

    for col in cols:
        diff[col] = (df1[col] - df2[col]).abs().sum()

    return diff


# =========================
# VALIDACIONES
# =========================
def validate_sales_by_day():
    print("\n🔍 Validando: sales_by_day")

    df = pd.read_csv(FINAL_DATA, parse_dates=["date"])

    python_df = (
        df.groupby("date")
        .agg(
            total_revenue=("revenue", "sum"),
            total_units=("units_sold", "sum")
        )
        .reset_index()
    )

    sql_df = pd.read_csv(SQL_OUTPUTS / "sales_by_day.csv", parse_dates=["date"])

    merged = python_df.merge(sql_df, on="date", suffixes=("_py", "_sql"))

    diff = compare_dataframes(
        merged,
        merged.rename(columns={
            "total_revenue_sql": "total_revenue",
            "total_units_sql": "total_units"
        }),
        ["total_revenue_py", "total_units_py"]
    )

    revenue_diff = (merged["total_revenue_py"] - merged["total_revenue_sql"]).abs().sum()
    units_diff = (merged["total_units_py"] - merged["total_units_sql"]).abs().sum()

    print(f"💰 Revenue diff: {revenue_diff}")
    print(f"📦 Units diff: {units_diff}")

    return revenue_diff == 0 and units_diff == 0


def validate_top_products():
    print("\n🔍 Validando: top_products")

    df = pd.read_csv(FINAL_DATA)

    python_df = (
        df.groupby("product_name")
        .agg(
            total_revenue=("revenue", "sum")
        )
        .sort_values("total_revenue", ascending=False)
        .head(10)
        .reset_index()
    )

    sql_df = pd.read_csv(SQL_OUTPUTS / "top_products.csv")

    # comparación básica
    match = set(python_df["product_name"]) == set(sql_df["product_name"])

    print(f"📊 Coincidencia de productos top: {match}")

    return match


# =========================
# MAIN
# =========================
def run_all_validations():
    print("\n🚀 Ejecutando validaciones SQL vs Python...")

    results = {
        "sales_by_day": validate_sales_by_day(),
        "top_products": validate_top_products(),
    }

    print("\n📋 RESULTADOS:")
    for k, v in results.items():
        print(f"{k}: {'✅ OK' if v else '❌ ERROR'}")

    if all(results.values()):
        print("\n🎯 VALIDACIÓN COMPLETA EXITOSA")
    else:
        print("\n⚠️ HAY PROBLEMAS EN LAS VALIDACIONES")


if __name__ == "__main__":
    run_all_validations()