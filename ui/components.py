import streamlit as st

from config.settings import CURRENCY


def hero(title: str, subtitle: str, pills: list[str]) -> None:
    pill_html = "".join([f"<span class='pill'>{p}</span>" for p in pills])

    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
            <div class="pill-row">{pill_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi(label: str, value: str, note: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info(message: str) -> None:
    st.markdown(f"<div class='info-box'>{message}</div>", unsafe_allow_html=True)


def success(message: str) -> None:
    st.markdown(f"<div class='success-box'>✅ {message}</div>", unsafe_allow_html=True)


def warning(message: str) -> None:
    st.markdown(f"<div class='warning-box'>⚠️ {message}</div>", unsafe_allow_html=True)


def error(message: str) -> None:
    st.markdown(f"<div class='error-box'>❌ {message}</div>", unsafe_allow_html=True)


def format_currency(value: float | int) -> str:
    value = float(value)

    if abs(value) >= 10_000_000:
        return f"{CURRENCY}{value / 10_000_000:.2f}Cr"
    if abs(value) >= 100_000:
        return f"{CURRENCY}{value / 100_000:.2f}L"
    if abs(value) >= 1_000:
        return f"{CURRENCY}{value / 1_000:.2f}K"

    return f"{CURRENCY}{value:,.0f}"


def format_number(value: float | int) -> str:
    value = float(value)

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.2f}K"

    return f"{value:,.0f}"
