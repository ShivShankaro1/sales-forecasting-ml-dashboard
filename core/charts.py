import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def apply_layout(fig: go.Figure, height: int = 420) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(2,6,23,0.55)",
        font=dict(
            color="#e5e7eb",
            family="Inter, Segoe UI, Arial",
            size=13,
        ),
        title=dict(
            font=dict(
                size=21,
                color="#f8fafc",
                family="Inter, Segoe UI, Arial",
            ),
            x=0.02,
            xanchor="left",
        ),
        margin=dict(l=22, r=22, t=72, b=48),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="right",
            x=1,
            bgcolor="rgba(15,23,42,0.55)",
            bordercolor="rgba(148,163,184,0.20)",
            borderwidth=1,
        ),
        hoverlabel=dict(
            bgcolor="#020617",
            bordercolor="#00e5ff",
            font_size=13,
            font_color="#ffffff",
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(148,163,184,0.25)",
        tickfont=dict(color="#cbd5e1"),
        title_font=dict(color="#e5e7eb"),
    )

    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.14)",
        zeroline=False,
        linecolor="rgba(148,163,184,0.25)",
        tickfont=dict(color="#cbd5e1"),
        title_font=dict(color="#e5e7eb"),
    )

    return fig


def daily_sales_chart(daily_df: pd.DataFrame) -> go.Figure:
    fig = px.line(
        daily_df,
        x="Date",
        y="Sales",
        title="Daily Sales Trend",
    )

    fig.update_traces(
        line=dict(color="#00e5ff", width=3.5),
        fill="tozeroy",
        fillcolor="rgba(0,229,255,0.16)",
        hovertemplate="<b>Date:</b> %{x}<br><b>Sales:</b> ₹%{y:,.2f}<extra></extra>",
    )

    return apply_layout(fig, 450)


def monthly_sales_chart(df: pd.DataFrame) -> go.Figure:
    monthly = df.copy()
    monthly["Month"] = monthly["Date"].dt.to_period("M").astype(str)
    monthly = monthly.groupby("Month", as_index=False)["Sales"].sum()

    fig = px.bar(
        monthly,
        x="Month",
        y="Sales",
        title="Monthly Sales Summary",
        text_auto=".2s",
    )

    fig.update_traces(
        marker=dict(
            color=monthly["Sales"],
            colorscale=[
                [0, "#0ea5e9"],
                [0.5, "#6366f1"],
                [1, "#d946ef"],
            ],
            line=dict(color="rgba(255,255,255,0.20)", width=1),
        ),
        hovertemplate="<b>Month:</b> %{x}<br><b>Sales:</b> ₹%{y:,.2f}<extra></extra>",
    )

    return apply_layout(fig, 430)


def category_sales_chart(df: pd.DataFrame) -> go.Figure:
    category_df = df.groupby("Category", as_index=False)["Sales"].sum()
    category_df = category_df.sort_values("Sales", ascending=False)

    fig = px.bar(
        category_df,
        x="Category",
        y="Sales",
        title="Category-wise Revenue",
        color="Sales",
        color_continuous_scale=["#00e5ff", "#6366f1", "#d946ef"],
        text_auto=".2s",
    )

    fig.update_traces(
        marker_line_color="rgba(255,255,255,0.22)",
        marker_line_width=1.2,
        hovertemplate="<b>Category:</b> %{x}<br><b>Sales:</b> ₹%{y:,.2f}<extra></extra>",
    )

    fig.update_layout(coloraxis_showscale=False)

    return apply_layout(fig, 430)


def product_sales_chart(df: pd.DataFrame) -> go.Figure:
    product_df = df.groupby("Product", as_index=False)["Sales"].sum()
    product_df = product_df.sort_values("Sales", ascending=True).tail(10)

    fig = px.bar(
        product_df,
        x="Sales",
        y="Product",
        orientation="h",
        title="Top 10 Products by Revenue",
        color="Sales",
        color_continuous_scale=["#22d3ee", "#818cf8", "#f472b6"],
        text_auto=".2s",
    )

    fig.update_traces(
        marker_line_color="rgba(255,255,255,0.20)",
        marker_line_width=1,
        hovertemplate="<b>Product:</b> %{y}<br><b>Sales:</b> ₹%{x:,.2f}<extra></extra>",
    )

    fig.update_layout(coloraxis_showscale=False)

    return apply_layout(fig, 450)


def actual_predicted_chart(result_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=result_df["Date"],
            y=result_df["Actual Sales"],
            mode="lines+markers",
            name="Actual Sales",
            line=dict(color="#22c55e", width=3.5),
            marker=dict(size=6, color="#22c55e"),
            hovertemplate="<b>Actual:</b> ₹%{y:,.2f}<br><b>Date:</b> %{x}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=result_df["Date"],
            y=result_df["Predicted Sales"],
            mode="lines+markers",
            name="Predicted Sales",
            line=dict(color="#f59e0b", width=3.5, dash="dot"),
            marker=dict(size=6, color="#f59e0b"),
            hovertemplate="<b>Predicted:</b> ₹%{y:,.2f}<br><b>Date:</b> %{x}<extra></extra>",
        )
    )

    fig.update_layout(title="Actual vs Predicted Sales")

    return apply_layout(fig, 450)


def forecast_chart(daily_df: pd.DataFrame, forecast_df: pd.DataFrame) -> go.Figure:
    recent_history = daily_df.tail(90)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=recent_history["Date"],
            y=recent_history["Sales"],
            mode="lines",
            name="Historical Sales",
            line=dict(color="#00e5ff", width=3.5),
            fill="tozeroy",
            fillcolor="rgba(0,229,255,0.10)",
            hovertemplate="<b>Historical:</b> ₹%{y:,.2f}<br><b>Date:</b> %{x}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Predicted Sales"],
            mode="lines+markers",
            name="Forecast Sales",
            line=dict(color="#facc15", width=4, dash="dash"),
            marker=dict(size=8, color="#facc15", line=dict(color="#ffffff", width=1)),
            hovertemplate="<b>Forecast:</b> ₹%{y:,.2f}<br><b>Date:</b> %{x}<extra></extra>",
        )
    )

    fig.update_layout(title="Future Sales Forecast")

    return apply_layout(fig, 480)
