SELECT
    product_id,
    product_name,
    category,

    SUM(revenue) AS total_revenue,
    SUM(units_sold) AS total_units,

    RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank,

    RANK() OVER (
        PARTITION BY category
        ORDER BY SUM(revenue) DESC
    ) AS category_rank

FROM read_csv_auto('data/processed/final_dataset.csv')

GROUP BY product_id, product_name, category
ORDER BY revenue_rank;