"""Generate model, forecast CSV and static output images for the repository.

Run from the project root:
    python scripts/generate_project_outputs.py
"""

from __future__ import annotations

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import matplotlib.pyplot as plt
import pandas as pd

from src.data_preprocessing import aggregate_daily_sales, clean_sales_data
from src.forecasting import forecast_sales, summarize_forecast
from src.model_training import train_sales_model

DATA_PATH = BASE_DIR / "data" / "sample_sales_data.csv"
MODEL_PATH = BASE_DIR / "models" / "sales_forecasting_model.pkl"
OUTPUT_DIR = BASE_DIR / "output"
SCREENSHOT_DIR = BASE_DIR / "screenshots"

OUTPUT_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR.mkdir(exist_ok=True)

raw_data = pd.read_csv(DATA_PATH)
cleaned_data = clean_sales_data(raw_data)
daily_sales = aggregate_daily_sales(cleaned_data)
training_result = train_sales_model(daily_sales, MODEL_PATH)
forecast_result = forecast_sales(training_result["model_bundle"], 30)
forecast_result.to_csv(OUTPUT_DIR / "forecast_output.csv", index=False)

metrics = training_result["metrics"]
prediction_result = training_result["prediction_result"]
summary = summarize_forecast(forecast_result)

plt.figure(figsize=(12, 6))
plt.plot(daily_sales["Date"], daily_sales["Sales"])
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(SCREENSHOT_DIR / "sales_trend.png", dpi=140)
plt.close()

category_sales = cleaned_data.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
plt.figure(figsize=(10, 6))
plt.bar(category_sales["Category"], category_sales["Sales"])
plt.title("Category-wise Sales")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(SCREENSHOT_DIR / "category_sales.png", dpi=140)
plt.close()

product_sales = cleaned_data.groupby("Product", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False).head(10)
plt.figure(figsize=(12, 6))
plt.bar(product_sales["Product"], product_sales["Sales"])
plt.title("Top Products by Sales")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(SCREENSHOT_DIR / "top_products.png", dpi=140)
plt.close()

plt.figure(figsize=(12, 6))
plt.plot(prediction_result["Date"], prediction_result["Sales"], label="Actual Sales")
plt.plot(prediction_result["Date"], prediction_result["Predicted_Sales"], label="Predicted Sales")
plt.title("Actual Sales vs Predicted Sales")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.tight_layout()
plt.savefig(SCREENSHOT_DIR / "actual_vs_predicted.png", dpi=140)
plt.close()

plt.figure(figsize=(12, 6))
plt.plot(daily_sales.tail(90)["Date"], daily_sales.tail(90)["Sales"], label="Historical Sales")
plt.plot(forecast_result["Date"], forecast_result["Predicted_Sales"], label="Forecast Sales")
plt.title("30-Day Future Sales Forecast")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.tight_layout()
plt.savefig(SCREENSHOT_DIR / "forecast_result.png", dpi=140)
plt.close()

metric_names = ["MAE", "RMSE", "R2 Score"]
metric_values = [metrics["MAE"], metrics["RMSE"], metrics["R2 Score"]]
plt.figure(figsize=(8, 5))
plt.bar(metric_names, metric_values)
plt.title("Model Performance Metrics")
plt.tight_layout()
plt.savefig(SCREENSHOT_DIR / "model_performance.png", dpi=140)
plt.close()

summary_df = pd.DataFrame([summary])
summary_df.to_csv(OUTPUT_DIR / "forecast_summary.csv", index=False)

print("Generated model, output CSV files and static output images.")
