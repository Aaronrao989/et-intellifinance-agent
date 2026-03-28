from typing import List, Dict, Any

from app.config import settings


def get_rules() -> List[Dict[str, Any]]:
    """
    Returns a list of compliance rules.
    Each rule is a dictionary with:
    - name
    - description
    - condition (used in validator)
    """

    rules = [
        {
            "name": "MAX_TRANSACTION_LIMIT",
            "description": "Transaction amount should not exceed threshold",
            "threshold": settings.MAX_TRANSACTION_THRESHOLD,
            "type": "amount_check"
        },
        {
            "name": "NO_NEGATIVE_TRANSACTIONS",
            "description": "Transactions should not have negative amounts",
            "type": "negative_check"
        },
        {
            "name": "DUPLICATE_TRANSACTION_CHECK",
            "description": "Duplicate transactions are not allowed",
            "type": "duplicate_check"
        },
        {
            "name": "MISMATCH_TRANSACTION_CHECK",
            "description": "Mismatched transactions indicate inconsistency",
            "type": "mismatch_check"
        },
        {
            "name": "CURRENCY_CHECK",
            "description": "Only allowed currencies should be used",
            "allowed": settings.ALLOWED_CURRENCIES,
            "type": "currency_check"
        }
    ]

    return rules