SELECT
  product_name,
  SUM(revenue) AS total_revenue,
  RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM read_csv_auto('data/processed/final_dataset.csv')
GROUP BY product_name
ORDER BY revenue_rank;