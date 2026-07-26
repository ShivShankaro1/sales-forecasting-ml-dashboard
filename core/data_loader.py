import numpy as np
import pandas as pd

from config.settings import SAMPLE_DATA_PATH


def generate_sample_data() -> pd.DataFrame:
    np.random.seed(42)

    dates = pd.date_range(start="2024-01-01", periods=730, freq="D")

    products = [
        ("Laptop", "Electronics", 55000),
        ("Smartphone", "Electronics", 30000),
        ("Headphones", "Accessories", 2500),
        ("Keyboard", "Accessories", 1500),
        ("Mouse", "Accessories", 800),
        ("Office Chair", "Furniture", 9000),
        ("Desk", "Furniture", 12000),
        ("Monitor", "Electronics", 15000),
    ]

    rows = []

    for date in dates:
        month_factor = 1.25 if date.month in [10, 11, 12] else 1.0
        weekend_factor = 1.15 if date.dayofweek in [5, 6] else 1.0

        for product, category, price in products:
            base_qty = np.random.randint(1, 8)
            quantity = max(1, int(base_qty * month_factor * weekend_factor))
            discount_noise = np.random.uniform(0.88, 1.12)
            sales = quantity * price * discount_noise

            rows.append(
                {
                    "Date": date.strftime("%Y-%m-%d"),
                    "Product": product,
                    "Category": category,
                    "Sales": round(sales, 2),
                    "Quantity": quantity,
                    "Price": price,
                }
            )

    return pd.DataFrame(rows)


def get_sample_dataset_for_button() -> pd.DataFrame:
    """
    Return sample dataset only when user clicks Load Sample Dataset.
    This does not auto-load sample data on app start or page change.
    """

    if SAMPLE_DATA_PATH.exists():
        return pd.read_csv(SAMPLE_DATA_PATH)

    sample_df = generate_sample_data()
    sample_df.to_csv(SAMPLE_DATA_PATH, index=False)
    return sample_df
