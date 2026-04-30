
from datetime import datetime


class ExpenseManager:


    def __init__(self):
        self.expenses = []

        self.total = 0.0

    def add_expense(self, label, amount):

        if amount <= 0:
            raise ValueError("greater than zero amount")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        expense = {
            "label": label.strip() if label.strip() else "Expense",
            "amount": amount,
            "date": timestamp
        }

        self.expenses.append(expense)

        # ACCUMULATOR:
        self.total = self.total + amount

        return expense

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            removed = self.expenses.pop(index)
            self.total = self.total - removed["amount"]
            return removed
        raise IndexError("No expense found at that position.")

    def clear_all(self):
        self.expenses = []
        self.total = 0.0

    def get_average(self):
        if not self.expenses:
            return 0.0
        return self.total / len(self.expenses)

    def get_highest(self):
        if not self.expenses:
            return None
        return max(self.expenses, key=lambda e: e["amount"])

    def get_count(self):
        return len(self.expenses)
