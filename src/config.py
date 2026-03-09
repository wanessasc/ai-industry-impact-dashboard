from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "ai_market_clean_v2.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "ai_market_clean_processed.csv"

PERCENT_COLUMNS_RAW = [
    "ai_adoption_rate_percent",
    "job_loss_dueto_ai_percent",
    "revenue_increase_due_to_ai_percent",
    "human_ai_collaboration_rate_percent",
    "consumer_trust_in_ai_percent",
    "market_share_of_ai_companies_percent",
]

COLUMN_RENAME_MAP = {
    "job_loss_dueto_ai_percent": "job_loss_due_to_ai_percent",
}

PERCENT_COLUMNS_CLEAN = [
    "ai_adoption_rate_percent",
    "job_loss_due_to_ai_percent",
    "revenue_increase_due_to_ai_percent",
    "human_ai_collaboration_rate_percent",
    "consumer_trust_in_ai_percent",
    "market_share_of_ai_companies_percent",
]

