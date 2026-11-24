"""Validate transaction data at input and file-import boundaries."""
from datetime import date
from math import isfinite

CATEGORIES = {"food", "housing", "transport", "shopping", "health", "entertainment", "salary", "other"}
KINDS = {"expense", "income"}


def validate_transaction(record):
    """Return a cleaned transaction or raise a descriptive ValueError."""
    required = {"id", "date", "kind", "category", "amount", "currency"}
    if not isinstance(record, dict) or set(record) != required:
        raise ValueError("transaction must contain exactly: id, date, kind, category, amount, currency")
    transaction_id = str(record["id"]).strip()
    if not transaction_id or not transaction_id.startswith("T") or not transaction_id[1:].isdigit():
        raise ValueError("id must have the format T001")
    day = str(record["date"]).strip()
    try:
        if date.fromisoformat(day).isoformat() != day:
            raise ValueError()
    except ValueError:
        raise ValueError("date must be a real date in YYYY-MM-DD format") from None
    kind = str(record["kind"]).strip().lower()
    if kind not in KINDS:
        raise ValueError("kind must be expense or income")
    category = str(record["category"]).strip().lower()
    if category not in CATEGORIES:
        raise ValueError("unknown category; choose: " + ", ".join(sorted(CATEGORIES)))
    try:
        amount = float(record["amount"])
    except (ValueError, TypeError):
        raise ValueError("amount must be a number greater than 0") from None
    if not isfinite(amount) or amount <= 0:
        raise ValueError("amount must be a finite number greater than 0")
    currency = str(record["currency"]).strip().upper()
    if currency != "EUR":
        raise ValueError("currency must be EUR (conversion is not supported)")
    return {"id": transaction_id, "date": day, "kind": kind,
            "category": category, "amount": round(amount, 2), "currency": currency}
