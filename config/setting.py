# config/setting.py — Central configuration for the Weather Analytics Dashboard
# SAVE THIS FILE AS: config/setting.py

import os

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Data paths ────────────────────────────────────────────────────────────────
DATA_DIR  = os.path.join(BASE_DIR, "data")
LOG_DIR   = os.path.join(BASE_DIR, "logs")
DATA_FILE = os.path.join(DATA_DIR, "weather.csv")

# ── Dashboard meta ────────────────────────────────────────────────────────────
APP_TITLE  = "WeatherIQ"
APP_HOST   = "0.0.0.0"
APP_PORT   = 8050
DEBUG_MODE = True

# ── Analytics config ──────────────────────────────────────────────────────────
MOVING_AVG_WINDOW   = 7        # days for rolling average
OUTLIER_Z_THRESHOLD = 3.0      # z-score cutoff for anomaly detection

# ── Required CSV columns ──────────────────────────────────────────────────────
REQUIRED_COLUMNS = [
    "date", "city", "temperature", "humidity",
    "wind_speed", "pressure", "condition",
]

# ── Condition colours (shared across both themes) ─────────────────────────────
CONDITION_COLORS = {
    "Sunny":         "#FBBF24",
    "Cloudy":        "#94A3B8",
    "Rainy":         "#4F8EF7",
    "Stormy":        "#7C3AED",
    "Foggy":         "#D1D5DB",
    "Windy":         "#34D399",
    "Partly Cloudy": "#FB923C",
}

# ── Vidarbha region cities ────────────────────────────────────────────────────
VIDARBHA_CITIES = [
    "Nagpur", "Amravati", "Wardha", "Chandrapur", "Akola",
    "Yavatmal", "Bhandara", "Gondia", "Washim", "Gadchiroli",
]

# ══════════════════════════════════════════════════════════════════════════════
#   LIGHT THEME  — Primary palette: #353535 / #3C6E71 / #FFFFFF / #D9D9D9 / #284B63
# ══════════════════════════════════════════════════════════════════════════════
LIGHT_THEME = {
    "name": "light",

    # ── Backgrounds ──────────────────────────────────────────────────────────
    "bg":           "#D9D9D9",    # main page background
    "surface":      "#FFFFFF",    # card / panel background
    "surface2":     "#F2F4F6",    # inner nested surface
    "border":       "#C4CDD6",

    # ── Brand colours ────────────────────────────────────────────────────────
    "primary":      "#3C6E71",    # teal accent
    "secondary":    "#284B63",    # dark-blue accent
    "success":      "#3C6E71",
    "warning":      "#E8A838",
    "danger":       "#E05A5A",

    # ── Text ─────────────────────────────────────────────────────────────────
    "text":         "#353535",    # primary body text
    "text_inv":     "#FFFFFF",    # text on dark backgrounds
    "muted":        "#6B7280",

    # ── Header bar ───────────────────────────────────────────────────────────
    "header_bg":    "#284B63",
    "header_text":  "#FFFFFF",

    # ── Buttons ──────────────────────────────────────────────────────────────
    "button_bg":    "#284B63",
    "button_hover": "#3C6E71",
    "button_text":  "#FFFFFF",

    # ── Card specifics ────────────────────────────────────────────────────────
    "card_bg":      "#FFFFFF",
    "card_border":  "#E2E8F0",
    "card_shadow":  "0 2px 16px rgba(40,75,99,0.10)",

    # ── Sidebar ───────────────────────────────────────────────────────────────
    "sidebar_bg":   "#FFFFFF",
    "sidebar_border": "#E2E8F0",

    # ── Plotly chart tokens ───────────────────────────────────────────────────
    "plot_bg":      "rgba(0,0,0,0)",
    "paper_bg":     "rgba(0,0,0,0)",
    "grid_color":   "#D9D9D9",
    "font_color":   "#353535",
    "axis_color":   "#6B7280",
    "legend_bg":    "rgba(255,255,255,0.85)",
    "template":     "plotly_white",

    # ── Toggle button label ───────────────────────────────────────────────────
    "toggle_label": "Dark Mode",
    "toggle_icon":  "🌙",
}

# ══════════════════════════════════════════════════════════════════════════════
#   DARK THEME  — Palette: #FFFFFF / #00171F / #003459 / #007EA7 / #00A8E8
# ══════════════════════════════════════════════════════════════════════════════
DARK_THEME = {
    "name": "dark",

    # ── Backgrounds ──────────────────────────────────────────────────────────
    "bg":           "#00171F",    # main page background
    "surface":      "#003459",    # card / panel background
    "surface2":     "#00253E",    # inner nested surface
    "border":       "#007EA7",

    # ── Brand colours ────────────────────────────────────────────────────────
    "primary":      "#007EA7",    # medium blue
    "secondary":    "#00A8E8",    # bright cyan-blue
    "success":      "#00A8E8",
    "warning":      "#FFC947",
    "danger":       "#FF6B6B",

    # ── Text ─────────────────────────────────────────────────────────────────
    "text":         "#FFFFFF",
    "text_inv":     "#003459",
    "muted":        "#B0C4D8",

    # ── Header bar ───────────────────────────────────────────────────────────
    "header_bg":    "#003459",
    "header_text":  "#FFFFFF",

    # ── Buttons ──────────────────────────────────────────────────────────────
    "button_bg":    "#007EA7",
    "button_hover": "#00A8E8",
    "button_text":  "#FFFFFF",

    # ── Card specifics ────────────────────────────────────────────────────────
    "card_bg":      "#003459",
    "card_border":  "#007EA7",
    "card_shadow":  "0 4px 24px rgba(0,0,0,0.45)",

    # ── Sidebar ───────────────────────────────────────────────────────────────
    "sidebar_bg":   "#003459",
    "sidebar_border": "#007EA7",

    # ── Plotly chart tokens ───────────────────────────────────────────────────
    "plot_bg":      "rgba(0,0,0,0)",
    "paper_bg":     "rgba(0,0,0,0)",
    "grid_color":   "#004A6E",
    "font_color":   "#FFFFFF",
    "axis_color":   "#B0C4D8",
    "legend_bg":    "rgba(0,52,89,0.85)",
    "template":     "plotly_dark",

    # ── Toggle button label ───────────────────────────────────────────────────
    "toggle_label": "Light Mode",
    "toggle_icon":  "☀️",
}

# ── Backward-compatible COLORS alias (maps to dark theme keys) ────────────────
COLORS = {
    "primary":   DARK_THEME["primary"],
    "secondary": DARK_THEME["secondary"],
    "success":   DARK_THEME["success"],
    "warning":   DARK_THEME["warning"],
    "danger":    DARK_THEME["danger"],
    "dark":      DARK_THEME["bg"],
    "card_bg":   DARK_THEME["card_bg"],
    "bg":        DARK_THEME["bg"],
    "text":      DARK_THEME["text"],
    "muted":     DARK_THEME["muted"],
    "border":    DARK_THEME["border"],
}

# ── Theme lookup ──────────────────────────────────────────────────────────────
THEMES = {
    "light": LIGHT_THEME,
    "dark":  DARK_THEME,
}

def get_theme(name: str) -> dict:
    """Return theme dict by name ('light' or 'dark'). Defaults to dark."""
    return THEMES.get(name, DARK_THEME)