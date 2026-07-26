"""Generate sample dataset, trained model, forecast output and project images."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
SCREENSHOT_DIR = BASE_DIR / "screenshots"
MODEL_DIR = BASE_DIR / "models"

DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

np.random.seed(42)

products = [
    ("Laptop", "Electronics", 55000),
    ("Smartphone", "Electronics", 30000),
    ("Headphones", "Accessories", 2500),
    ("Keyboard", "Accessories", 1500),
    ("Mouse", "Accessories", 800),
    ("Office Chair", "Furniture", 8500),
    ("Desk", "Furniture", 12000),
    ("Monitor", "Electronics", 14000),
]

dates = pd.date_range(start="2024-01-01", periods=730, freq="D")
rows = []

for day_number, date in enumerate(dates):
    month_factor = 1 + 0.18 * np.sin(2 * np.pi * date.month / 12)
    weekend_factor = 1.20 if date.dayofweek in [5, 6] else 1.0
    trend_factor = 1 + day_number / 1800

    for product, category, price in products:
        base_quantity = {
            "Laptop": 2,
            "Smartphone": 3,
            "Headphones": 8,
            "Keyboard": 5,
            "Mouse": 7,
            "Office Chair": 2,
            "Desk": 1,
            "Monitor": 3,
        }[product]

        seasonal_quantity = base_quantity * month_factor * weekend_factor * trend_factor
        quantity = max(0, int(np.random.poisson(seasonal_quantity)))

        # Keep at least some transaction rows visible for every product over time.
        if quantity == 0 and np.random.rand() < 0.15:
            quantity = 1

        discount_factor = np.random.uniform(0.95, 1.05)
        sales = round(quantity * price * discount_factor, 2)

        rows.append(
            {
                "Date": date.strftime("%Y-%m-%d"),
                "Product": product,
                "Category": category,
                "Sales": sales,
                "Quantity": quantity,
                "Price": price,
            }
        )

sample_data = pd.DataFrame(rows)
sample_data.to_csv(DATA_DIR / "sample_sales_data.csv", index=False)
print(f"Sample dataset created: {DATA_DIR / 'sample_sales_data.csv'}")
