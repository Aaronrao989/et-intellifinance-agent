import pandas as pd
from loguru import logger
from typing import List, Dict, Any

from app.config import settings


def detect_anomalies(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Detect anomalies using rule-based logic:
    - High-value transactions
    - Negative amounts
    - Suspicious frequency (same date clustering)
    """

    logger.info("🚨 Detecting anomalies...")

    anomalies = []

    try:
        # RULE 1: High-value transactions
        high_value = df[df["amount"] > settings.MAX_TRANSACTION_THRESHOLD]

        for _, row in high_value.iterrows():
            anomalies.append({
                "transaction_id": row["transaction_id"],
                "type": "HIGH_VALUE",
                "reason": f"Amount exceeds threshold ({settings.MAX_TRANSACTION_THRESHOLD})",
                "amount": float(row["amount"])
            })

        # RULE 2: Negative transactions
        negative_txns = df[df["amount"] < 0]

        for _, row in negative_txns.iterrows():
            anomalies.append({
                "transaction_id": row["transaction_id"],
                "type": "NEGATIVE_AMOUNT",
                "reason": "Transaction amount is negative",
                "amount": float(row["amount"])
            })

        # RULE 3: Suspicious frequency (many txns on same date)
        date_counts = df["date"].value_counts()
        suspicious_dates = date_counts[date_counts > 5].index  # threshold = 5

        suspicious_txns = df[df["date"].isin(suspicious_dates)]

        for _, row in suspicious_txns.iterrows():
            anomalies.append({
                "transaction_id": row["transaction_id"],
                "type": "FREQUENCY_SPIKE",
                "reason": "Too many transactions on same date",
                "date": str(row["date"])
            })

        logger.info(f"✅ Anomaly detection complete: {len(anomalies)} anomalies found")

        return anomalies

    except Exception as e:
        logger.error(f"❌ Anomaly Detection Error: {str(e)}")

        return [{
            "type": "ERROR",
            "reason": str(e)
        }]