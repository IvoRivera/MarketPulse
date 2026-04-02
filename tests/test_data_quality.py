import pandas as pd

DATA_PATH = "data/processed/final_dataset.csv"


def load_data():
    return pd.read_csv(DATA_PATH, parse_dates=["date"])


def test_dataset_not_empty():
    df = load_data()
    assert len(df) > 0, "El dataset está vacío"


def test_no_nulls_in_key_columns():
    df = load_data()

    assert df["date"].isna().sum() == 0, "Nulos en date"
    assert df["product_id"].isna().sum() == 0, "Nulos en product_id"
    assert df["clean_price"].isna().sum() == 0, "Nulos en clean_price"


def test_revenue_positive():
    df = load_data()

    assert (df["revenue"] >= 0).all(), "Hay revenue negativo"


def test_weather_coverage():
    df = load_data()

    null_ratio = df["temperature"].isna().mean()
    assert null_ratio < 0.01, f"Demasiados nulos en clima: {null_ratio}"


def test_units_non_negative():
    df = load_data()

    assert (df["units_sold"] >= 0).all(), "Hay ventas negativas"


def test_price_consistency():
    df = load_data()

    diff = (df["raw_price"] - df["clean_price"]).abs().mean()
    assert diff < 10000, f"Diferencia promedio de precios muy alta: {diff}"


def test_date_range():
    df = load_data()

    min_date = df["date"].min()
    max_date = df["date"].max()

    assert min_date < max_date, "Rango de fechas inválido"


def test_categories_not_empty():
    df = load_data()

    assert df["category"].nunique() > 0, "No hay categorías"


def test_rolling_feature_exists():
    df = load_data()

    assert "rolling_7d_units" in df.columns, "Falta feature rolling"