import pandas as pd
from loguru import logger
from typing import Union


REQUIRED_COLUMNS = ["transaction_id", "amount", "date"]


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names to lowercase and trims spaces
    """
    df.columns = [col.strip().lower() for col in df.columns]
    return df


def validate_columns(df: pd.DataFrame):
    """
    Ensures required columns exist
    """
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning:
    - Remove nulls
    - Convert amount to float
    - Parse date
    """
    df = df.dropna(subset=["transaction_id", "amount"])

    # Convert amount
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Drop rows where amount conversion failed
    df = df.dropna(subset=["amount"])

    # Convert date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df


def parse_data(data: Union[str, dict, pd.DataFrame]) -> pd.DataFrame:
    """
    Accepts:
    - File path (CSV)
    - Dictionary (list of records)
    - Pandas DataFrame

    Returns:
    - Cleaned Pandas DataFrame
    """

    logger.info("📂 Parsing input data...")

    try:
        # CASE 1: File path
        if isinstance(data, str):
            df = pd.read_csv(data)

        # CASE 2: Dict / JSON-like
        elif isinstance(data, dict):
            df = pd.DataFrame(data)

        # CASE 3: Already DataFrame
        elif isinstance(data, pd.DataFrame):
            df = data.copy()

        else:
            raise ValueError("Unsupported data format")

        # Standardize
        df = standardize_columns(df)

        # Validate
        validate_columns(df)

        # Clean
        df = clean_data(df)

        logger.info(f"✅ Data parsed successfully: {len(df)} records")

        return df

    except Exception as e:
        logger.error(f"❌ Data Parsing Error: {str(e)}")
        raise