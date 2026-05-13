# utils/data_loader.py

import logging
import pandas as pd
from config.settings import DATA_FILE, REQUIRED_COLUMNS

logger = logging.getLogger(__name__)


def load_data(filepath: str = DATA_FILE) -> pd.DataFrame:
    """Load weather CSV, validate columns, and return a clean DataFrame."""
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} rows from {filepath}")
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"Weather data file missing at {filepath}")
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        raise

    # Column validation
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Date parsing
    df["date"] = pd.to_datetime(df["date"])
    return df