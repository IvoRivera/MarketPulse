import pandas as pd
import requests
from pathlib import Path

# =========================
# CONFIG
# =========================
OUTPUT_PATH = Path("data/raw/weather_data.csv")

# Coordenadas Santiago (puedes cambiarlas después)
LAT = -33.45
LON = -70.66


# =========================
# API CALL
# =========================
def fetch_weather(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Obtiene datos históricos de clima desde Open-Meteo.
    """
    print("🌦️ Obteniendo datos climáticos...")

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_mean,precipitation_sum",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temperature": data["daily"]["temperature_2m_mean"],
        "precipitation": data["daily"]["precipitation_sum"]
    })

    df["date"] = pd.to_datetime(df["date"])

    print(f"Datos climáticos obtenidos: {len(df)} registros")

    return df


# =========================
# SAVE
# =========================
def save_weather(df: pd.DataFrame):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Archivo guardado en {OUTPUT_PATH}")


# =========================
# MAIN
# =========================

def get_date_range_from_sales(path: Path):
    """
    Obtiene el rango de fechas desde el dataset de ventas.
    """
    df = pd.read_csv(path, parse_dates=["date"])

    start_date = df["date"].min().date()
    end_date = df["date"].max().date()

    print(f"📅 Rango detectado: {start_date} → {end_date}")

    return str(start_date), str(end_date)

def run_weather_pipeline():
    sales_path = Path("data/raw/raw_market_data.csv")

    start_date, end_date = get_date_range_from_sales(sales_path)

    df = fetch_weather(start_date, end_date)
    save_weather(df)

if __name__ == "__main__":
    run_weather_pipeline()

