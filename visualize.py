"""
Personal Finance Tracker — visualisation module.

Generates spending-by-category pie chart, monthly income-vs-expense
bar chart, and a cumulative balance line chart using matplotlib.
"""

import matplotlib
matplotlib.use("Agg")  # non-interactive backend so it works headless
import matplotlib.pyplot as plt
from collections import defaultdict
from tracker import list_transactions, get_summary


def plot_spending_by_category(save_path: str = "spending_by_category.png") -> str:
    """Pie chart of total spend (expenses only) per category."""
    summary = get_summary()
    # Only negative amounts count as spending
    spending = {k: abs(v) for k, v in summary["by_category"].items() if v < 0}

    if not spending:
        print("No expenses recorded yet — nothing to plot.")
        return ""

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(spending.values(), labels=spending.keys(), autopct="%1.1f%%",
           startangle=140)
    ax.set_title("Spending by Category")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {save_path}")
    return save_path


def plot_monthly_income_expense(save_path: str = "monthly_income_expense.png") -> str:
    """Grouped bar chart: income vs expenses for each month."""
    transactions = list_transactions()
    if not transactions:
        print("No transactions recorded yet — nothing to plot.")
        return ""

    monthly_income: dict[str, float] = defaultdict(float)
    monthly_expense: dict[str, float] = defaultdict(float)

    for t in transactions:
        month_key = t["date"][:7]  # "YYYY-MM"
        if t["amount"] >= 0:
            monthly_income[month_key] += t["amount"]
        else:
            monthly_expense[month_key] += abs(t["amount"])

    months = sorted(set(monthly_income) | set(monthly_expense))
    incomes = [monthly_income.get(m, 0) for m in months]
    expenses = [monthly_expense.get(m, 0) for m in months]

    x = range(len(months))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar([i - width / 2 for i in x], incomes, width, label="Income", color="#2ecc71")
    ax.bar([i + width / 2 for i in x], expenses, width, label="Expenses", color="#e74c3c")
    ax.set_xticks(list(x))
    ax.set_xticklabels(months, rotation=45, ha="right")
    ax.set_ylabel("Amount ($)")
    ax.set_title("Monthly Income vs Expenses")
    ax.legend()
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {save_path}")
    return save_path


def plot_balance_over_time(save_path: str = "balance_over_time.png") -> str:
    """Line chart of cumulative balance ordered by date."""
    transactions = list_transactions()
    if not transactions:
        print("No transactions recorded yet — nothing to plot.")
        return ""

    sorted_txns = sorted(transactions, key=lambda t: t["date"])
    dates = [t["date"] for t in sorted_txns]
    cumulative = []
    running = 0.0
    for t in sorted_txns:
        running += t["amount"]
        cumulative.append(running)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, cumulative, marker="o", linewidth=2, color="#3498db")
    ax.fill_between(dates, cumulative, alpha=0.15, color="#3498db")
    ax.set_xlabel("Date")
    ax.set_ylabel("Balance ($)")
    ax.set_title("Cumulative Balance Over Time")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {save_path}")
    return save_path


if __name__ == "__main__":
    plot_spending_by_category()
    plot_monthly_income_expense()
    plot_balance_over_time()
