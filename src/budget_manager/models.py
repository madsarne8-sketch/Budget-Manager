"""Transaction record schema."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Transaction:
    id: str
    date: str
    kind: str
    category: str
    amount: float
    currency: str
