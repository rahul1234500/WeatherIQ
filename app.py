# app.py — Weather Analytics Dashboard (Entry Point)
# SAVE THIS FILE AS: app.py (project root)

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import logging
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State

from config.settings import (
    APP_TITLE, APP_HOST, APP_PORT, DEBUG_MODE,
    LIGHT_THEME, DARK_THEME, get_theme,
)
from utilis.data_loader import load_data
from utilis.preprocessing import clean_data, add_features, apply_filters
from utilis import analytics
from components import charts, cards, filters as filter_comp

# ── Logging ───────────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/dashboard.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("app")

# ── Load & prepare data ───────────────────────────────────────────────────────
logger.info("Loading data...")
raw_df   = load_data()
clean_df = clean_data(raw_df)
full_df  = add_features(clean_df)
logger.info(f"Dataset ready: {len(full_df):,} rows")

all_cities     = sorted(full_df["city"].unique().tolist())
all_conditions = sorted(full_df["condition"].unique().tolist())
all_years      = sorted(full_df["year"].unique().tolist())
min_date       = full_df["date"].min().date()
max_date       = full_df["date"].max().date()
temp_min       = int(full_df["temperature"].min()) - 1
temp_max       = int(full_df["temperature"].max()) + 1

logger.info(f"Cities: {len(all_cities)} | Years: {all_years} | Dates: {min_date} to {max_date}")

# ── Dash app ──────────────────────────────────────────────────────────────────
app = Dash(
    __name__,
    title=APP_TITLE,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True,
)
server = app.server  # gunicorn entry point


# ── Layout ────────────────────────────────────────────────────────────────────
def serve_layout():
    init_kpis  = analytics.compute_kpis(full_df)
    init_theme = DARK_THEME

    return html.Div(
        id="theme-wrapper",
        className="theme-dark",   # default; sync callback corrects on load
        children=[

            # ── Stores & intervals ────────────────────────────────────────
            dcc.Store(id="theme-store", data="dark", storage_type="local"),
            dcc.Store(id="filter-store"),
            dcc.Interval(id="clock-tick", interval=60_000),

            # ══════════════════════════════════════════════════════════════
            # STICKY HEADER
            # ══════════════════════════════════════════════════════════════
            html.Div(
                className="topbar",
                children=[
                    # Brand
                    html.Div([
                        html.Span("🌤️", className="topbar-logo"),
                        html.Div([
                            html.H1(
                                ["Weather", html.Span("IQ", className="accent-word")],
                                className="topbar-title",
                            ),
                            html.P(
                                f"India Climate Insights  •  2023 – 2026  •  {len(full_df):,} records",
                                className="topbar-sub",
                            ),
                        ]),
                    ], className="topbar-brand"),

                    # Right controls
                    html.Div([
                        html.Div([
                            html.Span("●", className="live-dot"),
                            html.Span(" LIVE"),
                        ], className="live-badge"),

                        html.Button(
                            id="theme-toggle",
                            children="☀️  Light Mode",
                            n_clicks=0,
                            className="theme-btn",
                        ),
                    ], className="topbar-right"),
                ],
            ),

            # ══════════════════════════════════════════════════════════════
            # PAGE BODY
            # ══════════════════════════════════════════════════════════════
            html.Div(
                className="page-body",
                children=[

                    # KPI Section
                    html.P("Key Performance Indicators", className="section-title"),
                    html.Div(
                        id="kpi-section",
                        children=cards.build_kpi_section(init_kpis, init_theme),
                    ),

                    # Main grid
                    html.Div([

                        # Sidebar filters
                        filter_comp.build_filters(full_df),

                        # Charts grid
                        html.Div([

                            # Row 1: Full-width temperature trend
                            html.Div(
                                dcc.Graph(id="temp-trend",
                                          config={"displayModeBar": False}),
                                className="chart-card",
                            ),

                            # Row 2: Moving avg + Humidity (2 columns)
                            html.Div([
                                html.Div(
                                    dcc.Graph(id="moving-avg",
                                              config={"displayModeBar": False}),
                                    className="chart-card",
                                ),
                                html.Div(
                                    dcc.Graph(id="humidity-bar",
                                              config={"displayModeBar": False}),
                                    className="chart-card",
                                ),
                            ], className="chart-row-2"),

                            # Row 3: Pie + Scatter + Heatmap (3 columns)
                            html.Div([
                                html.Div(
                                    dcc.Graph(id="condition-pie",
                                              config={"displayModeBar": False}),
                                    className="chart-card",
                                ),
                                html.Div(
                                    dcc.Graph(id="wind-scatter",
                                              config={"displayModeBar": False}),
                                    className="chart-card",
                                ),
                                html.Div(
                                    dcc.Graph(id="corr-heatmap",
                                              config={"displayModeBar": False}),
                                    className="chart-card",
                                ),
                            ], className="chart-row-3"),

                            # Row 4: City box plot (full width)
                            html.Div(
                                dcc.Graph(id="city-box",
                                          config={"displayModeBar": False}),
                                className="chart-card",
                            ),

                        ], className="charts-area"),

                    ], className="main-layout"),
                ],
            ),
        ],
    )


