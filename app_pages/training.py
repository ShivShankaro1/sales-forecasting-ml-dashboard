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


def page_training() -> None:
    hero(
        "Model Training & Retraining",
        "Train multiple ML models, compare their performance and automatically save the best model for forecasting.",
        ["Linear Regression", "Random Forest", "Gradient Boosting", "Best Model Selection"],
    )

    if st.session_state.daily_sales is None:
        warning("No dataset loaded. Please upload CSV data from Upload Data page first.")
        return

    info(
        "<b>Training Logic:</b><br>"
        "The app converts dates into ML features like day, month, year, day of week, week of year and weekend flag. "
        "Then it trains multiple models and selects the model with the lowest RMSE."
    )

    c1, c2 = st.columns([1, 1])

    with c1:
        if st.button("Train / Retrain Model", use_container_width=True):
            try:
                with st.spinner("Training models..."):
                    result = train_models(st.session_state.daily_sales)
                    st.session_state.training_result = result
                    st.session_state.model_bundle = result["model_bundle"]

                success("Model trained successfully and saved inside models folder.")

            except Exception as ex:
                error(f"Training failed: {ex}")

    with c2:
        if st.button("Load Saved Model", use_container_width=True):
            try:
                model_bundle = load_saved_model()
                st.session_state.model_bundle = model_bundle
                success("Saved model loaded successfully.")

            except Exception as ex:
                error(str(ex))

    if st.session_state.training_result is not None:
        result = st.session_state.training_result
        metrics = result["metrics"]

        st.markdown("---")

        c3, c4, c5, c6 = st.columns(4)

        with c3:
            kpi("Best Model", str(metrics["Model"]), "Selected automatically")
        with c4:
            kpi("MAE", format_currency(metrics["MAE"]), "Lower is better")
        with c5:
            kpi("RMSE", format_currency(metrics["RMSE"]), "Lower is better")
        with c6:
            kpi("R² Score", f"{metrics['R2 Score']:.3f}", "Higher is better")

        left, right = st.columns(2)

        with left:
            st.subheader("Model Comparison")
            st.dataframe(result["comparison"], hide_index=True, use_container_width=True)

        with right:
            st.subheader("Actual vs Predicted")
            st.plotly_chart(actual_predicted_chart(result["best_prediction"]), use_container_width=True)

    elif st.session_state.model_bundle is not None:
        bundle = st.session_state.model_bundle

        st.subheader("Loaded Model Information")

        model_info = pd.DataFrame(
            [
                ["Model", bundle.get("model_name")],
                ["Trained On", bundle.get("trained_on")],
                ["Training Rows", bundle.get("trained_rows")],
                ["Testing Rows", bundle.get("tested_rows")],
                ["Forecast Starts After", pd.to_datetime(bundle.get("last_date")).strftime("%d %b %Y")],
            ],
            columns=["Metric", "Value"],
        )

        st.dataframe(model_info, hide_index=True, use_container_width=True)
