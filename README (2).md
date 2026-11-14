# Python Files & Errors Assessment

Two small management tools for a training institute, built with Python file handling, exception handling, sets, and comprehensions.

## Overview

| Program | Purpose |
|---|---|
| `expense_tracker.py` | Records daily operational expenses (stationery, internet, refreshments, transport) in `expenses.csv` and reports totals by category. |
| `attendance_cleaner.py` | Cleans `attendance.txt` (duplicates, messy capitalization, extra spaces) and saves a sorted list to `attendance_clean.csv`. |

## How to Run

Requires Python 3.8+. No extra libraries needed.

```bash
# Expense Tracker
python expense_tracker.py

# Attendance Cleaner (attendance.txt must be in the same folder)
python attendance_cleaner.py
```

**Expense Tracker menu:** 1. Add New Expense · 2. Show All Expenses · 3. Calculate Total Expenses by Category · 4. Exit

## Errors Handled and Why

| Error | Where | Why |
|---|---|---|
| `FileNotFoundError` | `expense_tracker.py` on startup | On the first run `expenses.csv` doesn't exist yet. The program starts with an empty list instead of crashing. |
| `ValueError` | Amount input | Text like `abc` can't convert to a number. The program shows a message and asks again. Negative amounts are rejected too. |
| `ValueError` | Date input | Dates must be `YYYY-MM-DD` so records stay consistent. |
| `FileNotFoundError` | `attendance_cleaner.py` | If `attendance.txt` is missing, a clear message is shown instead of a traceback. |

## Sets and List Comprehensions

**Sets**
- Expense Tracker: `{e["category"] for e in expenses}` gives each category once, even if used many times.
- Attendance Cleaner: `set(cleaned)` removes duplicate names, and `len()` of it gives the unique student count.

**List comprehension**
- `[" ".join(line.strip().title().split()) for line in lines if line.strip()]` cleans every name in one line: `strip()` removes outer spaces, `title()` fixes capitalization, and blank lines are skipped. The `split()`/`join()` part also fixes extra spaces *between* words.

## Sample Run: Data Saved and Loaded Again

**Run 1** (no `expenses.csv` yet): add two expenses, including invalid amounts first.

```
No saved expenses found. Starting with an empty list.
Choose an option (1-4): 1
Date (YYYY-MM-DD): 2026-11-10
Item name: A4 Paper
Category: stationery
Amount: abc
Invalid amount. Please enter a valid positive number.
Amount: -5
Invalid amount. Please enter a valid positive number.
Amount: 1500
Expense added and saved.
Choose an option (1-4): 1
Date (YYYY-MM-DD): 2026-11-11
Item name: Internet Bill
Category: Utilities
Amount: 4500.50
Expense added and saved.
Choose an option (1-4): 4
Goodbye!
```

**Run 2** (program restarted): the data is loaded from the file.

```
Choose an option (1-4): 2

Date        Item                Category           Amount
---------------------------------------------------------
2026-11-10  A4 Paper            Stationery        1500.00
2026-11-11  Internet Bill       Utilities         4500.50

Unique categories: Stationery, Utilities

Choose an option (1-4): 3
Total expenses by category:
  Stationery        1500.00
  Utilities         4500.50
  GRAND TOTAL       6000.50
```

`expenses.csv` after the run:

```
date,item,category,amount
2026-11-10,A4 Paper,Stationery,1500.0
2026-11-11,Internet Bill,Utilities,4500.5
```

**Attendance Cleaner output** (10 raw records with duplicates):

```
Original records : 10
Unique students  : 6

Cleaned attendance list:
  1. Ali Raza
  2. Ayesha Noor
  3. Bilal Hussain
  4. Hira Aslam
  5. Sara Khan
  6. Usman Ahmed

Saved to attendance_clean.csv
```
