
from models import Transaction
from analytics import (
    running_balance,
    make_flagger,
    find_duplicates,
    category_totals
)

transactions = [
    Transaction("2026-08-01", "Salary", 1000, "INCOME"),
    Transaction("2026-08-02", "Food", -100, "FOOD"),
    Transaction("2026-08-03", "Transport", -50, "TRANSPORT"),
]

print("Balances:", list(running_balance(transactions)))

flagger = make_flagger(200)

print("Flag 500:", flagger(
    Transaction("2026-08-04", "Large", 500, "OTHER")
))

print("Flag 50:", flagger(
    Transaction("2026-08-05", "Small", 50, "OTHER")
))

print("Category totals:", category_totals(transactions))

duplicate_list = transactions + [transactions[1]]

print("Duplicates:", find_duplicates(duplicate_list))
