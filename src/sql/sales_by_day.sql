SELECT
  date,
  SUM(revenue) AS total_revenue,
  SUM(units_sold) AS total_units
FROM read_csv_auto('data/processed/final_dataset.csv')
GROUP BY date
ORDER BY date;