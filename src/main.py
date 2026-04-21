"""Punto de entrada del pipeline: ejecuta ingesta → procesamiento → análisis SQL."""
import subprocess, sys
steps = [
    ["python", "src/ingestion/data_gen.py"],
    ["python", "src/ingestion/weather_api.py"],
    ["python", "src/processing/data_cleaning.py"],
    ["python", "src/processing/feature_engineering.py"],
    ["python", "src/processing/data_modeling.py"],
    ["python", "src/analysis/run_sql.py"],
]
for step in steps:
    print(f"\n▶ Running: {' '.join(step)}")
    result = subprocess.run(step, check=True)