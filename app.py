"""
Sales Forecasting Dashboard using Machine Learning

Run:
    python -m streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from config.settings import APP_TITLE
from app_pages.about import page_about
from app_pages.analysis import page_analysis
from app_pages.forecast import page_forecast
from app_pages.home import page_home
from app_pages.performance import page_performance
from app_pages.training import page_training
from app_pages.upload import page_upload
from state.session import initialize_state
from ui.styles import load_css
from ui.background import render_video_background


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("# 📈 Sales Forecasting")
        st.caption("Machine Learning Dashboard")
        st.markdown("---")

        page = st.radio(
            "Navigation",
            [
                "🏠 Home Dashboard",
                "📤 Upload Data",
                "📊 Sales Analysis",
                "🧠 Model Training",
                "🔮 Forecast Sales",
                "📌 Model Performance",
                "ℹ️ About Project",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")

        if st.session_state.clean_data is not None:
            df = st.session_state.clean_data

            st.caption("Active Dataset")

            dataset_type = "Sample Data" if st.session_state.is_sample_data else "Uploaded Data"

            st.write(f"**{st.session_state.source_name}**")
            st.write(f"Type: **{dataset_type}**")
            st.write(f"Rows: **{len(df):,}**")
            st.write(
                f"Period: **{df['Date'].min().strftime('%d %b %Y')} - "
                f"{df['Date'].max().strftime('%d %b %Y')}**"
            )
        else:
            st.caption("Active Dataset")
            st.write("No dataset loaded")

        return page


def render_page_container_start() -> None:
    st.markdown('<div class="page-shell">', unsafe_allow_html=True)


def render_page_container_end() -> None:
    st.markdown('</div>', unsafe_allow_html=True)


def main() -> None:
    initialize_state()
    load_css()
    render_video_background()

    page = render_sidebar()

    render_page_container_start()

    if page == "🏠 Home Dashboard":
        page_home()
    elif page == "📤 Upload Data":
        page_upload()
    elif page == "📊 Sales Analysis":
        page_analysis()
    elif page == "🧠 Model Training":
        page_training()
    elif page == "🔮 Forecast Sales":
        page_forecast()
    elif page == "📌 Model Performance":
        page_performance()
    elif page == "ℹ️ About Project":
        page_about()

    render_page_container_end()


if __name__ == "__main__":
    main()
