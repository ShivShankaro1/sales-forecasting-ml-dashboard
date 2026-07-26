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


def page_performance() -> None:
    hero(
        "Model Performance",
        "Review model accuracy, comparison metrics and actual vs predicted output.",
        ["MAE", "RMSE", "R² Score", "Error Analysis"],
    )

    if st.session_state.daily_sales is None:
        warning("No dataset loaded. Please upload CSV data from Upload Data page first.")
        return

    if st.session_state.training_result is None:
        warning("Train the model first to see performance metrics in this session.")
        return

    result = st.session_state.training_result
    metrics = result["metrics"]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi("Best Model", str(metrics["Model"]), "Selected model")
    with c2:
        kpi("MAE", format_currency(metrics["MAE"]), "Average error")
    with c3:
        kpi("RMSE", format_currency(metrics["RMSE"]), "Large error penalty")
    with c4:
        kpi("R² Score", f"{metrics['R2 Score']:.3f}", "Higher is better")

    st.subheader("Model Comparison")
    st.dataframe(result["comparison"], hide_index=True, use_container_width=True)

    st.subheader("Actual vs Predicted Sales")
    st.plotly_chart(actual_predicted_chart(result["best_prediction"]), use_container_width=True)

    error_df = result["best_prediction"].copy()
    error_df["Absolute Error"] = error_df["Error"].abs()

    fig = px.bar(
        error_df,
        x="Date",
        y="Absolute Error",
        title="Prediction Error by Date",
    )

    fig.update_traces(marker_color="#f87171")

    st.plotly_chart(apply_layout(fig, 420), use_container_width=True)
