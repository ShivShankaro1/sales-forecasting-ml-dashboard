import pandas as pd
import streamlit as st

from core.preprocessing import clean_data, get_daily_sales, validate_data
from ui.components import error


def initialize_state() -> None:
    """
    Initialize session state only once.
    Do not auto-load sample data here.
    Do not reset uploaded data on page change.
    """

    defaults = {
        "raw_data": None,
        "clean_data": None,
        "daily_sales": None,
        "training_result": None,
        "model_bundle": None,
        "forecast_result": None,
        "source_name": None,
        "is_sample_data": False,

        # Upload confirmation flow
        "pending_upload_data": None,
        "pending_upload_name": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def store_data(df: pd.DataFrame, source_name: str, is_sample: bool = False) -> bool:
    """
    Validate, clean and store the selected dataset in Streamlit session state.
    Uploaded data remains active after page navigation.
    """

    valid, messages = validate_data(df)

    if not valid:
        for msg in messages:
            error(msg)
        return False

    try:
        cleaned = clean_data(df)

        if cleaned.empty:
            error("No valid rows found after data cleaning.")
            return False

        daily = get_daily_sales(cleaned)

        st.session_state.raw_data = df.copy()
        st.session_state.clean_data = cleaned.copy()
        st.session_state.daily_sales = daily.copy()
        st.session_state.source_name = source_name
        st.session_state.is_sample_data = is_sample

        # Reset model and forecast because active dataset changed
        st.session_state.training_result = None
        st.session_state.model_bundle = None
        st.session_state.forecast_result = None

        return True

    except Exception as ex:
        error(f"Data processing failed: {ex}")
        return False
