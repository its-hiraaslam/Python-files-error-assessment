"""Institute Expense Tracker.

Records daily operational expenses (stationery, internet, refreshments,
transport, ...) in expenses.csv so the data survives between runs.

Author: Hira Aslam | GitHub: hiraaslam-data
"""

import csv
import math
from datetime import date, datetime
from pathlib import Path

# ---------------------------------------------------------------- constants
DATA_FILE = Path(__file__).with_name("expenses.csv")  # saved next to this script
FIELDNAMES = ["date", "item", "category", "amount"]
DATE_FORMAT = "%Y-%m-%d"

CHOICE_ADD = "1"
CHOICE_SHOW = "2"
CHOICE_TOTALS = "3"
CHOICE_EXIT = "4"

MENU = (
    "\n===== Institute Expense Tracker =====\n"
    "1. Add New Expense\n"
    "2. Show All Expenses\n"
    "3. Calculate Total Expenses by Category\n"
    "4. Exit"
)


# ------------------------------------------------------------ file handling
def load_expenses(filename=DATA_FILE):
    """Load saved expenses from the CSV file and return them as a list of dicts.

    A missing file is not an error for the user: FileNotFoundError is caught
    and the program starts with an empty list. Damaged rows are skipped.
    """
    expenses = []
    skipped = 0
    try:
        with open(filename, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                try:
                    expense_date = (row["date"] or "").strip()
                    item = (row["item"] or "").strip()
                    category = (row["category"] or "").strip().title()
                    amount = parse_amount(row["amount"])
                    if not (expense_date and item and category):
                        raise ValueError("empty field")
                except (KeyError, TypeError, ValueError):
                    skipped += 1  # row is damaged: keep going with the rest
                    continue
                expenses.append(
                    {"date": expense_date, "item": item,
                     "category": category, "amount": amount}
                )
    except FileNotFoundError:
        print(f"No saved file found ({Path(filename).name}). Starting with an empty expense list.")
        return []
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error: could not read {Path(filename).name} ({error}). Starting with an empty list.")
        return []

    print(f"Loaded {len(expenses)} expense(s) from {Path(filename).name}.")
    if skipped:
        print(f"Warning: {skipped} damaged row(s) were skipped.")
    return expenses


def save_expense(expense, filename=DATA_FILE):
    """Append one expense to the CSV file (the header is written once)."""
    path = Path(filename)
    needs_header = not path.exists() or path.stat().st_size == 0
    with open(path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if needs_header:
            writer.writeheader()
        writer.writerow({**expense, "amount": f"{expense['amount']:.2f}"})


# --------------------------------------------------------- input validation
def parse_amount(text):
    """Convert text to a positive, finite number or raise ValueError."""
    value = float(text)  # raises ValueError for "abc", "", "1,500", ...
    if not math.isfinite(value) or value <= 0:
        raise ValueError("amount must be a positive number")
    return value


def get_text(prompt):
    """Ask until the user types something that is not empty."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("This field cannot be empty. Please try again.")


def get_date(prompt):
    """Ask for a date in YYYY-MM-DD format; pressing Enter uses today's date."""
    while True:
        text = input(prompt).strip()
        if not text:
            return date.today().strftime(DATE_FORMAT)
        try:
            return datetime.strptime(text, DATE_FORMAT).strftime(DATE_FORMAT)
        except ValueError:
            print("Invalid date. Please use the format YYYY-MM-DD (for example 2026-11-19).")


def get_amount(prompt):
    """Ask until the user enters a valid positive number (ValueError is caught)."""
    while True:
        try:
            return parse_amount(input(prompt))
        except ValueError:
            print("Invalid amount. Please enter a positive number (for example 1500 or 249.50).")


# -------------------------------------------------------------- menu actions
def add_expense(expenses):
    """Collect a new expense from the user, save it, then add it to the list."""
    print("\n--- Add New Expense ---")
    expense = {
        "date": get_date("Date (YYYY-MM-DD, Enter for today): "),
        "item": get_text("Item name: "),
        "category": get_text("Category (e.g. Stationery, Internet): ").title(),
        "amount": get_amount("Amount: "),
    }
    try:
        save_expense(expense)
    except OSError as error:
        print(f"Error: the expense could not be saved ({error}).")
        return
    expenses.append(expense)
    print(f"Expense saved to {DATA_FILE.name}.")


def get_categories(expenses):
    """Return the unique categories as a set (duplicates disappear automatically)."""
    return {expense["category"] for expense in expenses}


def show_expenses(expenses):
    """Print every expense in a table, then the unique categories."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    item_width = max(len("Item"), *(len(e["item"]) for e in expenses))
    cat_width = max(len("Category"), *(len(e["category"]) for e in expenses))
    header = f"{'No':>3}  {'Date':<10}  {'Item':<{item_width}}  {'Category':<{cat_width}}  {'Amount':>10}"

    print("\n--- All Expenses ---")
    print(header)
    print("-" * len(header))
    for number, e in enumerate(expenses, start=1):
        print(f"{number:>3}  {e['date']:<10}  {e['item']:<{item_width}}  "
              f"{e['category']:<{cat_width}}  {e['amount']:>10,.2f}")

    categories = get_categories(expenses)
    print(f"\nUnique categories ({len(categories)}): {', '.join(sorted(categories))}")


def show_totals(expenses):
    """Print the total amount spent in each category and the grand total."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    # one pass per category: dictionary comprehension over the set of categories
    totals = {
        category: sum(e["amount"] for e in expenses if e["category"] == category)
        for category in sorted(get_categories(expenses))
    }

    print("\n--- Total Expenses by Category ---")
    for category, total in totals.items():
        print(f"{category:<20} {total:>12,.2f}")
    print("-" * 33)
    print(f"{'Grand total':<20} {sum(totals.values()):>12,.2f}")


# ---------------------------------------------------------------------- main
def main():
    expenses = load_expenses()
    while True:
        print(MENU)
        choice = input("Enter your choice (1-4): ").strip()
        if choice == CHOICE_ADD:
            add_expense(expenses)
        elif choice == CHOICE_SHOW:
            show_expenses(expenses)
        elif choice == CHOICE_TOTALS:
            show_totals(expenses)
        elif choice == CHOICE_EXIT:
            print("Goodbye! All expenses are saved in", DATA_FILE.name)
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # every expense is saved the moment it is added, so nothing is lost
        print("\nProgram closed. Saved expenses are safe in", DATA_FILE.name)
