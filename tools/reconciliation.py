import pandas as pd
from loguru import logger
from typing import Dict, Any


def reconcile_transactions(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs basic reconciliation:
    - Detect duplicate transactions
    - Identify unmatched transactions (simple heuristic)
    """

    logger.info("🔍 Running reconciliation...")

    try:
        # 1. Detect duplicates based on transaction_id
        duplicates = df[df.duplicated(subset=["transaction_id"], keep=False)]

        duplicate_ids = duplicates["transaction_id"].unique().tolist()

        # 2. Detect potential mismatches
        # Simple rule: same amount + same date but different IDs
        mismatch_groups = (
            df.groupby(["amount", "date"])
            .filter(lambda x: len(x) > 1)
        )

        mismatches = mismatch_groups[
            ~mismatch_groups["transaction_id"].isin(duplicate_ids)
        ]

        # 3. Summary
        total_transactions = len(df)
        duplicate_count = len(duplicate_ids)
        mismatch_count = len(mismatches)

        logger.info("✅ Reconciliation complete")

        return {
            "total_transactions": total_transactions,
            "duplicate_transactions": duplicate_ids,
            "duplicate_count": duplicate_count,
            "mismatched_transactions": mismatches.to_dict(orient="records"),
            "mismatch_count": mismatch_count,
        }

    except Exception as e:
        logger.error(f"❌ Reconciliation Error: {str(e)}")

        return {
            "status": "error",
            "message": str(e)
        }