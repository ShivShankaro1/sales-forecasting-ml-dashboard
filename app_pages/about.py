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


def page_about() -> None:
    hero(
        "About Project",
        "Internship-ready machine learning project with source code, documentation, screenshots and GitHub submission structure.",
        ["GitHub Ready", "Documentation", "Screenshots", "Output Files"],
    )

    st.subheader("Project Scope")

    info(
        "This project predicts future sales using historical sales data. "
        "It provides CSV upload, data validation, sales analysis, model training, model performance review, and future sales forecasting."
    )

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Features")

        features = pd.DataFrame(
            [
                ["Upload CSV", "Upload custom sales data"],
                ["Sample Data", "Auto-generated sample dataset included"],
                ["Sales Dashboard", "KPIs and business summary"],
                ["Sales Analysis", "Product/category/monthly charts"],
                ["Model Training", "Train and retrain ML model"],
                ["Forecasting", "Predict future sales"],
                ["Export", "Download forecast CSV"],
            ],
            columns=["Feature", "Description"],
        )

        st.dataframe(features, hide_index=True, use_container_width=True)

    with c2:
        st.subheader("Technology Stack")

        tech = pd.DataFrame(
            [
                ["Python", "Core programming language"],
                ["Streamlit", "Web dashboard UI"],
                ["Pandas / NumPy", "Data processing"],
                ["Scikit-learn", "Machine learning"],
                ["Plotly", "Interactive charts"],
                ["Joblib", "Model saving/loading"],
            ],
            columns=["Technology", "Purpose"],
        )

        st.dataframe(tech, hide_index=True, use_container_width=True)

    st.subheader("Submission Folder Structure")

    st.code(
        """
sales-forecasting-ml-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_sales_data.csv
├── models/
│   └── sales_forecasting_model.pkl
├── output/
│   ├── forecast_output.csv
│   ├── model_comparison.csv
│   └── actual_vs_predicted.csv
├── screenshots/
├── documentation/
└── src/
        """.strip()
    )
