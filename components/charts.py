# components/charts.py — All Plotly chart builders (theme-aware)
# SAVE THIS FILE AS: components/charts.py
# Every function accepts a `theme` dict from config.settings.LIGHT_THEME / DARK_THEME

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from config.settings import CONDITION_COLORS
from utilis import analytics


# ── Shared layout factory ─────────────────────────────────────────────────────
def _base_layout(theme: dict, title: str = "") -> dict:
    """Return a Plotly layout dict wired to the active theme's tokens."""
    return dict(
        title=dict(
            text=title,
            font=dict(size=15, color=theme["font_color"], family="Inter, sans-serif"),
            x=0.01, xanchor="left",
        ),
        paper_bgcolor=theme["paper_bg"],
        plot_bgcolor=theme["plot_bg"],
        font=dict(color=theme["font_color"], family="Inter, sans-serif", size=12),
        margin=dict(l=48, r=24, t=52, b=44),
        legend=dict(
            bgcolor=theme["legend_bg"],
            font=dict(color=theme["font_color"], size=11),
            bordercolor=theme["border"],
            borderwidth=1,
        ),
        xaxis=dict(
            gridcolor=theme["grid_color"],
            zerolinecolor=theme["grid_color"],
            tickfont=dict(color=theme["axis_color"], size=11),
            linecolor=theme["border"],
        ),
        yaxis=dict(
            gridcolor=theme["grid_color"],
            zerolinecolor=theme["grid_color"],
            tickfont=dict(color=theme["axis_color"], size=11),
            linecolor=theme["border"],
        ),
        hoverlabel=dict(
            bgcolor=theme["surface"],
            font_color=theme["text"],
            bordercolor=theme["border"],
        ),
    )


def _apply(fig: go.Figure, theme: dict, title: str = "") -> go.Figure:
    fig.update_layout(**_base_layout(theme, title))
    return fig


def _empty(msg: str, theme: dict) -> go.Figure:
    """Empty-state placeholder chart."""
    fig = go.Figure()
    fig.add_annotation(
        text=msg, xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color=theme["muted"]),
    )
    fig.update_layout(**_base_layout(theme))
    return fig


# ── 1. Temperature Trend Line Chart ──────────────────────────────────────────
def temperature_trend_chart(df: pd.DataFrame, theme: dict) -> go.Figure:
    if df.empty:
        return _empty("No data for selected filters", theme)

    trend = analytics.temperature_trend(df)
    fig = px.line(
        trend, x="date", y="avg_temp",
        labels={"avg_temp": "Avg Temp (°C)", "date": "Date"},
        color_discrete_sequence=[theme["primary"]],
    )
    fig.update_traces(line_width=2.5, mode="lines")
    return _apply(fig, theme, "🌡️  Temperature Trend Over Time")


# ── 2. 7-Day Moving Average Chart ────────────────────────────────────────────
def moving_average_chart(df: pd.DataFrame, theme: dict) -> go.Figure:
    if df.empty:
        return _empty("No data", theme)

    ma = analytics.moving_average(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ma["date"], y=ma["avg_temp"],
        name="Daily Avg", mode="lines",
        line=dict(color=theme["muted"], width=1),
        opacity=0.55,
    ))
    fig.add_trace(go.Scatter(
        x=ma["date"], y=ma["moving_avg"],
        name="7-Day Moving Avg", mode="lines",
        line=dict(color=theme["warning"], width=2.8),
    ))
    return _apply(fig, theme, "📈  7-Day Moving Average Temperature")


# ── 3. Monthly Humidity Bar Chart ─────────────────────────────────────────────
def humidity_bar_chart(df: pd.DataFrame, theme: dict) -> go.Figure:
    if df.empty:
        return _empty("No data", theme)

    monthly = analytics.monthly_insights(df)
    monthly["period"] = monthly["month_name"].astype(str) + " " + monthly["year"].astype(str)
    fig = px.bar(
        monthly, x="period", y="avg_humidity",
        labels={"avg_humidity": "Humidity (%)", "period": "Month"},
        color="avg_humidity",
        color_continuous_scale=[theme["primary"], theme["secondary"]],
    )
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_tickangle=-45,
    )
    return _apply(fig, theme, "💧  Monthly Average Humidity")


# ── 4. Weather Condition Donut Pie Chart ──────────────────────────────────────
def condition_pie_chart(df: pd.DataFrame, theme: dict) -> go.Figure:
    if df.empty:
        return _empty("No data", theme)

    freq   = analytics.condition_frequency(df)
    colors = [CONDITION_COLORS.get(c, theme["primary"]) for c in freq["condition"]]
    fig = go.Figure(go.Pie(
        labels=freq["condition"],
        values=freq["count"],
        marker=dict(colors=colors, line=dict(color=theme["bg"], width=2)),
        hole=0.42,
        textinfo="label+percent",
        textposition="outside",
        textfont=dict(color=theme["font_color"], size=11),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
    ))
    fig.update_layout(**_base_layout(theme, "⛅  Weather Condition Distribution"))
    fig.update_layout(margin=dict(l=50, r=50, t=50, b=50))  # Extra margin for outside labels
    return fig


# ── 5. Wind Speed vs Temperature Scatter ──────────────────────────────────────
def wind_scatter_chart(df: pd.DataFrame, theme: dict) -> go.Figure:
    if df.empty:
        return _empty("No data", theme)

    sample = df.sample(min(1500, len(df)), random_state=42)
    fig = px.scatter(
        sample, x="temperature", y="wind_speed",
        color="condition",
        color_discrete_map=CONDITION_COLORS,
        labels={"temperature": "Temperature (°C)", "wind_speed": "Wind Speed (km/h)"},
        opacity=0.72,
        hover_data=["city", "date"],
    )
    return _apply(fig, theme, "💨  Wind Speed vs Temperature")


# ── 6. Correlation Heatmap ────────────────────────────────────────────────────
def correlation_heatmap(df: pd.DataFrame, theme: dict) -> go.Figure:
    if df.empty:
        return _empty("No data", theme)

    corr = analytics.correlation_matrix(df)

    # Use theme-appropriate colorscale
    if theme["name"] == "dark":
        colorscale = [[0, "#003459"], [0.5, "#007EA7"], [1, "#00A8E8"]]
    else:
        colorscale = [[0, "#284B63"], [0.5, "#3C6E71"], [1, "#FFFFFF"]]

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale=colorscale,
        zmin=-1, zmax=1,
        text=corr.values.round(2),
        texttemplate="%{text}",
        textfont=dict(size=13, color=theme["font_color"]),
        hovertemplate="%{x} × %{y}<br>Correlation: %{z:.3f}<extra></extra>",
    ))
    fig.update_layout(**_base_layout(theme, "🔗  Correlation Heatmap"))
    return fig


# ── 7. City Comparison Box Plot ───────────────────────────────────────────────
def city_comparison_chart(df: pd.DataFrame, theme: dict) -> go.Figure:
    if df.empty:
        return _empty("No data", theme)

    fig = px.box(
        df, x="city", y="temperature",
        color="city",
        labels={"temperature": "Temperature (°C)", "city": "City"},
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig.update_traces(boxmean="sd")
    fig.update_layout(showlegend=False)
    return _apply(fig, theme, "🏙️  Temperature Distribution by City")