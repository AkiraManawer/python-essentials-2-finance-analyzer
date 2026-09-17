import os
import platform
from datetime import datetime

from analytics import (
    category_totals,
    find_duplicates,
    find_outliers
)


def monthly_summary(
        transactions,
        rejected_count=0,
        report_path="data/report.txt"
):
    os.makedirs("data", exist_ok=True)
    now = datetime.now()

    total_income = sum(
        transaction.amount
        for transaction in transactions
        if transaction.amount > 0
    )

    balance = sum(
        transaction.amount
        for transaction in transactions
    )

    totals = category_totals(transactions)
    duplicates = find_duplicates(transactions)
    outliers = find_outliers(transactions)

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("PERSONAL FINANCE REPORT\n")
        file.write("=" * 45 + "\n")

        file.write(f"Report date: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Operating System: {platform.system()}\n")
        file.write(f"Platform: {platform.platform()}\n")
        file.write(f"Python version: {platform.python_version()}\n\n")

        file.write(f"Valid Transactions: {len(transactions)}\n")
        file.write(f"Rejected rows: {rejected_count}\n")
        file.write(f"Total Income: {total_income:.2f}\n")
        file.write(f"Total expenses: {total_expenses:.2f}\n")
        file.write(f"Net balance change: {balance:.2f}\n\n")

        file.write("Category Totals:\n")
        file.write("=" * 45 + "\n")

        for category, amount in totals.items():
            file.write(f"{category}: {amount:.2f}\n")

        file.write("\nDuplicate Transactions:\n")
        file.write("=" * 45 + "\n")

        if duplicates:
            for transaction in duplicates:
                file.write(str(transaction) + "\n")
        else:
            file.write("No duplicate transactions found.\n")

        file.write("\nOutliers:\n")
        file.write("=" * 45 + "\n")

        if outliers:
            for transaction in outliers:
                file.write(str(transaction) + "\n")
        else:
            file.write("No outliers found.\n")

    with open("data/run_log.txt", "a", encoding="utf-8") as log:
        log.write(
            f"{now.strftime('%Y-%m-%d %H:%M:%S')} - "
            f"Report generated for {len(transactions)} "
            f"transactions\n"
        )
    return report_path
