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


def page_analysis() -> None:
    hero(
        "Sales Analysis",
        "Explore product, category, monthly sales and quantity patterns using interactive filters and charts.",
        ["Filters", "Top Products", "Monthly Trends", "Category Analysis"],
    )

    if st.session_state.clean_data is None:
        warning("No dataset loaded. Please upload CSV data from Upload Data page first.")
        return

    df = st.session_state.clean_data.copy()

    with st.sidebar:
        st.markdown("---")
        st.subheader("Analysis Filters")

        categories = sorted(df["Category"].unique().tolist())
        selected_categories = st.multiselect(
            "Category",
            categories,
            default=categories,
        )

        products = sorted(df["Product"].unique().tolist())
        selected_products = st.multiselect(
            "Product",
            products,
            default=products,
        )

    filtered = df[
        (df["Category"].isin(selected_categories))
        & (df["Product"].isin(selected_products))
    ]

    if filtered.empty:
        warning("No records found for selected filters.")
        return

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi("Filtered Revenue", format_currency(filtered["Sales"].sum()), "Current filter")
    with c2:
        kpi("Filtered Rows", format_number(len(filtered)), "Visible records")
    with c3:
        kpi("Avg Order Value", format_currency(filtered["Sales"].mean()), "Average per row")
    with c4:
        kpi("Total Quantity", format_number(filtered["Quantity"].sum()), "Units sold")

    tab1, tab2, tab3 = st.tabs(["Trend Analysis", "Product Analysis", "Data Table"])

    with tab1:
        daily_filtered = get_daily_sales(filtered)
        c5, c6 = st.columns(2)

        with c5:
            st.plotly_chart(daily_sales_chart(daily_filtered), use_container_width=True)

        with c6:
            st.plotly_chart(monthly_sales_chart(filtered), use_container_width=True)

    with tab2:
        c7, c8 = st.columns(2)

        with c7:
            st.plotly_chart(category_sales_chart(filtered), use_container_width=True)

        with c8:
            st.plotly_chart(product_sales_chart(filtered), use_container_width=True)

    with tab3:
        st.dataframe(filtered.sort_values("Date", ascending=False), use_container_width=True)

        st.download_button(
            "Download Filtered Data",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="filtered_sales_data.csv",
            mime="text/csv",
            use_container_width=True,
        )
