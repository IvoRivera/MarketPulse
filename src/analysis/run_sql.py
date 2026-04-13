import duckdb
from pathlib import Path

# =========================
# CONFIG
# =========================
BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_PATH = BASE_DIR / "data/processed/sql_outputs"

QUERY_MAP = {
    "sales_by_day": BASE_DIR / "src/sql/sales_by_day.sql",
    "top_products": BASE_DIR / "src/sql/top_products.sql",
    "rolling_avg": BASE_DIR / "src/sql/rolling_avg.sql",
    "product_ranking": BASE_DIR / "src/sql/product_ranking.sql",
}

QUERY_NAME = "product_ranking" # Cambiar para ejecutar query deseada
QUERY_PATH = QUERY_MAP[QUERY_NAME]


# =========================
# RUN QUERY
# =========================
def run_query(query_path: Path):
  print("🧠 Ejecutando query SQL...")

  with open(query_path, "r") as f:
    query = f.read()

  df = duckdb.query(query).to_df()

  print("\n📊 Resultado:")
  print(df.head())
  print(f"\nFilas totales: {len(df)}")

  return df


# =========================
# SAVE RESULT
# =========================
def save_result(df, query_name: str):
  OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

  path = OUTPUT_PATH / f"{query_name}.csv"
  df.to_csv(path, index=False)

  print(f"💾 Resultado guardado en {path}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
  result_df = run_query(QUERY_PATH)
  save_result(result_df, QUERY_NAME)