import pandas as pd
import plotly.express as px
import streamlit as st

from config.settings import CURRENCY, REQUIRED_COLUMNS
from core.charts import (
    actual_predicted_chart,
    apply_layout,
    category_sales_chart,
    daily_sales_chart,
    forecast_chart,
    monthly_sales_chart,
    product_sales_chart,
)
from core.data_loader import get_sample_dataset_for_button
from core.forecasting import forecast_sales
from core.model import load_saved_model, train_models
from core.preprocessing import get_daily_sales, validate_data
from state.session import store_data
from ui.components import (
    error,
    format_currency,
    format_number,
    hero,
    info,
    kpi,
    success,
    warning,
)


def page_home() -> None:
    hero(
        "Sales Forecasting Dashboard using Machine Learning",
        "A premium business intelligence dashboard for uploading sales data, analyzing revenue trends, training ML models, and forecasting future sales with export-ready results.",
        [
            "Revenue Intelligence",
            "Forecast Automation",
            "ML Model Comparison",
            "CSV Based Workflow",
            "Business Dashboard",
        ],
    )

    if st.session_state.clean_data is None or st.session_state.daily_sales is None:
        warning(
            "No active dataset found. Go to Upload Data page and either upload your CSV file "
            "or click Load Sample Dataset to test the dashboard."
        )

        st.subheader("Expected CSV Format")

        expected_df = pd.DataFrame(
            {
                "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "Product": ["Laptop", "Mouse", "Keyboard"],
                "Category": ["Electronics", "Accessories", "Accessories"],
                "Sales": [55000, 1600, 3000],
                "Quantity": [1, 2, 2],
                "Price": [55000, 800, 1500],
            }
        )

        st.dataframe(expected_df, hide_index=True, use_container_width=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            info("<b>Step 1:</b><br>Upload a CSV file with required sales columns.")
        with c2:
            info("<b>Step 2:</b><br>Train the ML model from Model Training page.")
        with c3:
            info("<b>Step 3:</b><br>Generate future sales forecast and download output.")

        return

    df = st.session_state.clean_data
    daily = st.session_state.daily_sales

    total_sales = df["Sales"].sum()
    avg_daily_sales = daily["Sales"].mean()
    peak_daily_sales = daily["Sales"].max()
    total_records = len(df)

    total_quantity = df["Quantity"].sum()
    avg_order_value = df["Sales"].mean()
    total_products = df["Product"].nunique()
    total_categories = df["Category"].nunique()

    best_product = df.groupby("Product")["Sales"].sum().idxmax()
    best_category = df.groupby("Category")["Sales"].sum().idxmax()

    dataset_type = "Sample Dataset" if st.session_state.is_sample_data else "Uploaded Dataset"

    st.markdown("### Executive Sales Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi("Total Revenue", format_currency(total_sales), "Overall sales amount")
    with c2:
        kpi("Avg Daily Sales", format_currency(avg_daily_sales), "Daily average revenue")
    with c3:
        kpi("Peak Daily Sales", format_currency(peak_daily_sales), "Highest one-day revenue")
    with c4:
        kpi("Total Records", format_number(total_records), "Clean transaction rows")

    c5, c6, c7, c8 = st.columns(4)

    with c5:
        kpi("Total Quantity", format_number(total_quantity), "Units sold")
    with c6:
        kpi("Avg Order Value", format_currency(avg_order_value), "Average row revenue")
    with c7:
        kpi("Products", format_number(total_products), "Unique products")
    with c8:
        kpi("Categories", format_number(total_categories), "Unique categories")

        st.markdown("---")

    st.subheader("Forecasting Workflow")

    w1, w2, w3, w4 = st.columns(4)

    with w1:
        info(
            "<b>1. Upload Data</b><br>"
            "Upload sales CSV with Date, Product, Category, Sales, Quantity and Price."
        )

    with w2:
        info(
            "<b>2. Analyze Revenue</b><br>"
            "Review daily, monthly, product-wise and category-wise sales performance."
        )

    with w3:
        info(
            "<b>3. Train Model</b><br>"
            "Train multiple ML models and select the best model using RMSE."
        )

    with w4:
        info(
            "<b>4. Forecast Sales</b><br>"
            "Generate future sales forecast and download CSV output."
        )

    st.markdown("---")

    st.subheader("Business Readiness Score")

    score_1, score_2, score_3 = st.columns(3)

    with score_1:
        kpi("Data Quality", "Ready", "Required columns validated")

    with score_2:
        model_status = "Ready" if st.session_state.model_bundle is not None else "Pending"
        kpi("Model Status", model_status, "Train model before forecast")

    with score_3:
        forecast_status = "Generated" if st.session_state.forecast_result is not None else "Pending"
        kpi("Forecast Status", forecast_status, "Generate forecast output")
    st.markdown("---")

    c9, c10 = st.columns(2)

    with c9:
        st.subheader("Category Revenue Distribution")
        st.plotly_chart(category_sales_chart(df), use_container_width=True)

    with c10:
        st.subheader("Monthly Revenue Movement")
        st.plotly_chart(monthly_sales_chart(df), use_container_width=True)

    st.markdown("---")

    st.subheader("Top Products Leaderboard")

    top_products = (
        df.groupby("Product", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Quantity=("Quantity", "sum"),
            Average_Price=("Price", "mean"),
        )
        .sort_values("Total_Sales", ascending=False)
        .head(8)
    )

    top_products["Total_Sales"] = top_products["Total_Sales"].map(lambda x: f"{CURRENCY}{x:,.2f}")
    top_products["Average_Price"] = top_products["Average_Price"].map(lambda x: f"{CURRENCY}{x:,.2f}")

    st.dataframe(top_products, hide_index=True, use_container_width=True)

    st.markdown("---")

    c11, c12, c13 = st.columns(3)

    with c11:
        info("<b>Next Action:</b><br>Go to Model Training and train/retrain the forecasting model.")
    with c12:
        info("<b>Forecasting:</b><br>After training, generate future sales forecast for 7 to 365 days.")
    with c13:
        info("<b>Submission:</b><br>Take screenshots of dashboard, training result, forecast chart and output table.")
