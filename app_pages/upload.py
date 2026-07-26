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


def page_upload() -> None:
    hero(
        "Upload & Validate Sales Data",
        "Upload your CSV file, preview it first, then manually apply it as the active dataset. You can also load the built-in sample dataset for quick testing.",
        ["CSV Validation", "Manual Apply", "Sample Dataset", "Cleaned Preview", "Download Output"],
    )

    st.subheader("Required CSV Columns")

    required_df = pd.DataFrame(
        {
            "Column": REQUIRED_COLUMNS,
            "Description": [
                "Sales transaction date",
                "Product name",
                "Product category",
                "Revenue / Sales amount",
                "Quantity sold",
                "Product price",
            ],
        }
    )

    st.dataframe(required_df, hide_index=True, use_container_width=True)

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.subheader("Upload CSV File")
        st.write("Select a CSV file first. It will not be applied until you click the button below.")

        uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)

                st.session_state.pending_upload_data = uploaded_df.copy()
                st.session_state.pending_upload_name = uploaded_file.name

                success(f"{uploaded_file.name} selected successfully. Review preview below, then click Apply Uploaded Dataset.")

                st.markdown("#### Uploaded File Preview")
                st.dataframe(uploaded_df.head(10), use_container_width=True)

                valid, messages = validate_data(uploaded_df)

                if valid:
                    success("CSV structure is valid. Required columns are available.")

                    if st.button("Apply Uploaded Dataset", use_container_width=True):
                        if store_data(uploaded_df, uploaded_file.name, is_sample=False):
                            success(f"{uploaded_file.name} applied successfully as active dataset.")

                            st.session_state.pending_upload_data = None
                            st.session_state.pending_upload_name = None

                else:
                    for msg in messages:
                        error(msg)

            except Exception as ex:
                error(f"Unable to read uploaded file: {ex}")

    with right:
        st.subheader("Use Sample Dataset")
        st.write("Use this only if you want to test the dashboard quickly.")

        info(
            "<b>Note:</b><br>"
            "Sample data will load only when you click the button. It will not automatically replace uploaded data."
        )

        if st.button("Load Sample Dataset", use_container_width=True):
            try:
                sample_df = get_sample_dataset_for_button()

                if store_data(sample_df, "sample_sales_data.csv", is_sample=True):
                    success("Sample dataset loaded successfully and set as active dataset.")

            except Exception as ex:
                error(f"Unable to load sample dataset: {ex}")

        st.markdown("#### Sample Format")

        sample_format = pd.DataFrame(
            {
                "Date": ["2024-01-01", "2024-01-02"],
                "Product": ["Laptop", "Mouse"],
                "Category": ["Electronics", "Accessories"],
                "Sales": [55000, 1600],
                "Quantity": [1, 2],
                "Price": [55000, 800],
            }
        )

        st.dataframe(sample_format, hide_index=True, use_container_width=True)

    st.markdown("---")

    if st.session_state.clean_data is not None:
        st.subheader("Active Cleaned Dataset Preview")

        df = st.session_state.clean_data

        dataset_type = "Sample Dataset" if st.session_state.is_sample_data else "Uploaded Dataset"

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            kpi("Rows", format_number(len(df)), "After cleaning")
        with c2:
            kpi("Products", format_number(df["Product"].nunique()), "Unique products")
        with c3:
            kpi("Categories", format_number(df["Category"].nunique()), "Unique categories")
        with c4:
            kpi("Missing Values", format_number(df.isna().sum().sum()), "After preprocessing")

        info(
            f"<b>Active Dataset:</b> {st.session_state.source_name}<br>"
            f"<b>Dataset Type:</b> {dataset_type}<br>"
            f"<b>Date Range:</b> {df['Date'].min().strftime('%d %b %Y')} - {df['Date'].max().strftime('%d %b %Y')}"
        )

        st.dataframe(df.head(30), use_container_width=True)

        st.download_button(
            "Download Cleaned Data",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="cleaned_sales_data.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        warning("No active dataset yet. Upload a CSV file and click Apply Uploaded Dataset, or click Load Sample Dataset.")
