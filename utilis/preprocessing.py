# utils/preprocessing.py
# SAVE THIS FILE AS: utilis/preprocessing.py

import logging
import numpy as np
import pandas as pd
from config.settings import OUTLIER_Z_THRESHOLD

logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates, fill missing values, optimise dtypes.
    Handles mixed-year datasets (2023, 2024, 2025, 2026) safely.
    """
    original_len = len(df)

    # 1. Drop exact duplicates
    df = df.drop_duplicates()
    logger.info(f"Removed {original_len - len(df)} duplicate rows")

    # 2. Ensure date column is properly parsed (safe for any valid date string)
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 3. Drop rows with unparseable dates
    bad_dates = df["date"].isna().sum()
    if bad_dates > 0:
        logger.warning(f"Dropped {bad_dates} rows with invalid dates")
        df = df.dropna(subset=["date"])

    # 4. Fill numeric NaNs with city-level median
    numeric_cols = ["temperature", "humidity", "wind_speed", "pressure"]
    for col in numeric_cols:
        df[col] = df.groupby("city")[col].transform(lambda s: s.fillna(s.median()))

    # 5. Fill remaining NaNs (edge case: whole city missing)
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # 6. Dtype optimisation
    df["city"]      = df["city"].astype("category")
    df["condition"] = df["condition"].astype("category")

    logger.info(f"Clean dataset: {len(df)} rows")
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer time and analytical features. Safe for all years including 2026."""
    df = df.copy()

    # Time features
    df["year"]       = df["date"].dt.year.astype(int)
    df["month"]      = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%B")
    df["day_of_week"]= df["date"].dt.day_name()
    df["quarter"]    = df["date"].dt.quarter
    df["season"]     = df["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3:  "Spring", 4: "Spring", 5: "Spring",
        6:  "Summer", 7: "Summer", 8: "Summer",
        9:  "Autumn", 10: "Autumn", 11: "Autumn",
    })

    # Temperature category
    df["temp_category"] = pd.cut(
        df["temperature"],
        bins=[-np.inf, 15, 25, 35, np.inf],
        labels=["Cold", "Mild", "Warm", "Hot"],
    )

    # Outlier flag (z-score per city)
    for col in ["temperature", "humidity", "wind_speed"]:
        z = (df[col] - df.groupby("city")[col].transform("mean")) / \
             df.groupby("city")[col].transform("std")
        df[f"{col}_outlier"] = z.abs() > OUTLIER_Z_THRESHOLD

    return df


def apply_filters(
    df: pd.DataFrame,
    cities=None,
    conditions=None,
    temp_range=None,
    humidity_range=None,
    date_range=None,
    years=None,          # NEW: year list filter (e.g. [2023, 2024, 2026])
) -> pd.DataFrame:
    """Apply user-selected dashboard filters to the dataframe.
    All parameters are optional; omitting any means no filter on that dimension.
    """
    if cities:
        df = df[df["city"].isin(cities)]
    if conditions:
        df = df[df["condition"].isin(conditions)]
    if years:
        df = df[df["year"].isin([int(y) for y in years])]
    if temp_range and len(temp_range) == 2:
        df = df[df["temperature"].between(*temp_range)]
    if humidity_range and len(humidity_range) == 2:
        df = df[df["humidity"].between(*humidity_range)]
    if date_range and len(date_range) == 2:
        try:
            df = df[df["date"].between(
                pd.Timestamp(date_range[0]),
                pd.Timestamp(date_range[1]),
            )]
        except Exception:
            pass   # silently ignore unparseable date strings
    return df