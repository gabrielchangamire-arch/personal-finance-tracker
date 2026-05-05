# Personal Finance Tracker

A command-line personal finance tracker built with Python. Track income and expenses by category, view summaries, and generate charts.

## Features

- **Add transactions** - record income (positive) or expenses (negative) with category, description, and date
- **Filter & list** - view all transactions or filter by category
- **Financial summary** - total income, expenses, net balance, and per-category breakdown
- **Charts** - auto-generated PNG charts:
  - Spending by category (pie chart)
  - Monthly income vs expenses (bar chart)
  - Cumulative balance over time (line chart)
- **Delete transactions** - remove entries by ID

## Setup

```bash
# Clone the repo
git clone https://github.com/gabrielchangamire-arch/personal-finance-tracker.git
cd personal-finance-tracker

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Follow the interactive menu to add transactions, view summaries, and generate charts.

## Project Structure

```
personal-finance-tracker/
├── main.py             # CLI menu and entry point
├── tracker.py          # Core logic - add, list, summarise, delete transactions
├── visualize.py        # Matplotlib chart generation
├── requirements.txt    # Python dependencies
└── .gitignore
```

## Data Storage

Transactions are stored locally in `transactions.json` (auto-created on first use, git-ignored).
