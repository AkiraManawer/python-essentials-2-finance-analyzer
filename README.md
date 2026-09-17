# Akira Manawer
# Python Essentials 2 - Fianance Analyzer

# Personal Finance Transaction Analyzer

This project is a Python program that reads bank statement
transactions, validates messy data, calculates balances,
categorises transactions, detects duplicates and unusual
transactions, and creates summary reports.

## Features

- Object-oriented transaction classes
- Defensive file parsing
- Running balance generator
- Category totals
- Duplicate detection
- Statistical outlier detection
- Monthly reports
- Automated tests

## Project files

- models.py: Transaction classes
- parser.py: File reading and validation
- analytics.py: Financial calculations and analysis
- reporting.py: Reports and run logs
- main.py: User menu
- tests.py: Assertion tests

## Example usage

1. Run python main.py.
2. Choose option 1 to generate the sample statement.
3. Choose option 2 to load and validate transactions.
4. Choose option 3 to display the running balance.
5. Choose option 4 to view category totals.
6. Choose option 5 to find duplicates.
7. Choose option 6 to flag unusual amounts.
8. Choose option 7 to create the report.
9. Choose option 8 to see the testing instructions.

## Testing

The project contains 14 assertions in tests.py.
The tests cover valid transactions, broken dates, missing
fields, junk rows, invalid amounts, running balances,
closures, duplicate detection, and inheritance.

Run the tests using:

python tests.py