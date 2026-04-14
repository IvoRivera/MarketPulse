SELECT 
    f.date,
    f.product_id,
    f.units_sold AS daily_units,
    AVG(f.units_sold) OVER (
        PARTITION BY f.product_id 
        ORDER BY f.date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7d_units
FROM read_csv_auto('data/processed/data_model/fact_sales.csv') f
ORDER BY f.product_id, f.date;