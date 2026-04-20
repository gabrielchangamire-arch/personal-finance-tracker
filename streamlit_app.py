"""
Personal Finance Tracker — Streamlit web interface.

Run:  streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from tracker import add_transaction, list_transactions, get_summary, delete_transaction

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")
st.title("Personal Finance Tracker")

# ── Sidebar: Add Transaction ────────────────────────────────────────
st.sidebar.header("Add Transaction")
with st.sidebar.form("add_form", clear_on_submit=True):
    tx_type = st.selectbox("Type", ["Expense", "Income"])
    amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
    category = st.text_input("Category", placeholder="e.g. Food, Rent, Salary")
    description = st.text_input("Description (optional)", placeholder="e.g. Weekly groceries")
    date = st.date_input("Date")
    submitted = st.form_submit_button("Add")

    if submitted:
        if not category:
            st.error("Category is required.")
        else:
            final_amount = amount if tx_type == "Income" else -amount
            record = add_transaction(final_amount, category, description,
                                     date.strftime("%Y-%m-%d"))
            st.success(f"Added: ${record['amount']:+.2f} [{record['category']}]")
            st.rerun()

# ── Summary Metrics ─────────────────────────────────────────────────
summary = get_summary()
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${summary['total_income']:,.2f}")
col2.metric("Total Expenses", f"${abs(summary['total_expenses']):,.2f}")
col3.metric("Net Balance", f"${summary['net_balance']:,.2f}",
            delta=f"${summary['net_balance']:,.2f}")

# ── Transaction Table ───────────────────────────────────────────────
st.subheader("Transactions")
transactions = list_transactions()

if transactions:
    df = pd.DataFrame(transactions)
    df = df[["id", "date", "amount", "category", "description"]]
    df.columns = ["ID", "Date", "Amount", "Category", "Description"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Delete transaction
    with st.expander("Delete a transaction"):
        ids = [t["id"] for t in transactions]
        del_id = st.selectbox("Select transaction ID to delete", ids)
        if st.button("Delete"):
            if delete_transaction(del_id):
                st.success(f"Transaction {del_id} deleted.")
                st.rerun()
            else:
                st.error(f"Transaction {del_id} not found.")
else:
    st.info("No transactions yet. Use the sidebar to add one.")

# ── Charts ──────────────────────────────────────────────────────────
if transactions:
    st.subheader("Charts")

    chart1, chart2 = st.columns(2)

    # 1. Spending by category pie chart
    with chart1:
        spending = {k: abs(v) for k, v in summary["by_category"].items() if v < 0}
        if spending:
            fig1, ax1 = plt.subplots(figsize=(6, 5))
            ax1.pie(spending.values(), labels=spending.keys(),
                    autopct="%1.1f%%", startangle=140)
            ax1.set_title("Spending by Category")
            st.pyplot(fig1)
            plt.close(fig1)
        else:
            st.caption("No expenses to chart yet.")

    # 2. Monthly income vs expenses bar chart
    with chart2:
        monthly_income: dict[str, float] = defaultdict(float)
        monthly_expense: dict[str, float] = defaultdict(float)
        for t in transactions:
            month_key = t["date"][:7]
            if t["amount"] >= 0:
                monthly_income[month_key] += t["amount"]
            else:
                monthly_expense[month_key] += abs(t["amount"])

        months = sorted(set(monthly_income) | set(monthly_expense))
        incomes = [monthly_income.get(m, 0) for m in months]
        expenses = [monthly_expense.get(m, 0) for m in months]

        if months:
            x = range(len(months))
            width = 0.35
            fig2, ax2 = plt.subplots(figsize=(6, 5))
            ax2.bar([i - width / 2 for i in x], incomes, width,
                    label="Income", color="#2ecc71")
            ax2.bar([i + width / 2 for i in x], expenses, width,
                    label="Expenses", color="#e74c3c")
            ax2.set_xticks(list(x))
            ax2.set_xticklabels(months, rotation=45, ha="right")
            ax2.set_ylabel("Amount ($)")
            ax2.set_title("Monthly Income vs Expenses")
            ax2.legend()
            fig2.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

    # 3. Balance over time line chart (full width)
    sorted_txns = sorted(transactions, key=lambda t: t["date"])
    dates = [t["date"] for t in sorted_txns]
    cumulative = []
    running = 0.0
    for t in sorted_txns:
        running += t["amount"]
        cumulative.append(running)

    fig3, ax3 = plt.subplots(figsize=(10, 4))
    ax3.plot(dates, cumulative, marker="o", linewidth=2, color="#3498db")
    ax3.fill_between(dates, cumulative, alpha=0.15, color="#3498db")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Balance ($)")
    ax3.set_title("Cumulative Balance Over Time")
    ax3.tick_params(axis="x", rotation=45)
    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)
