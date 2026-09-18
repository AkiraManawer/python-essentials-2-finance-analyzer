
from models import Transaction
from reporting import monthly_summary

transactions = [
    Transaction("2026-08-01", "Salary", 10000, "INCOME"),
    Transaction("2026-08-02", "Groceries", -500, "FOOD"),
    Transaction("2026-08-03", "Transport", -200, "TRANSPORT"),
]

report_path = monthly_summary(
    transactions,
    rejected_count=2
)

print("Report created:", report_path)
