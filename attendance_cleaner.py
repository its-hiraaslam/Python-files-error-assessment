"""Student Attendance Cleaner.

Reads raw attendance names from attendance.txt, fixes spacing and
capitalisation, removes duplicates with a set, sorts the names A-Z and saves
the result to attendance_clean.csv.

Author: Hira Aslam | GitHub: hiraaslam-data
"""

import csv
import sys
from pathlib import Path

# ---------------------------------------------------------------- constants
BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "attendance.txt"
OUTPUT_FILE = BASE_DIR / "attendance_clean.csv"
CSV_HEADER = ["student_name"]


def read_lines(filename=INPUT_FILE):
    """Return the lines of the attendance file, or None if it cannot be read."""
    try:
        # utf-8-sig also removes the invisible BOM that Windows Notepad can add
        with open(filename, encoding="utf-8-sig") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: '{Path(filename).name}' was not found. Put it in the same folder as this script.")
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error: could not read '{Path(filename).name}' ({error}).")
    return None


def clean_names(lines):
    """Strip extra spaces and apply Title Case to every non-blank line."""
    # list comprehension: strip() trims the ends, split/join fixes spaces in the
    # middle, title() fixes capitalisation; blank lines are skipped.
    return [" ".join(line.strip().split()).title() for line in lines if line.strip()]


def save_clean_list(names, filename=OUTPUT_FILE):
    """Write the cleaned, sorted names to a CSV file (one name per row)."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)
            writer.writerows([name] for name in names)
    except OSError as error:
        print(f"Error: could not save '{Path(filename).name}' ({error}).")
        return False
    return True


def show_report(original_count, blank_count, unique_count, names):
    """Print the counts and the final attendance list."""
    print("\n===== Attendance Cleaning Report =====")
    print(f"Original records   : {original_count}")
    if blank_count:
        print(f"Blank lines ignored: {blank_count}")
    print(f"Unique students    : {unique_count}")
    print(f"Duplicates removed : {original_count - unique_count}")
    print("\nCleaned attendance list (A-Z):")
    for number, name in enumerate(names, start=1):
        print(f"{number:>3}. {name}")


def main():
    lines = read_lines()
    if lines is None:
        return 1

    cleaned = clean_names(lines)
    if not cleaned:
        print("The attendance file has no student names. Nothing to clean.")
        return 0

    unique_students = set(cleaned)          # a set keeps each name only once
    unique_count = len(unique_students)     # total number of unique students
    sorted_names = sorted(unique_students)  # alphabetical order

    if not save_clean_list(sorted_names):
        return 1

    show_report(len(cleaned), len(lines) - len(cleaned), unique_count, sorted_names)
    print(f"\nSaved cleaned list to {OUTPUT_FILE.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
