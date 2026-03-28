from typing import List, Dict, Any


def validate_rules(finance_result: Dict[str, Any], rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Applies rules dynamically on finance_result.
    Returns list of violations.
    """

    violations = []

    summary = finance_result.get("summary", {})
    anomalies = finance_result.get("anomalies", [])
    reconciliation = finance_result.get("reconciliation", {})

    total_amount = summary.get("total_amount", 0)

    for rule in rules:
        rule_type = rule.get("type")

        # RULE 1: Max transaction threshold
        if rule_type == "amount_check":
            threshold = rule.get("threshold", 0)
            if total_amount > threshold:
                violations.append({
                    "rule": rule["name"],
                    "reason": f"Total amount {total_amount} exceeds threshold {threshold}"
                })

        # RULE 2: Negative transactions
        elif rule_type == "negative_check":
            for anomaly in anomalies:
                if anomaly.get("type") == "NEGATIVE_AMOUNT":
                    violations.append({
                        "rule": rule["name"],
                        "reason": "Negative transaction detected",
                        "transaction_id": anomaly.get("transaction_id")
                    })

        # RULE 3: Duplicate transactions
        elif rule_type == "duplicate_check":
            if reconciliation.get("duplicate_count", 0) > 0:
                violations.append({
                    "rule": rule["name"],
                    "reason": "Duplicate transactions found",
                    "count": reconciliation.get("duplicate_count")
                })

        # RULE 4: Mismatch transactions
        elif rule_type == "mismatch_check":
            if reconciliation.get("mismatch_count", 0) > 0:
                violations.append({
                    "rule": rule["name"],
                    "reason": "Mismatched transactions found",
                    "count": reconciliation.get("mismatch_count")
                })

        # RULE 5: Currency check (if present)
        elif rule_type == "currency_check":
            # Only validate if currency column exists
            currency_list = finance_result.get("currency_list", [])

            allowed = rule.get("allowed", [])

            for currency in currency_list:
                if currency not in allowed:
                    violations.append({
                        "rule": rule["name"],
                        "reason": f"Unsupported currency detected: {currency}"
                    })

    return violations