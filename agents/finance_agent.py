import pandas as pd
from loguru import logger
from typing import Dict, Any

from tools.data_parser import parse_data
from tools.reconciliation import reconcile_transactions
from tools.anomaly_detector import detect_anomalies


class FinanceAgent:
    def __init__(self):
        pass

    def analyze(self, data) -> Dict[str, Any]:
        """
        Performs:
        1. Data Parsing
        2. Reconciliation
        3. Anomaly Detection
        4. Summary Generation
        """

        logger.info("📊 Finance Agent: Starting analysis")

        try:
            # STEP 1: Parse Data
            df = parse_data(data)

            if df.empty:
                raise ValueError("Input data is empty")

            # STEP 2: Reconciliation
            reconciliation_result = reconcile_transactions(df)

            # STEP 3: Anomaly Detection
            anomalies = detect_anomalies(df)

            # STEP 4: Summary Metrics
            total_transactions = len(df)
            total_amount = df["amount"].sum()

            summary = {
                "total_transactions": total_transactions,
                "total_amount": float(total_amount),
                "average_transaction": float(total_amount / total_transactions)
                if total_transactions > 0 else 0
            }

            logger.info("✅ Finance analysis complete")

            return {
                "status": "success",
                "summary": summary,
                "reconciliation": reconciliation_result,
                "anomalies": anomalies
            }

        except Exception as e:
            logger.error(f"❌ Finance Agent Error: {str(e)}")

            return {
                "status": "error",
                "message": str(e)
            }