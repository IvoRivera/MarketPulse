SELECT
  product_name,
  SUM(revenue) AS total_revenue,
  SUM(units_sold) AS total_units
FROM read_csv_auto('data/processed/final_dataset.csv')
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;