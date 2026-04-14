SELECT 
  p.product_id,
  p.product_name,
  p.category,
  SUM(f.revenue) AS total_revenue,
  SUM(f.units_sold) AS total_units,

  RANK() OVER (ORDER BY SUM(f.revenue) DESC) AS revenue_rank,

  RANK() OVER (
    PARTITION BY p.category 
    ORDER BY SUM(f.revenue) DESC
  ) AS category_rank

FROM read_csv_auto('data/processed/data_model/fact_sales.csv') f
JOIN read_csv_auto('data/processed/data_model/dim_product.csv') p
  ON f.product_id = p.product_id

GROUP BY p.product_id, p.product_name, p.category
ORDER BY revenue_rank;