import pandas as pd

from src.config import COLUMN_RENAME_MAP, PERCENT_COLUMNS_CLEAN, PERCENT_COLUMNS_RAW


def _normalize_percentage_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert percentage columns to 0-100 scale.
    Source values appear to be stored as hundredths (e.g., 4429 -> 44.29).
    """
    for col in PERCENT_COLUMNS_CLEAN:
        if col in df.columns and df[col].max() > 100:
            df[col] = df[col] / 100.0
        df[col] = df[col].clip(lower=0, upper=100)
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich AI market dataset."""
    cleaned = df.copy()
    cleaned = cleaned.rename(columns=COLUMN_RENAME_MAP)

    text_cols = [
        "country",
        "industry",
        "top_ai_tools_used",
        "regulation_status",
    ]
    for col in text_cols:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype(str).str.strip()

    for col in PERCENT_COLUMNS_RAW:
        new_col = COLUMN_RENAME_MAP.get(col, col)
        if new_col in cleaned.columns:
            cleaned[new_col] = pd.to_numeric(cleaned[new_col], errors="coerce")

    cleaned["year"] = pd.to_numeric(cleaned["year"], errors="coerce").astype("Int64")
    cleaned["ai_generated_content_volume_tbs_per_year"] = pd.to_numeric(
        cleaned["ai_generated_content_volume_tbs_per_year"], errors="coerce"
    )

    cleaned = cleaned.dropna().copy()
    cleaned = _normalize_percentage_columns(cleaned)

    cleaned["net_impact_percent"] = (
        cleaned["revenue_increase_due_to_ai_percent"]
        - cleaned["job_loss_due_to_ai_percent"]
    )
    cleaned["ai_maturity_score"] = (
        0.40 * cleaned["ai_adoption_rate_percent"]
        + 0.35 * cleaned["human_ai_collaboration_rate_percent"]
        + 0.25 * cleaned["consumer_trust_in_ai_percent"]
    ).round(2)

    cleaned["year"] = cleaned["year"].astype(int)
    cleaned = cleaned.sort_values(["year", "country", "industry"]).reset_index(drop=True)
    return cleaned
