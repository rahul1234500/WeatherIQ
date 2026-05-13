# smoke_test.py — Full end-to-end validation
# Run with:  python smoke_test.py

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("  Weather Dashboard v2 — Full Smoke Test")
print("=" * 60)

# Package versions
import dash, plotly, pandas as pd, numpy as np
print(f"\nPackage versions:")
print(f"  dash    : {dash.__version__}")
print(f"  plotly  : {plotly.__version__}")
print(f"  pandas  : {pd.__version__}")
print(f"  numpy   : {np.__version__}")

# Import chain
print("\nImport chain:")
from config.settings import (
    APP_TITLE, COLORS, CONDITION_COLORS, REQUIRED_COLUMNS,
    LIGHT_THEME, DARK_THEME, get_theme, VIDARBHA_CITIES,
)
print("  [OK] config.settings (LIGHT_THEME, DARK_THEME, get_theme, VIDARBHA_CITIES)")

from utilis.data_loader import load_data
print("  [OK] utilis.data_loader")

from utilis.preprocessing import clean_data, add_features, apply_filters
print("  [OK] utilis.preprocessing")

from utilis import analytics
print("  [OK] utilis.analytics")

from components import charts, cards, filters
print("  [OK] components (charts, cards, filters)")

# Data pipeline
print("\nData pipeline:")
raw   = load_data()
clean = clean_data(raw)
full  = add_features(clean)

print(f"  Rows loaded  : {len(full):,}")
city_list = sorted(full['city'].unique().tolist())
print(f"  Cities ({len(city_list)}): {', '.join(city_list[:5])}... etc.")
years = sorted(full['year'].unique().tolist())
print(f"  Years        : {years}")
print(f"  Date range   : {full['date'].min().date()} to {full['date'].max().date()}")

# Vidarbha cities check
vidarbha_in_data = [c for c in VIDARBHA_CITIES if c in city_list]
print(f"\nVidarbha cities in dataset ({len(vidarbha_in_data)}/10):")
print(f"  {', '.join(vidarbha_in_data)}")
assert len(vidarbha_in_data) == 10, "Missing Vidarbha cities!"

# Analytics
print("\nAnalytics:")
kpis = analytics.compute_kpis(full)
for k, v in kpis.items():
    print(f"  {k:<18}: {v}")

freq = analytics.condition_frequency(full)
print("\nCondition frequency:")
print(freq.to_string(index=False))

# Theme system
print("\nTheme system:")
light = get_theme("light")
dark  = get_theme("dark")
print(f"  [OK] LIGHT_THEME: name={light['name']}, bg={light['bg']}, primary={light['primary']}")
print(f"  [OK] DARK_THEME:  name={dark['name']}, bg={dark['bg']}, primary={dark['primary']}")

# Chart builders — both themes
print("\nChart builders (dark theme):")
for name, fn in [
    ("temperature_trend_chart", charts.temperature_trend_chart),
    ("moving_average_chart",    charts.moving_average_chart),
    ("humidity_bar_chart",      charts.humidity_bar_chart),
    ("condition_pie_chart",     charts.condition_pie_chart),
    ("wind_scatter_chart",      charts.wind_scatter_chart),
    ("correlation_heatmap",     charts.correlation_heatmap),
    ("city_comparison_chart",   charts.city_comparison_chart),
]:
    fig = fn(full, dark)
    print(f"  [OK] {name}")

print("\nChart builders (light theme):")
for name, fn in [
    ("temperature_trend_chart", charts.temperature_trend_chart),
    ("condition_pie_chart",     charts.condition_pie_chart),
    ("city_comparison_chart",   charts.city_comparison_chart),
]:
    fig = fn(full, light)
    print(f"  [OK] {name}")

# KPI cards
print("\nKPI cards:")
kpi_dark  = cards.build_kpi_section(kpis, dark)
kpi_light = cards.build_kpi_section(kpis, light)
print("  [OK] build_kpi_section (dark)")
print("  [OK] build_kpi_section (light)")

# Year filter
print("\nYear filter:")
df_2026 = apply_filters(full, years=[2026])
print(f"  2026 only: {len(df_2026):,} rows")
df_vid  = apply_filters(full, cities=VIDARBHA_CITIES)
print(f"  Vidarbha only: {len(df_vid):,} rows")
df_both = apply_filters(full, cities=["Nagpur", "Chandrapur"], years=[2025, 2026])
print(f"  Nagpur+Chandrapur 2025-2026: {len(df_both):,} rows")

# Empty state guard
empty_fig = charts.temperature_trend_chart(pd.DataFrame(), dark)
print("\n  [OK] Empty DataFrame handled gracefully (dark)")
empty_fig = charts.temperature_trend_chart(pd.DataFrame(), light)
print("  [OK] Empty DataFrame handled gracefully (light)")

print("\n" + "=" * 60)
print("  ALL TESTS PASSED - Dashboard v2 is production ready!")
print("=" * 60)
print(f"\nOpen browser at: http://127.0.0.1:8050")
print(f"Run:  python app.py")
