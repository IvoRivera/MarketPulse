SELECT 
  d.date,
  SUM(f.revenue) AS total_revenue,
  SUM(f.units_sold) AS total_units
FROM read_csv_auto('data/processed/data_model/fact_sales.csv') f
JOIN read_csv_auto('data/processed/data_model/dim_date.csv') d
  ON f.date = d.date
GROUP BY d.date
ORDER BY d.date;