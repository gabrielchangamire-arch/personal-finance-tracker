"""
Personal Finance Tracker — CLI entry point.

Run:  python main.py
"""

from tracker import add_transaction, list_transactions, get_summary, delete_transaction
from visualize import plot_spending_by_category, plot_monthly_income_expense, plot_balance_over_time


def print_menu():
    print("\n===== Personal Finance Tracker =====")
    print("1. Add transaction")
    print("2. View all transactions")
    print("3. View transactions by category")
    print("4. View summary")
    print("5. Generate charts")
    print("6. Delete a transaction")
    print("7. Exit")
    print("====================================")


def handle_add():
    print("\n-- Add Transaction --")
    try:
        amount = float(input("Amount (negative for expense, positive for income): "))
    except ValueError:
        print("Invalid amount.")
        return
    category = input("Category (e.g. Food, Rent, Salary): ").strip()
    if not category:
        print("Category is required.")
        return
    description = input("Description (optional): ").strip()
    date = input("Date (YYYY-MM-DD, leave blank for today): ").strip() or None

    record = add_transaction(amount, category, description, date)
    print(f"Added: id={record['id']}  ${record['amount']:+.2f}  "
          f"[{record['category']}]  {record['date']}")


def handle_list(category=None):
    transactions = list_transactions(category=category)
    if not transactions:
        label = f" in '{category}'" if category else ""
        print(f"No transactions found{label}.")
        return
    print(f"\n{'ID':>4}  {'Date':<12} {'Amount':>10}  {'Category':<14} Description")
    print("-" * 65)
    for t in transactions:
        print(f"{t['id']:>4}  {t['date']:<12} ${t['amount']:>+9.2f}  "
              f"{t['category']:<14} {t['description']}")


def handle_summary():
    s = get_summary()
    print("\n-- Financial Summary --")
    print(f"  Total income:   ${s['total_income']:>10.2f}")
    print(f"  Total expenses: ${s['total_expenses']:>10.2f}")
    print(f"  Net balance:    ${s['net_balance']:>10.2f}")
    print("\n  Breakdown by category:")
    for cat, total in sorted(s["by_category"].items()):
        print(f"    {cat:<16} ${total:>+10.2f}")


def handle_charts():
    print("\nGenerating charts...")
    plot_spending_by_category()
    plot_monthly_income_expense()
    plot_balance_over_time()
    print("Done. Check the PNG files in the current directory.")


def handle_delete():
    try:
        tid = int(input("Transaction ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return
    if delete_transaction(tid):
        print(f"Transaction {tid} deleted.")
    else:
        print(f"Transaction {tid} not found.")


def main():
    while True:
        print_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            handle_add()
        elif choice == "2":
            handle_list()
        elif choice == "3":
            cat = input("Category to filter: ").strip()
            handle_list(category=cat)
        elif choice == "4":
            handle_summary()
        elif choice == "5":
            handle_charts()
        elif choice == "6":
            handle_delete()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice — enter 1-7.")


if __name__ == "__main__":
    main()
