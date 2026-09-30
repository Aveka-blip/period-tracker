"""
Simple Period Tracker
A beginner-friendly Python project.
Saves your period start dates to a file and predicts your next one.
"""

import json
from datetime import date, datetime, timedelta

DATA_FILE = "periods.json"


def load_dates():
    """Read saved dates from the file. Returns an empty list if none yet."""
    try:
        with open(DATA_FILE, "r") as file:
            text_dates = json.load(file)
        return [datetime.strptime(d, "%Y-%m-%d").date() for d in text_dates]
    except FileNotFoundError:
        return []


def save_dates(dates):
    """Save the dates list to the file as text."""
    text_dates = [d.strftime("%Y-%m-%d") for d in dates]
    with open(DATA_FILE, "w") as file:
        json.dump(text_dates, file)


def ask_for_date(prompt):
    """Ask for a date. Press Enter to use today."""
    while True:
        answer = input(prompt).strip()
        if answer == "":
            return date.today()
        try:
            return datetime.strptime(answer, "%Y-%m-%d").date()
        except ValueError:
            print("Oops! Please use the format YYYY-MM-DD (like 2026-09-30).")


def log_period(dates):
    """Add a new period start date."""
    new_date = ask_for_date("Period start date (YYYY-MM-DD, Enter = today): ")
    if new_date in dates:
        print("That date is already saved!")
        return
    dates.append(new_date)
    dates.sort()
    save_dates(dates)
    print(f"Saved {new_date}.")


def show_history(dates):
    """Print every saved date."""
    if not dates:
        print("No periods logged yet.")
        return
    print("\nYour logged period start dates:")
    for number, d in enumerate(dates, start=1):
        print(f"  {number}. {d.strftime('%B %d, %Y')}")


def get_cycle_lengths(dates):
    """Days between each period start and the next one."""
    lengths = []
    for i in range(1, len(dates)):
        lengths.append((dates[i] - dates[i - 1]).days)
    return lengths


def predict_next(dates):
    """Predict the next period using the average cycle length."""
    if len(dates) < 2:
        print("Log at least 2 periods so I can work out your cycle length.")
        return

    lengths = get_cycle_lengths(dates)
    average = round(sum(lengths) / len(lengths))
    next_date = dates[-1] + timedelta(days=average)
    days_left = (next_date - date.today()).days

    print(f"\nAverage cycle length: {average} days")
    print(f"Predicted next period: {next_date.strftime('%B %d, %Y')}")

    if days_left > 0:
        print(f"That's in {days_left} day(s).")
    elif days_left == 0:
        print("That's today!")
    else:
        print(f"That was {abs(days_left)} day(s) ago - it may be late or need logging.")


def delete_last(dates):
    """Remove the most recent entry (in case of a typo)."""
    if not dates:
        print("Nothing to delete.")
        return
    removed = dates.pop()
    save_dates(dates)
    print(f"Deleted {removed}.")


def main():
    dates = load_dates()

    while True:
        print("\n=== Period Tracker ===")
        print("1. Log a period")
        print("2. See history")
        print("3. Predict next period")
        print("4. Delete last entry")
        print("5. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            log_period(dates)
        elif choice == "2":
            show_history(dates)
        elif choice == "3":
            predict_next(dates)
        elif choice == "4":
            delete_last(dates)
        elif choice == "5":
            print("Bye! Take care :)")
            break
        else:
            print("Please pick a number from 1 to 5.")


if __name__ == "__main__":
    main()
