# components/filters.py — Sidebar filter controls with Year dropdown
# SAVE THIS FILE AS: components/filters.py

import pandas as pd
from dash import html, dcc


def build_filters(df: pd.DataFrame) -> html.Div:
    """Build the full sidebar filter panel.
    Dynamically derives all option ranges from the passed dataframe.
    Includes: City, Condition, Year, Temperature, Humidity, Date Range.
    """
    cities     = sorted(df["city"].unique().tolist())
    conditions = sorted(df["condition"].unique().tolist())
    years      = sorted(df["year"].unique().tolist())
    min_temp   = int(df["temperature"].min()) - 1
    max_temp   = int(df["temperature"].max()) + 1
    min_date   = df["date"].min().date()
    max_date   = df["date"].max().date()

    return html.Div([

        html.H3("Filters", className="filter-heading"),

        # ── City ──────────────────────────────────────────────────────────────
        html.Label("📍 City", className="filter-label"),
        dcc.Dropdown(
            id="city-filter",
            options=[{"label": c, "value": c} for c in cities],
            value=cities,
            multi=True,
            placeholder="All cities",
            className="dash-dropdown",
        ),

        # ── Weather Condition ──────────────────────────────────────────────────
        html.Label("🌤️ Condition", className="filter-label"),
        dcc.Dropdown(
            id="condition-filter",
            options=[{"label": c, "value": c} for c in conditions],
            value=[],
            multi=True,
            placeholder="All conditions",
            className="dash-dropdown",
        ),

        # ── Year (NEW) ─────────────────────────────────────────────────────────
        html.Label("📅 Year", className="filter-label"),
        dcc.Dropdown(
            id="year-filter",
            options=[{"label": str(y), "value": y} for y in years],
            value=years,
            multi=True,
            placeholder="All years",
            className="dash-dropdown",
        ),

        # ── Temperature Range ──────────────────────────────────────────────────
        html.Label("🌡️ Temperature Range (°C)", className="filter-label"),
        dcc.RangeSlider(
            id="temp-filter",
            min=min_temp, max=max_temp, step=1,
            value=[min_temp, max_temp],
            marks={v: str(v) for v in range(min_temp, max_temp + 1, 10)},
            tooltip={"always_visible": False, "placement": "bottom"},
        ),

        # ── Humidity Range ─────────────────────────────────────────────────────
        html.Label("💧 Humidity Range (%)", className="filter-label"),
        dcc.RangeSlider(
            id="humidity-filter",
            min=0, max=100, step=5,
            value=[0, 100],
            marks={v: str(v) for v in range(0, 101, 20)},
            tooltip={"always_visible": False},
        ),

        # ── Date Range ─────────────────────────────────────────────────────────
        html.Label("📆 Date Range", className="filter-label"),
        dcc.DatePickerRange(
            id="date-filter",
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=min_date,
            end_date=max_date,
            display_format="MMM D, YYYY",
            className="date-picker",
            number_of_months_shown=1,  # Show 1 month instead of 2 to prevent overlap
        ),

        # ── Reset button ───────────────────────────────────────────────────────
        html.Div([
            html.Button("Reset Filters", id="reset-btn", className="reset-btn"),
        ], style={"marginTop": "22px"}),

    ], className="filter-sidebar")