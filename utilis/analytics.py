# utils/analytics.py

import pandas as pd
import numpy as np
from config.settings import MOVING_AVG_WINDOW


def compute_kpis(df: pd.DataFrame) -> dict:
    """Return key performance indicators as a dict."""
    return {
        "avg_temp":     round(df["temperature"].mean(), 1),
        "max_temp":     round(df["temperature"].max(), 1),
        "min_temp":     round(df["temperature"].min(), 1),
        "avg_humidity": round(df["humidity"].mean(), 1),
        "avg_wind":     round(df["wind_speed"].mean(), 1),
        "total_records": len(df),
    }


def temperature_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Daily average temperature grouped across selected cities."""
    return (
        df.groupby("date")["temperature"]
        .mean()
        .reset_index()
        .rename(columns={"temperature": "avg_temp"})
        .sort_values("date")
    )


def moving_average(df: pd.DataFrame) -> pd.DataFrame:
    """7-day rolling average on daily temperature."""
    trend = temperature_trend(df)
    trend["moving_avg"] = trend["avg_temp"].rolling(window=MOVING_AVG_WINDOW, min_periods=1).mean()
    return trend


def monthly_insights(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly avg temperature, humidity, wind speed."""
    return (
        df.groupby(["year", "month", "month_name"])
        .agg(avg_temp=("temperature", "mean"),
             avg_humidity=("humidity", "mean"),
             avg_wind=("wind_speed", "mean"))
        .round(2)
        .reset_index()
        .sort_values(["year", "month"])
    )


def condition_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """Return condition name and count, sorted descending."""
    counts = df["condition"].value_counts().reset_index()
    counts.columns = ["condition", "count"]
    return counts


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["temperature", "humidity", "wind_speed", "pressure"]
    return df[cols].corr().round(3)


def anomalies(df: pd.DataFrame) -> pd.DataFrame:
    flag_cols = [c for c in df.columns if c.endswith("_outlier")]
    mask = df[flag_cols].any(axis=1)
    return df[mask].copy()