"""CSV persistence and verified, non-overwriting JSON backups."""
import csv
import hashlib
import json
from pathlib import Path
from .services import add_transaction

FIELDS = ["id", "date", "kind", "category", "amount", "currency"]


def load_transactions(path):
    path = Path(path)
    if not path.exists():
        return []
    records = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError("CSV must have columns: " + ", ".join(FIELDS))
        for line, record in enumerate(reader, start=2):
            try:
                records = add_transaction(records, record)
            except ValueError as error:
                raise ValueError(f"Row {line}: {error}") from None
    return records


def save_transactions(path, records):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write to a temporary file, then replace the dataset after a successful write.
    temporary = path.with_name(path.name + ".tmp")
    try:
        with temporary.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(records)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def backup_transactions(path, destination):
    """Create a JSON backup exclusively and verify the written bytes."""
    records = load_transactions(path)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(records, indent=2) + "\n").encode("utf-8")
    with destination.open("xb") as handle:
        handle.write(payload)
    if hashlib.sha256(destination.read_bytes()).digest() != hashlib.sha256(payload).digest():
        raise OSError("backup verification failed")
    return len(records)
