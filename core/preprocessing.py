from typing import Tuple

import pandas as pd

from config.settings import REQUIRED_COLUMNS


def validate_data(df: pd.DataFrame) -> Tuple[bool, list[str]]:
    messages = []

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        messages.append(f"Missing required columns: {', '.join(missing_columns)}")
        return False, messages

    if df.empty:
        messages.append("Uploaded file is empty.")
        return False, messages

    return True, messages


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = df.copy()

    clean_df["Date"] = pd.to_datetime(clean_df["Date"], errors="coerce")
    clean_df["Sales"] = pd.to_numeric(clean_df["Sales"], errors="coerce")
    clean_df["Quantity"] = pd.to_numeric(clean_df["Quantity"], errors="coerce")
    clean_df["Price"] = pd.to_numeric(clean_df["Price"], errors="coerce")

    clean_df = clean_df.dropna(subset=["Date", "Sales", "Quantity", "Price", "Product", "Category"])

    clean_df = clean_df[clean_df["Sales"] >= 0]
    clean_df = clean_df[clean_df["Quantity"] >= 0]
    clean_df = clean_df[clean_df["Price"] >= 0]

    clean_df["Product"] = clean_df["Product"].astype(str).str.strip()
    clean_df["Category"] = clean_df["Category"].astype(str).str.strip()

    clean_df = clean_df.sort_values("Date").reset_index(drop=True)

    return clean_df


def get_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    daily = df.groupby("Date", as_index=False)["Sales"].sum()
    daily = daily.sort_values("Date").reset_index(drop=True)
    return daily


def create_features(daily_df: pd.DataFrame) -> pd.DataFrame:
    feature_df = daily_df.copy()

    feature_df["Day"] = feature_df["Date"].dt.day
    feature_df["Month"] = feature_df["Date"].dt.month
    feature_df["Year"] = feature_df["Date"].dt.year
    feature_df["DayOfWeek"] = feature_df["Date"].dt.dayofweek
    feature_df["DayOfYear"] = feature_df["Date"].dt.dayofyear
    feature_df["WeekOfYear"] = feature_df["Date"].dt.isocalendar().week.astype(int)
    feature_df["Quarter"] = feature_df["Date"].dt.quarter
    feature_df["IsWeekend"] = feature_df["DayOfWeek"].isin([5, 6]).astype(int)

    return feature_df
