SELECT
  date,
  product_id,
  SUM(units_sold) AS daily_units,
  AVG(SUM(units_sold)) OVER (
    PARTITION BY product_id
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS rolling_7d_units
FROM read_csv_auto('data/processed/final_dataset.csv')
GROUP BY date, product_id
ORDER BY product_id, date;