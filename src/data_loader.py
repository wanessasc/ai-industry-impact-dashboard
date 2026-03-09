from pathlib import Path

import pandas as pd

from src.config import PROCESSED_DATA_PATH, RAW_DATA_PATH


def load_raw_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load raw CSV dataset."""
    dataset_path = Path(path) if path else RAW_DATA_PATH
    return pd.read_csv(dataset_path)


def load_processed_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load processed CSV dataset."""
    dataset_path = Path(path) if path else PROCESSED_DATA_PATH
    return pd.read_csv(dataset_path)


def save_processed_data(df: pd.DataFrame, path: str | Path | None = None) -> Path:
    """Persist processed dataset and return output path."""
    dataset_path = Path(path) if path else PROCESSED_DATA_PATH
    dataset_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(dataset_path, index=False)
    return dataset_path
