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


def page_forecast() -> None:
    hero(
        "Forecast Future Sales",
        "Generate future sales forecast using the trained model and export prediction results as CSV.",
        ["7 to 365 Days", "Forecast Chart", "CSV Export", "Summary KPIs"],
    )

    if st.session_state.daily_sales is None:
        warning("No dataset loaded. Please upload CSV data from Upload Data page first.")
        return

    if st.session_state.model_bundle is None:
        try:
            st.session_state.model_bundle = load_saved_model()
        except Exception:
            warning("Please train the model first from the Model Training page.")
            return

    left, right = st.columns([0.8, 1.2])

    with left:
        st.subheader("Forecast Settings")
        forecast_days = st.slider(
            "Select forecast period in days",
            min_value=7,
            max_value=365,
            value=30,
        )

        generate = st.button("Generate Forecast", use_container_width=True)

    with right:
        bundle = st.session_state.model_bundle

        model_df = pd.DataFrame(
            [
                ["Active Model", bundle.get("model_name")],
                ["Trained On", bundle.get("trained_on")],
                ["Forecast Starts After", pd.to_datetime(bundle.get("last_date")).strftime("%d %b %Y")],
            ],
            columns=["Item", "Details"],
        )

        st.subheader("Active Model")
        st.dataframe(model_df, hide_index=True, use_container_width=True)

    if generate:
        try:
            forecast_df = forecast_sales(st.session_state.model_bundle, forecast_days)
            st.session_state.forecast_result = forecast_df
            success("Forecast generated successfully.")

        except Exception as ex:
            error(f"Forecast failed: {ex}")

    if st.session_state.forecast_result is not None:
        forecast_df = st.session_state.forecast_result

        total_forecast = forecast_df["Predicted Sales"].sum()
        avg_forecast = forecast_df["Predicted Sales"].mean()
        peak_forecast = forecast_df["Predicted Sales"].max()

        best_date = forecast_df.loc[
            forecast_df["Predicted Sales"].idxmax(),
            "Date",
        ].strftime("%d %b %Y")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            kpi("Total Forecast", format_currency(total_forecast), "Selected period")
        with c2:
            kpi("Avg Daily Forecast", format_currency(avg_forecast), "Daily expected revenue")
        with c3:
            kpi("Best Sales Date", best_date, "Highest forecast day")
        with c4:
            kpi("Peak Forecast", format_currency(peak_forecast), "Best expected day")

        st.plotly_chart(
            forecast_chart(st.session_state.daily_sales, forecast_df),
            use_container_width=True,
        )

        left2, right2 = st.columns([1.2, 0.8])

        with left2:
            st.subheader("Forecast Table")
            display_df = forecast_df.copy()
            display_df["Date"] = display_df["Date"].dt.strftime("%d %b %Y")
            display_df["Predicted Sales"] = display_df["Predicted Sales"].map(
                lambda value: f"{CURRENCY}{value:,.2f}"
            )

            st.dataframe(display_df, hide_index=True, use_container_width=True)

        with right2:
            st.subheader("Export Forecast")

            st.download_button(
                "Download Forecast CSV",
                data=forecast_df.to_csv(index=False).encode("utf-8"),
                file_name="sales_forecast_output.csv",
                mime="text/csv",
                use_container_width=True,
            )
