
from parser import generate_sample_file, load_transactions
from analytics import (
    running_balance,
    category_totals,
    find_duplicates,
    find_outliers,
    make_flagger
)
from reporting import monthly_summary


def display_menu():
    print("\n===== FINANCE TRANSACTION ANALYZER =====")
    print("1. Generate a messy sample statement file")
    print("2. Load & validate transactions")
    print("3. Show running balance (ledger)")
    print("4. Category breakdown")
    print("5. Detect duplicate transactions")
    print("6. Flag unusual transactions")
    print("7. Monthly summary report -> file")
    print("8. Run self-tests (tests.py)")
    print("9. Exit")


def main():
    transactions = []
    rejections = []

    while True:
        display_menu()

        try:
            choice = input("Choose an option (1-9): ").strip()

            if choice == "1":
                generate_sample_file()

            elif choice == "2":
                path = input(
                    "Enter statement path "
                    "(default data/statement.txt): "
                ).strip()

                if not path:
                    path = "data/statement.txt"

                transactions, rejections = load_transactions(path)

                print(
                    f"Loaded {len(transactions)} valid "
                    f"transactions."
                )

                print(
                    f"Rejected/inconsistent rows: "
                    f"{len(rejections)}"
                )

                for reason in rejections:
                    print("-", reason)

            elif choice == "3":
                if not transactions:
                    print("Load transactions first.")
                    continue

                print("\nRUNNING BALANCE")

                for transaction, balance in zip(
                    transactions,
                    running_balance(transactions)
                ):
                    print(
                        f"{transaction.date} | "
                        f"{transaction.description} | "
                        f"Balance: {balance:.2f}"
                    )

            elif choice == "4":
                if not transactions:
                    print("Load transactions first.")
                    continue

                totals = category_totals(transactions)

                print("\nCATEGORY BREAKDOWN")

                for category, amount in totals.items():
                    print(f"{category}: {amount:.2f}")

            elif choice == "5":
                if not transactions:
                    print("Load transactions first.")
                    continue

                duplicates = find_duplicates(transactions)

                if duplicates:
                    print("\nDUPLICATES FOUND")

                    for transaction in duplicates:
                        print(transaction)
                else:
                    print("No duplicates found.")

            elif choice == "6":
                if not transactions:
                    print("Load transactions first.")
                    continue

                try:
                    threshold = float(
                        input("Enter threshold amount: ")
                    )

                    flagger = make_flagger(threshold)

                    flagged = [
                        transaction
                        for transaction in transactions
                        if flagger(transaction)
                    ]

                    if flagged:
                        print("\nUNUSUAL TRANSACTIONS")

                        for transaction in flagged:
                            print(transaction)
                    else:
                        print("No transactions exceeded threshold.")

                except ValueError:
                    print("Please enter a valid number.")

            elif choice == "7":
                if not transactions:
                    print("Load transactions first.")
                    continue

                path = monthly_summary(
                    transactions,
                    len(rejections)
                )

                print(f"Report saved to {path}")

            elif choice == "8":
                print("Run this command in the terminal:")
                print("python tests.py")

            elif choice == "9":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please select 1-9.")

        except Exception as error:
            print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