app.layout = serve_layout


# ══════════════════════════════════════════════════════════════════════════════
# CALLBACKS
# ══════════════════════════════════════════════════════════════════════════════

# ── 1. Theme Toggle: store update only ────────────────────────────────────────
@app.callback(
    Output("theme-store", "data"),
    Input("theme-toggle", "n_clicks"),
    State("theme-store", "data"),
    prevent_initial_call=True,
)
def toggle_theme_store(n_clicks, current_theme):
    """Flip the stored theme name. UI sync handled by separate callback."""
    return "light" if current_theme == "dark" else "dark"


# ── 2. Theme Sync: store → wrapper class + button label ───────────────────────
#    Fires on EVERY store change (including localStorage restore on load).
@app.callback(
    Output("theme-wrapper", "className"),
    Output("theme-toggle",  "children"),
    Input("theme-store", "data"),
)
def sync_theme_ui(theme_name):
    """Apply wrapper class and update button label to match active theme."""
    if theme_name == "light":
        return "theme-light", "🌙  Dark Mode"
    return "theme-dark", "☀️  Light Mode"


# ── 3. Reset Filters ──────────────────────────────────────────────────────────
@app.callback(
    Output("city-filter",      "value"),
    Output("condition-filter", "value"),
    Output("year-filter",      "value"),
    Output("temp-filter",      "value"),
    Output("humidity-filter",  "value"),
    Output("date-filter",      "start_date"),
    Output("date-filter",      "end_date"),
    Input("reset-btn",         "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(_):
    return all_cities, [], all_years, [temp_min, temp_max], [0, 100], str(min_date), str(max_date)


# ── Helper filter ─────────────────────────────────────────────────────────────
def _apply_all_filters(cities, conditions, years, temp_range, hum_range,
                       start, end) -> pd.DataFrame:
    return apply_filters(
        full_df,
        cities         = cities       or all_cities,
        conditions     = conditions   if conditions else None,
        years          = years        if years      else None,
        temp_range     = temp_range,
        humidity_range = hum_range,
        date_range     = [start, end] if (start and end) else None,
    )


# ── 4. Master update: filters + theme → KPIs + all 7 charts ──────────────────
@app.callback(
    Output("kpi-section",   "children"),
    Output("temp-trend",    "figure"),
    Output("moving-avg",    "figure"),
    Output("humidity-bar",  "figure"),
    Output("condition-pie", "figure"),
    Output("wind-scatter",  "figure"),
    Output("corr-heatmap",  "figure"),
    Output("city-box",      "figure"),
    Input("city-filter",      "value"),
    Input("condition-filter", "value"),
    Input("year-filter",      "value"),
    Input("temp-filter",      "value"),
    Input("humidity-filter",  "value"),
    Input("date-filter",      "start_date"),
    Input("date-filter",      "end_date"),
    Input("theme-store",      "data"),
)
def update_all(cities, conditions, years, temp_range, hum_range, start, end, theme_name):
    theme = get_theme(theme_name)
    df    = _apply_all_filters(cities, conditions, years, temp_range, hum_range, start, end)
    logger.info(f"update_all [{theme_name}] -> {len(df):,} rows")

    return (
        cards.build_kpi_section(analytics.compute_kpis(df) if not df.empty else
                                {"avg_temp": "-", "max_temp": "-", "min_temp": "-",
                                 "avg_humidity": "-", "avg_wind": "-"}, theme),
        charts.temperature_trend_chart(df, theme),
        charts.moving_average_chart(df, theme),
        charts.humidity_bar_chart(df, theme),
        charts.condition_pie_chart(df, theme),
        charts.wind_scatter_chart(df, theme),
        charts.correlation_heatmap(df, theme),
        charts.city_comparison_chart(df, theme),
    )


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info(f"Starting {APP_TITLE} at http://{APP_HOST}:{APP_PORT}")
    app.run(host=APP_HOST, port=APP_PORT, debug=DEBUG_MODE)