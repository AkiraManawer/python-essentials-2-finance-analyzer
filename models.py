class Transaction:
    transaction_count = 0

    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = float(amount)
        self.category = category
        Transaction.transaction_count += 1

    def _str__(self):
        return (
            f"{self.date} | {self.description}|"
            f"{self.amount:.2f} | ({self.category})"
        )

    def is_income(self):
        return self.amount > 0

    def formatted(self):
        sign = "+" if self.amount > 0 else ""
        return (
            f"{self.date} | {self.description} | "
            f"{sign}{self.amount:.2f} | ({self.category})"
        )


class RecurringTransaction(Transaction):
    def __init__(self, date, description, amount, category, interval):
        super().__init__(date, description, amount, category)
        self.interval = interval

    def _str_(self):
        return (
            f"{super()._str_()} | "
            f"Recurring: {self.interval}"
        )
