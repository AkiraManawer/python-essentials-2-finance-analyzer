import os
from datetime import datetime
from models import Transaction


def generate_sample_file():
    os.makedirs("data", exist_ok=True)
    rows = [
        "date,description,amount,category",
        "2026-08-01,Salary,15000,Income",
        "2026/08/03,Groceries,-450.50,Food",
        "2026-08-04,Transport,-200,Transport",
        "2026-08-05,Electricity,-850,Utilities",
        "2026-08-06,Freelance,2500,Income",
        "2026-08-07,Coffee,-45,Food",
        "2026-08-08,Internet,-699,Utilities",
        "2026-08-09,Salary,15000,Income",
        "2026-08-09,Salary,15000,Income",
        "2026-08-10,Incorrect expense,500,Food",
        "2026-08-11,Incorrect income,-300,Income",
        "2026-08-12,Missing category,-100",
        "hello world",
        "2026-08-13,Broken amount,abc,Food",
        " 2026-08-14, Cinema ,-250,  Entertainment ",
    ]
    with open("data/statement.txt", "w", encoding="utf-8") as file:
        for row in rows:
            file.write(row + "\n")
    print("Messy sample statement created.")
    return "data/statement.txt"


def normalize_date(date_text):
    date_text = date_text.strip()
    date_text = date_text.replace("/", "-")
    parsed_date = datetime.strptime(date_text, "%Y-%m-%d")
    return parsed_date.strftime("%Y-%m-%d")


def load_transactions(path):
    transactions = []
    rejections = []

    if not os.path.exists(path):
        return [], [f"File not found: {path}"]
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except OSError as error:
        return [], [f"Error reading file: {error}"]
    if not lines:
        return [], ["File is empty"]
    for row_number, line in enumerate(lines, start=1):
        line = line.strip()
        if row_number == 1 and line.lower().startswith("date,"):
            continue
        if not line:
            rejections.append(f"Row {row_number}: Empty row")
            continue

        try:
            fields = line.split(",")
            if len(fields) != 4:
                raise ValueError("Incorrect number of fields")
            date_text, description, amount_text, category = [
                field.strip() for field in fields
            ]
            if not date_text:
                raise ValueError("Missing date")
            if not description:
                raise ValueError("Missing description")
            if not amount_text:
                raise ValueError("Missing amount")
            if not category:
                raise ValueError("Missing category")
            date_text = normalize_date(date_text)
            amount = float(amount_text)
            category = category.upper()

            if category == "INCOME" and amount < 0:
                raise ValueError("Income amount cannot be negative")
            if category != "INCOME" and amount > 0:
                rejections.append(
                    f"Row {row_number}: positive amount tagged"
                    f"as expense/category {category}"
                )
            transaction = Transaction(
                date_text,
                description,
                amount,
                category
            )
            transactions.append(transaction)
        except ValueError as error:
            rejections.append(f"Row {row_number}: {error}")
            except Exception as error:
            rejections.append(f"Row {row_number}: Unexpected error: {error}")
    return transactions, rejections
