"""Punto de entrada del pipeline: ejecuta ingesta → procesamiento → análisis SQL."""
import subprocess, sys
steps = [
    ["src/ingestion/data_gen.py"],
    ["src/ingestion/weather_api.py"],
    ["src/processing/data_cleaning.py"],
    ["src/processing/feature_engineering.py"],
    ["src/processing/data_modeling.py"],
    ["src/analysis/run_sql.py"],
]
for step in steps:
    cmd = [sys.executable] + step
    print(f"\n▶ Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=True)