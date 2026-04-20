"""
Personal Finance Tracker — core data logic.

Stores transactions in a local JSON file and provides helpers
for adding, listing, filtering, and summarising spend by category.
"""

import json
import os
from datetime import datetime

DATA_FILE = "transactions.json"


def _load_transactions() -> list[dict]:
    """Load transactions from the JSON data file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def _save_transactions(transactions: list[dict]) -> None:
    """Persist the transaction list to disk."""
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=2)


def add_transaction(amount: float, category: str, description: str = "",
                    date: str | None = None) -> dict:
    """
    Record a new transaction.

    Parameters
    ----------
    amount : float
        Positive = income, negative = expense.
    category : str
        e.g. "Food", "Rent", "Salary".
    description : str
        Free-text note.
    date : str | None
        ISO date string (YYYY-MM-DD). Defaults to today.

    Returns
    -------
    dict   The newly created transaction record.
    """
    transactions = _load_transactions()
    record = {
        "id": len(transactions) + 1,
        "amount": round(amount, 2),
        "category": category,
        "description": description,
        "date": date or datetime.now().strftime("%Y-%m-%d"),
    }
    transactions.append(record)
    _save_transactions(transactions)
    return record


def list_transactions(category: str | None = None,
                      start_date: str | None = None,
                      end_date: str | None = None) -> list[dict]:
    """Return transactions, optionally filtered by category and/or date range."""
    transactions = _load_transactions()

    if category:
        category_lower = category.lower()
        transactions = [t for t in transactions
                        if t["category"].lower() == category_lower]

    if start_date:
        transactions = [t for t in transactions if t["date"] >= start_date]

    if end_date:
        transactions = [t for t in transactions if t["date"] <= end_date]

    return transactions


def get_summary() -> dict:
    """
    Summarise all transactions.

    Returns a dict with:
      total_income, total_expenses, net_balance,
      by_category  — {category: sum}
    """
    transactions = _load_transactions()
    total_income = sum(t["amount"] for t in transactions if t["amount"] > 0)
    total_expenses = sum(t["amount"] for t in transactions if t["amount"] < 0)

    by_category: dict[str, float] = {}
    for t in transactions:
        by_category[t["category"]] = (
            by_category.get(t["category"], 0) + t["amount"]
        )

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_balance": round(total_income + total_expenses, 2),
        "by_category": {k: round(v, 2) for k, v in by_category.items()},
    }


def delete_transaction(transaction_id: int) -> bool:
    """Delete a transaction by its id. Returns True if found and removed."""
    transactions = _load_transactions()
    original_len = len(transactions)
    transactions = [t for t in transactions if t["id"] != transaction_id]
    if len(transactions) < original_len:
        _save_transactions(transactions)
        return True
    return False
