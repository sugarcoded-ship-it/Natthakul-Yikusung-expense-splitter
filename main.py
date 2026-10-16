from decimal import Decimal, InvalidOperation

from splitter import ExpenseBook


def print_menu() -> None:
    print("\n1. Add person")
    print("2. Add expense")
    print("3. Record repayment")
    print("4. View expenses and who still owes")
    print("5. Quit")


def read_amount(prompt: str) -> Decimal:
    try:
        return Decimal(input(prompt).strip())
    except InvalidOperation as error:
        raise ValueError("Amount must be a valid number.") from error


def add_person(book: ExpenseBook) -> None:
    book.add_person(input("Person name: ").strip())
    print("Person added.")


def add_expense(book: ExpenseBook) -> None:
    payer = input("Payer: ").strip()
    amount = read_amount("Amount: ")
    participants = [
        participant.strip()
        for participant in input("Participants (comma-separated): ").split(",")
        if participant.strip()
    ]
    date = input("Date: ").strip()
    book.add_expense(payer, amount, participants, date)
    print("Expense added.")


def record_repayment(book: ExpenseBook) -> None:
    if not book.expenses:
        print("No expenses recorded yet.")
        return

    for index, expense in enumerate(book.expenses, start=1):
        print(f"{index}. {expense.date} - {expense.payer} - {expense.amount}")
    expense_number_text = input("Expense number: ").strip()
    try:
        expense_number = int(expense_number_text)
    except ValueError:
        print(f"Expense number must be between 1 and {len(book.expenses)}")
        return
    if not 1 <= expense_number <= len(book.expenses):
        print(f"Expense number must be between 1 and {len(book.expenses)}")
        return
    expense_index = expense_number - 1
    from_person = input("Person repaying: ").strip()
    amount = read_amount("Amount: ")
    book.record_repayment(expense_index, from_person, amount)
    print("Repayment recorded.")


def view_expenses(book: ExpenseBook) -> None:
    if not book.expenses:
        print("No expenses recorded yet.")
        return

    for index, expense in enumerate(book.expenses, start=1):
        print(f"\nExpense {index}:")
        print(f"Date: {expense.date}")
        print(f"Payer: {expense.payer}")
        print(f"Amount: {expense.amount}")
        print("Shares:")
        for participant, share in expense.shares.items():
            print(f"  {participant}: {share}")

        print("Repayments and amounts still owed:")
        for participant, details in book.status(index - 1).items():
            print(
                f"  {participant}: paid {details['paid']}, "
                f"still owes {details['owes']}"
            )

    print("\nTotals still owed:")
    totals = book.totals()
    for person, payer_totals in totals.items():
        nonzero_totals = {
            payer: amount
            for payer, amount in payer_totals.items()
            if amount != Decimal("0.00")
        }
        for payer, amount in nonzero_totals.items():
            print(f"  {person} owes {payer}: {amount}")
    if not any(
        amount != Decimal("0.00")
        for payer_totals in totals.values()
        for amount in payer_totals.values()
    ):
        print("Nobody owes anything.")


def run_menu() -> None:
    book = ExpenseBook()
    while True:
        print_menu()
        try:
            choice = input("Choose an option: ").strip()
            if choice == "1":
                add_person(book)
            elif choice == "2":
                add_expense(book)
            elif choice == "3":
                record_repayment(book)
            elif choice == "4":
                view_expenses(book)
            elif choice == "5":
                print("Goodbye.")
                return
            else:
                print("Invalid option.")
        except (ValueError, InvalidOperation) as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("Goodbye.")
            return


if __name__ == "__main__":
    run_menu()
