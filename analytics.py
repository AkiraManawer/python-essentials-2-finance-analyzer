from statistics import mean, stdev


def running_balance(transactions, start=0.0):
    balance = float(start)
    for transaction in transactions:
        balance += transaction.amount
        yield balance


def make_flagger(threshold):
    def flagger(transaction):
        return abs(transaction.amount) > threshold

    return flagger


def find_duplicates(transactions):
    seen = set()
    duplicates = []
    for transaction in transactions:
        signature = (
            transaction.date,
            transaction.description,
            transaction.amount,
            transaction.category
        )
        if signature in seen:
            duplicates.append(transaction)
        else:
            seen.add(signature)
    return duplicates


def find_outliers(transactions):
    if len(transactions) < 3:
        return []
    amounts = [transaction.amount for transaction in transactions]

    average = mean(amounts)
    standard_deviation = stdev(amounts)

    if standard_deviation == 0:
        return []
    outliers = []
    for transaction in transactions:
        if abs(transaction.amount - average) > 2 * standard_deviation:
            outliers.append(transaction)
    return outliers


def category_totals(transactions):
    totals = {}
    for transaction in transactions:
        category = transaction.category
        if category not in totals:
            totals[category] = 0.0
        totals[category] += transaction.amount
    return totals
