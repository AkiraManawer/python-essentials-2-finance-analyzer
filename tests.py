import os
import tempfile

from models import Transaction, RecurringTransaction
from parser import load_transactions
from analytics import (
    running_balance,
    make_flagger,
    find_duplicates,
    find_outliers,
    category_totals
)

# Test 1: Valid row parses correctly


def test_valid_row():
    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        suffix=".txt",
        encoding="utf-8"
    ) as file:
        file.write("date,description,amount,category\n")
        file.write("2026-08-01,Salary,1000,INCOME\n")
        path = file.name

    try:
        transactions, rejections = load_transactions(path)
        assert len(transactions) == 1, (
            "Valid row was  not loaded"
        )
        assert transactions[0].date == "2026-08-01", (
            "Date is incorrect"
        )
        assert transactions[0].amount == 1000.0, (
            "Amount is incorrect"
        )
        assert transactions[0].category == "INCOME", (
            "Category is incorrect"
        )
    finally:
        os.remove(path)

# Test 2: Wrong date seperator normalised


def test_date_normalisation():
    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        suffix=".txt",
        encoding="utf-8"
    ) as file:
        file.write("date,description,amount,category\n")
        file.write("2026/08/03,Food,-100,FOOD\n")
        path = file.name

    try:
        transactions, rejections = load_transactions(path)

        assert transactions[0].date == "2026-08-03", (
            "Date was not normalised"
        )
    finally:
        os.remove(path)

# Test 3: Junk line is rejected.


def test_junk_line():
    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        suffix=".txt",
        encoding="utf-8"
    ) as file:
        file.write("date,description,amount,category\n")
        file.write("hello world\n")
        path = file.name

    try:
        transactions, rejections = load_transactions(path)

        assert len(transactions) == 0, (
            "Junk line was accepted"
        )
        assert len(rejections) >= 1, (
            "Junk line was not rejected"
        )
    finally:
        os.remove(path)


# Test 4: Missing fields are rejected.
def test_missing_fields():
    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        suffix=".txt",
        encoding="utf-8"
    ) as file:
        file.write("date,description,amount,category\n")
        file.write("2026-08-01,Food,-100\n")
        path = file.name

    try:
        transactions, rejections = load_transactions(path)

        assert len(transactions) == 0, (
            "Incomplete row was accepted"
        )
        assert len(rejections) >= 1, (
            "Incomplete row was not rejected"
        )
    finally:
        os.remove(path)


# Test 5: Non-numeric amount is rejected.
def test_invalid_amount():
    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        suffix=".txt",
        encoding="utf-8"
    ) as file:
        file.write("date,description,amount,category\n")
        file.write("2026-08-01,Food,abc,FOOD\n")
        path = file.name

    try:
        transactions, rejections = load_transactions(path)

        assert len(transactions) == 0, (
            "Invalid amount was accepted"
        )
        assert len(rejections) >= 1, (
            "Invalid amount was not rejected"
        )
    finally:
        os.remove(path)


# Test 6: Running balance is correct.
def test_running_balance():
    transactions = [
        Transaction("2026-08-01", "Salary", 1000, "INCOME"),
        Transaction("2026-08-02", "Food", -100, "FOOD"),
        Transaction("2026-08-03", "Transport", -50, "TRANSPORT"),
    ]

    result = list(running_balance(transactions))

    assert result == [1000.0, 900.0, 850.0], (
        "Running balance is incorrect"
    )


# Test 7: Closure flags large amounts.
def test_flagger():
    flagger = make_flagger(1000)

    large_transaction = Transaction(
        "2026-08-01", "Large", 5000, "OTHER"
    )

    small_transaction = Transaction(
        "2026-08-01", "Small", 50, "OTHER"
    )

    assert flagger(large_transaction) is True, (
        "Large transaction was not flagged"
    )

    assert flagger(small_transaction) is False, (
        "Small transaction was incorrectly flagged"
    )


# Test 8: Duplicate detection works.
def test_duplicates():
    first = Transaction(
        "2026-08-01", "Food", -100, "FOOD"
    )

    second = Transaction(
        "2026-08-02", "Transport", -50, "TRANSPORT"
    )

    duplicate = Transaction(
        "2026-08-01", "Food", -100, "FOOD"
    )

    duplicates = find_duplicates(
        [first, second, duplicate]
    )

    assert len(duplicates) == 1, (
        "Duplicate was not detected"
    )


# Test 9: Clean list has no duplicates.
def test_no_duplicates():
    transactions = [
        Transaction("2026-08-01", "Food", -100, "FOOD"),
        Transaction("2026-08-02", "Transport", -50, "TRANSPORT"),
    ]

    duplicates = find_duplicates(transactions)

    assert duplicates == [], (
        "False duplicate was detected"
    )


# Test 10: is_income works.
def test_is_income():
    income = Transaction(
        "2026-08-01", "Salary", 1000, "INCOME"
    )

    expense = Transaction(
        "2026-08-02", "Food", -100, "FOOD"
    )

    assert income.is_income() is True, (
        "Income was not identified correctly"
    )

    assert expense.is_income() is False, (
        "Expense was incorrectly identified as income"
    )


# Test 11: Category totals work.
def test_category_totals():
    transactions = [
        Transaction("2026-08-01", "Food", -100, "FOOD"),
        Transaction("2026-08-02", "Food", -50, "FOOD"),
        Transaction("2026-08-03", "Salary", 1000, "INCOME"),
    ]

    totals = category_totals(transactions)

    assert totals["FOOD"] == -150.0, (
        "Food total is incorrect"
    )

    assert totals["INCOME"] == 1000.0, (
        "Income total is incorrect"
    )


# Test 12: Subclass uses inheritance.
def test_recurring_transaction():
    transaction = RecurringTransaction(
        "2026-08-01",
        "Rent",
        -5000,
        "HOUSING",
        "Monthly"
    )

    assert transaction.interval == "Monthly", (
        "Recurring interval is incorrect"
    )

    assert transaction.is_income() is False, (
        "Recurring transaction inheritance failed"
    )


# Test 13: Missing file is handled.
def test_missing_file():
    transactions, rejections = load_transactions(
        "file_that_does_not_exist.txt"
    )

    assert transactions == [], (
        "Missing file returned transactions"
    )

    assert len(rejections) >= 1, (
        "Missing file was not reported"
    )


# Test 14: Empty file is handled.
def test_empty_file():
    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        suffix=".txt",
        encoding="utf-8"
    ) as file:
        path = file.name

    try:
        transactions, rejections = load_transactions(path)

        assert transactions == [], (
            "Empty file returned transactions"
        )

        assert len(rejections) >= 1, (
            "Empty file was not reported"
        )
    finally:
        os.remove(path)


# Run all tests.
if __name__ == "__main__":
    test_valid_row()
    test_date_normalisation()
    test_junk_line()
    test_missing_fields()
    test_invalid_amount()
    test_running_balance()
    test_flagger()
    test_duplicates()
    test_no_duplicates()
    test_is_income()
    test_category_totals()
    test_recurring_transaction()
    test_missing_file()
    test_empty_file()

    print("All tests passed")
