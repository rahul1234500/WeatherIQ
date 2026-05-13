# components/cards.py — Theme-aware KPI card HTML builders
# SAVE THIS FILE AS: components/cards.py

from dash import html


def kpi_card(title: str, value: str, unit: str, icon: str,
             accent: str, theme: dict) -> html.Div:
    """Single KPI card with floating icon and background tint (no top border)."""
    return html.Div([
        html.Div([
            html.Span(icon, className="kpi-icon", style={"backgroundColor": f"{accent}20", "color": accent}),
            html.Div([
                html.P(title, className="kpi-title"),
                html.H3(
                    [value, html.Span(f" {unit}", className="kpi-unit")],
                    className="kpi-value",
                ),
            ], className="kpi-text"),
        ], className="kpi-inner"),
    ], className="kpi-card")


def build_kpi_section(kpis: dict, theme: dict) -> html.Div:
    """Build a 5-card KPI grid using the active theme's accent colours."""
    cards_list = [
        kpi_card("Avg Temperature", str(kpis.get("avg_temp",   "—")), "°C",   "🌡️", theme["primary"],   theme),
        kpi_card("Max Temperature", str(kpis.get("max_temp",   "—")), "°C",   "🔥", theme["danger"],    theme),
        kpi_card("Min Temperature", str(kpis.get("min_temp",   "—")), "°C",   "❄️", theme["secondary"], theme),
        kpi_card("Avg Humidity",    str(kpis.get("avg_humidity","—")), "%",    "💧", theme["success"],   theme),
        kpi_card("Avg Wind Speed",  str(kpis.get("avg_wind",   "—")), "km/h", "💨", theme["warning"],   theme),
    ]
    return html.Div(cards_list, className="kpi-grid")