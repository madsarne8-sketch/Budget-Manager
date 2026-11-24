"""Normal, boundary, malformed-file and persistence tests."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from budget_manager.services import add_transaction, summary
from budget_manager.storage import load_transactions, save_transactions, backup_transactions

GOOD = {"id": "T001", "date": "2026-09-04", "kind": "expense", "category": "food", "amount": 18.50, "currency": "EUR"}


class BudgetTests(unittest.TestCase):
    def test_normal_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            records = add_transaction([], GOOD)
            save_transactions(path, records)
            self.assertEqual(load_transactions(path), records)
            self.assertEqual(summary(records)["expense"], 18.50)

    def test_negative_amount_rejected(self):
        with self.assertRaisesRegex(ValueError, "greater than 0"):
            add_transaction([], {**GOOD, "amount": -1})

    def test_unknown_category_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown category"):
            add_transaction([], {**GOOD, "category": "mystery"})

    def test_duplicate_id_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate transaction id"):
            add_transaction([GOOD], GOOD)

    def test_invalid_csv_has_row_number(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("id,date,kind,category,amount,currency\nT001,2026-09-04,expense,food,-2,EUR\n")
            with self.assertRaisesRegex(ValueError, "Row 2"):
                load_transactions(path)

    def test_backup_matches_data_and_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / "data.csv", Path(directory) / "backup.json"
            save_transactions(source, [GOOD])
            self.assertEqual(backup_transactions(source, target), 1)
            self.assertIn('"id": "T001"', target.read_text())
            with self.assertRaises(FileExistsError):
                backup_transactions(source, target)


if __name__ == "__main__":
    unittest.main()
