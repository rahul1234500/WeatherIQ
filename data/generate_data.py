"""
SAVE THIS FILE AS: data/generate_data.py

Generates a rich synthetic weather dataset covering:
  - 20 cities (10 major + 10 Vidarbha region)
  - Date range: 2023-01-01 to 2026-05-13 (current year included)
  - Daily records per city

Usage:  python data/generate_data.py
"""

import pandas as pd
import numpy as np
import os

# ── Conditions ────────────────────────────────────────────────────────────────
CONDITIONS   = ["Sunny", "Cloudy", "Rainy", "Stormy", "Foggy", "Windy", "Partly Cloudy"]
COND_WEIGHTS = [0.28,    0.22,     0.18,    0.08,     0.07,    0.07,    0.10]

# ── City climate profiles (realistic India values) ────────────────────────────
# Keys: temp_mean, temp_std, humid_mean, wind_mean, pressure_mean
CITY_PROFILE = {
    # ── Major metro cities ────────────────────────────────────────────────────
    "Delhi":      {"temp_mean": 27, "temp_std": 9,  "humid_mean": 55, "wind_mean": 12, "pressure_mean": 1008},
    "Mumbai":     {"temp_mean": 30, "temp_std": 4,  "humid_mean": 72, "wind_mean": 14, "pressure_mean": 1010},
    "Bengaluru":  {"temp_mean": 24, "temp_std": 4,  "humid_mean": 60, "wind_mean": 10, "pressure_mean": 1014},
    "Chennai":    {"temp_mean": 31, "temp_std": 3,  "humid_mean": 70, "wind_mean": 16, "pressure_mean": 1007},
    "Kolkata":    {"temp_mean": 28, "temp_std": 6,  "humid_mean": 68, "wind_mean": 11, "pressure_mean": 1009},
    "Hyderabad":  {"temp_mean": 28, "temp_std": 5,  "humid_mean": 58, "wind_mean": 12, "pressure_mean": 1011},
    "Pune":       {"temp_mean": 25, "temp_std": 5,  "humid_mean": 57, "wind_mean": 11, "pressure_mean": 1013},
    "Jaipur":     {"temp_mean": 28, "temp_std": 10, "humid_mean": 42, "wind_mean": 13, "pressure_mean": 1007},
    "Ahmedabad":  {"temp_mean": 30, "temp_std": 8,  "humid_mean": 45, "wind_mean": 14, "pressure_mean": 1006},
    "Lucknow":    {"temp_mean": 26, "temp_std": 9,  "humid_mean": 58, "wind_mean": 10, "pressure_mean": 1009},

    # ── Vidarbha region (central Maharashtra — hot, semi-arid) ───────────────
    "Nagpur":     {"temp_mean": 31, "temp_std": 9,  "humid_mean": 50, "wind_mean": 11, "pressure_mean": 1006},
    "Amravati":   {"temp_mean": 31, "temp_std": 9,  "humid_mean": 48, "wind_mean": 10, "pressure_mean": 1007},
    "Wardha":     {"temp_mean": 31, "temp_std": 9,  "humid_mean": 49, "wind_mean": 10, "pressure_mean": 1007},
    "Chandrapur": {"temp_mean": 32, "temp_std": 9,  "humid_mean": 52, "wind_mean": 10, "pressure_mean": 1006},
    "Akola":      {"temp_mean": 32, "temp_std": 10, "humid_mean": 46, "wind_mean": 11, "pressure_mean": 1006},
    "Yavatmal":   {"temp_mean": 31, "temp_std": 9,  "humid_mean": 50, "wind_mean": 10, "pressure_mean": 1007},
    "Bhandara":   {"temp_mean": 30, "temp_std": 8,  "humid_mean": 54, "wind_mean": 9,  "pressure_mean": 1007},
    "Gondia":     {"temp_mean": 30, "temp_std": 8,  "humid_mean": 55, "wind_mean": 9,  "pressure_mean": 1008},
    "Washim":     {"temp_mean": 31, "temp_std": 9,  "humid_mean": 47, "wind_mean": 10, "pressure_mean": 1007},
    "Gadchiroli": {"temp_mean": 31, "temp_std": 9,  "humid_mean": 56, "wind_mean": 9,  "pressure_mean": 1007},
}

# ── Date range: 2023-01-01 to today (2026-05-13) ─────────────────────────────
DATE_START = "2023-01-01"
DATE_END   = "2026-05-13"

np.random.seed(42)
date_range = pd.date_range(DATE_START, DATE_END, freq="D")

records = []
for city, p in CITY_PROFILE.items():
    n          = len(date_range)
    month_arr  = date_range.month

    # Seasonal sinusoidal temperature variation (peaks in May-June for India)
    season_factor = np.sin((month_arr - 3) * np.pi / 6)

    temps      = (p["temp_mean"]
                  + season_factor * (p["temp_std"] * 1.5)
                  + np.random.normal(0, p["temp_std"] * 0.4, n))
    humidities = np.clip(
        p["humid_mean"] - season_factor * 10 + np.random.normal(0, 8, n),
        20, 100
    )
    winds     = np.clip(p["wind_mean"] + np.random.normal(0, 4, n), 0, 80)
    pressures = np.clip(p["pressure_mean"] + np.random.normal(0, 5, n), 980, 1040)
    conditions = np.random.choice(CONDITIONS, size=n, p=COND_WEIGHTS)

    df_city = pd.DataFrame({
        "date":        date_range.strftime("%Y-%m-%d"),
        "city":        city,
        "temperature": temps.round(1),
        "humidity":    humidities.round(1),
        "wind_speed":  winds.round(1),
        "pressure":    pressures.round(1),
        "condition":   conditions,
    })
    records.append(df_city)

# Combine and sort
df = pd.concat(records, ignore_index=True).sort_values(["date", "city"])

# ── Save ──────────────────────────────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(__file__), "weather.csv")
df.to_csv(out_path, index=False)

years = sorted(df["date"].str[:4].unique().tolist())
print(f"[OK] Generated {len(df):,} rows -> {out_path}")
print(f"     Cities : {len(CITY_PROFILE)} ({', '.join(sorted(CITY_PROFILE)[:5])}...)")
print(f"     Years  : {years}")
print(f"     Dates  : {DATE_START} to {DATE_END}")
print()
print(df.head(3).to_string(index=False))
