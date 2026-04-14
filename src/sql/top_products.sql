SELECT 
  p.product_name,
  SUM(f.revenue) AS total_revenue,
  SUM(f.units_sold) AS total_units
FROM read_csv_auto('data/processed/data_model/fact_sales.csv') f
JOIN read_csv_auto('data/processed/data_model/dim_product.csv') p
  ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC
LIMIT 10;