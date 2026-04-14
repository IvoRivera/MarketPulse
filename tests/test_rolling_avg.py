
import pandas as pd

df = pd.read_csv("data/processed/final_dataset.csv")

print(df["rolling_7d_units"].head())
print(df["rolling_7d_units"].describe())