# Personal Budget Manager

This is a simple Python program for keeping track of income and expenses. I started with the `cli.py` example from class and used it as a base for the budget manager assignment.

You can add transactions, see what you have saved, check your balance, and make a backup of your data.

## What you need

- Python 3.10 or newer
- A terminal (like PowerShell or the terminal in VS Code)

You don't need to install any extra Python packages.

## How to use it

Open the `budget-manager` folder in your terminal. You can then try these commands:

```bash
python cli.py --help
python cli.py add expense 18.50 --category food --date 2026-09-04
python cli.py add income 2000 --category salary --date 2026-09-05
python cli.py list
python cli.py summary
```

The program saves your transactions in `data/transactions.csv`, so they are still there the next time you run it.

To create a backup, run:

```bash
python cli.py backup backups/backup-20260905.json
```

Use a new filename each time you make a backup, because the program won't replace an existing one.

## Example

The project includes some example transactions in `data/sample_transactions.csv`. To see their summary without changing your own saved transactions, run:

```bash
python cli.py --file data/sample_transactions.csv summary
```

For this example, the results should be:

- Income: EUR 2000.00
- Expenses: EUR 30.50
- Balance: EUR 1969.50

You can also replace `summary` with `list` to see the three example transactions.

## Testing

I included tests to check that the main parts of the program work correctly. Run them with:

```bash
python -m unittest discover -s tests -v
```

The six tests check saving and loading, invalid amounts, unknown categories, repeated IDs, invalid CSV data, and making backups safely.

You can also try the invalid example file:

```bash
python cli.py --file data/sample_invalid_transactions.csv list
```

This should give an error explaining which row has a problem.

## A few things to know

- Transactions can be either `income` or `expense`.
- The categories are: `entertainment`, `food`, `health`, `housing`, `other`, `salary`, `shopping`, and `transport`.
- Amounts must be greater than zero, and dates must use the `YYYY-MM-DD` format.
- The program only uses EUR, and each transaction gets its own ID.
- It checks for incorrect data instead of saving it.
- This is a basic student project. It doesn't support multiple users, automatic currency conversion, or undoing a transaction. Amounts are rounded to two decimal places.

## Project files

The main command is `cli.py`. The code in `src/budget_manager/` is split into smaller files for transactions, checking inputs, calculations, saving data, and the command-line interface.

I also included `DESIGN.md` to explain the structure and `AI_DISCLOSURE.md` to explain how AI was used.
