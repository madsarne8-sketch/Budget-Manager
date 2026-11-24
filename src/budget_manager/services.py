"""Business logic without terminal input or file operations."""
from .validation import validate_transaction


def next_id(transactions):
    return f"T{max((int(t['id'][1:]) for t in transactions), default=0) + 1:03d}"


def add_transaction(transactions, record):
    cleaned = validate_transaction(record)
    if any(t["id"] == cleaned["id"] for t in transactions):
        raise ValueError(f"duplicate transaction id: {cleaned['id']}")
    return [*transactions, cleaned]


def filter_transactions(transactions, kind=None, category=None):
    return [t for t in transactions if (kind is None or t["kind"] == kind)
            and (category is None or t["category"] == category)]


def summary(transactions):
    income = round(sum(t["amount"] for t in transactions if t["kind"] == "income"), 2)
    expense = round(sum(t["amount"] for t in transactions if t["kind"] == "expense"), 2)
    by_category = {}
    for t in transactions:
        if t["kind"] == "expense":
            by_category[t["category"]] = round(by_category.get(t["category"], 0) + t["amount"], 2)
    return {"income": income, "expense": expense, "balance": round(income - expense, 2),
            "expense_by_category": by_category}
