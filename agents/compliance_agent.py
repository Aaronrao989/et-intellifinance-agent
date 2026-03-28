from loguru import logger
from typing import Dict, Any, List

from compliance.rules import get_rules
from compliance.validator import validate_rules


class ComplianceAgent:
    def __init__(self):
        self.rules = get_rules()

    def validate(self, finance_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies compliance rules on finance results:
        - Checks anomalies
        - Checks reconciliation issues
        - Enforces financial constraints
        """

        logger.info("⚖️ Compliance Agent: Validating results...")

        try:
            violations = []

            # Extract relevant data
            anomalies = finance_result.get("anomalies", [])
            reconciliation = finance_result.get("reconciliation", {})

            # RULE CHECK 1: Anomalies
            if anomalies:
                for anomaly in anomalies:
                    violations.append({
                        "type": "ANOMALY",
                        "detail": anomaly
                    })

            # RULE CHECK 2: Duplicate Transactions
            duplicate_count = reconciliation.get("duplicate_count", 0)
            if duplicate_count > 0:
                violations.append({
                    "type": "DUPLICATE_TRANSACTIONS",
                    "count": duplicate_count,
                    "reason": "Duplicate transaction IDs detected"
                })

            # RULE CHECK 3: Mismatched Transactions
            mismatch_count = reconciliation.get("mismatch_count", 0)
            if mismatch_count > 0:
                violations.append({
                    "type": "MISMATCHED_TRANSACTIONS",
                    "count": mismatch_count,
                    "reason": "Potential inconsistencies in transaction data"
                })

            # RULE CHECK 4: External rule validation (extensible)
            rule_violations = validate_rules(finance_result, self.rules)
            violations.extend(rule_violations)

            # FINAL DECISION
            is_compliant = len(violations) == 0

            logger.info(f"✅ Compliance check complete | Compliant: {is_compliant}")

            return {
                "status": "success",
                "is_compliant": is_compliant,
                "violations": violations,
                "total_violations": len(violations)
            }

        except Exception as e:
            logger.error(f"❌ Compliance Agent Error: {str(e)}")

            return {
                "status": "error",
                "is_compliant": False,
                "message": str(e)
            }