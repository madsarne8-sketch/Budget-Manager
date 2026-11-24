"""Command-line interface adapted from the supplied classroom cli.py starter."""
import argparse
from datetime import date
import sys
from pathlib import Path
from .services import next_id, add_transaction, filter_transactions, summary
from .storage import load_transactions, save_transactions, backup_transactions
from .validation import CATEGORIES

DEFAULT_FILE = Path(__file__).resolve().parents[2] / "data" / "transactions.csv"


def build_parser():
    parser = argparse.ArgumentParser(description="Interactive Personal Budget Manager")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="CSV data file")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="Record an income or expense")
    add.add_argument("kind", choices=["expense", "income"])
    add.add_argument("amount", help="Positive amount in EUR")
    add.add_argument("--category", required=True, help="Category: " + ", ".join(sorted(CATEGORIES)))
    add.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    listed = commands.add_parser("list", help="Show transactions")
    listed.add_argument("--kind", choices=["expense", "income"])
    listed.add_argument("--category", choices=sorted(CATEGORIES))
    commands.add_parser("summary", help="Show total income, expenses and balance")
    backup = commands.add_parser("backup", help="Save verified JSON backup, without overwriting")
    backup.add_argument("destination", type=Path)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "backup":
            count = backup_transactions(args.file, args.destination)
            print(f"Backup created: {args.destination} ({count} transactions)")
            return 0
        records = load_transactions(args.file)
        if args.command == "add":
            record = {"id": next_id(records), "date": args.date, "kind": args.kind,
                      "category": args.category, "amount": args.amount, "currency": "EUR"}
            records = add_transaction(records, record)
            save_transactions(args.file, records)
            print(f"Added {record['id']}: {args.kind} EUR {float(args.amount):.2f} ({args.category.lower()})")
        elif args.command == "list":
            selected = filter_transactions(records, args.kind, args.category)
            if not selected:
                print("No transactions found.")
            for record in selected:
                print(f"{record['id']} | {record['date']} | {record['kind']:<7} | "
                      f"{record['category']:<13} | {record['amount']:.2f} {record['currency']}")
        elif args.command == "summary":
            result = summary(records)
            print(f"Income:   EUR {result['income']:.2f}")
            print(f"Expenses: EUR {result['expense']:.2f}")
            print(f"Balance:  EUR {result['balance']:.2f}")
            for category, amount in sorted(result["expense_by_category"].items()):
                print(f"  {category}: EUR {amount:.2f}")
        return 0
    except (ValueError, OSError, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
