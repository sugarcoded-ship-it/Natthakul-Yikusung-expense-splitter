from decimal import Decimal, InvalidOperation

from splitter import ExpenseBook, parse_amount, parse_date


def print_menu() -> None:
    print("\n1. Add person")
    print("2. Add expense")
    print("3. Record repayment")
    print("4. View expenses and who still owes")
    print("5. Quit")


def read_amount(prompt: str) -> Decimal:
    return parse_amount(input(prompt))


def add_person(book: ExpenseBook) -> None:
    book.add_person(input("Person name: ").strip())
    print("Person added.")


def add_expense(book: ExpenseBook) -> None:
    while True:
        payer = input("Payer: ").strip()
        if payer in book.people:
            break
        print(f"{payer} is not an existing person.")
        if input(f"Add {payer}? (y/n): ").strip().lower() in {"y", "yes"}:
            book.add_person(payer)
            break

    while True:
        amount_text = input("Amount: ")
        try:
            amount = parse_amount(amount_text)
            break
        except ValueError as error:
            print(f"Error: {error}")

    while True:
        participant_text = input("Participants (comma-separated): ")
        participants = [
            participant.strip()
            for participant in participant_text.split(",")
            if participant.strip()
        ]
        if not participants:
            print("Error: Expense must have at least one participant.")
            continue
        unknown_participant = next(
            (participant for participant in participants if participant not in book.people),
            None,
        )
        if unknown_participant is None:
            break
        print(f"{unknown_participant} is not an existing person.")
        if (
            input(f"Add {unknown_participant}? (y/n): ").strip().lower()
            in {"y", "yes"}
        ):
            book.add_person(unknown_participant)
        else:
            continue

    while True:
        date_text = input("Date: ")
        try:
            date = parse_date(date_text)
            break
        except ValueError as error:
            print(f"Error: {error}")

    book.add_expense(payer, amount, participants, date)
    print("Expense added.")


def record_repayment(book: ExpenseBook) -> None:
    if not book.expenses:
        print("No expenses recorded yet.")
        return

    for index, expense in enumerate(book.expenses, start=1):
        print(f"{index}. {expense.date} - {expense.payer} - {expense.amount}")
    while True:
        expense_number_text = input(
            "Expense number (Enter to cancel): "
        ).strip()
        if not expense_number_text:
            print("Cancelled.")
            return
        try:
            expense_number = int(expense_number_text)
        except ValueError:
            print(f"Expense number must be between 1 and {len(book.expenses)}")
            continue
        if 1 <= expense_number <= len(book.expenses):
            break
        print(f"Expense number must be between 1 and {len(book.expenses)}")
    expense_index = expense_number - 1

    if not any(
        participant != book.expenses[expense_index].payer
        for participant in book.expenses[expense_index].participants
    ):
        print("Nobody owes anything on this expense.")
        return

    while True:
        from_person = input("Person repaying (Enter to cancel): ").strip()
        if not from_person:
            print("Cancelled.")
            return
        try:
            amount_owed = book.amount_owed(expense_index, from_person)
        except ValueError as error:
            print(f"Error: {error}")
            continue
        if amount_owed == Decimal("0.00"):
            print(f"{from_person} has already paid this expense.")
            return

        while True:
            amount_text = input("Amount (Enter to cancel): ")
            if not amount_text.strip():
                print("Cancelled.")
                return
            try:
                amount = parse_amount(amount_text)
                book.record_repayment(expense_index, from_person, amount)
            except ValueError as error:
                print(f"Error: {error}")
                continue
            print("Repayment recorded.")
            return


def view_expenses(book: ExpenseBook) -> None:
    if not book.expenses:
        print("No expenses recorded yet.")
        return

    participants = list(
        dict.fromkeys(
            participant
            for expense in book.expenses
            for participant in expense.participants
        )
    )
    rows: list[list[str]] = []
    for index, expense in enumerate(book.expenses):
        status = book.status(index)
        participant_values = []
        for participant in participants:
            if participant not in expense.shares:
                participant_values.append("-")
                continue
            share = expense.shares[participant]
            if participant == expense.payer:
                participant_values.append(f"{share}")
                continue
            details = status[participant]
            participant_values.append(
                f"{share} / paid {details['paid']} / owes {details['owes']}"
            )
        rows.append(
            [
                str(index + 1),
                expense.date,
                expense.payer,
                str(expense.amount),
                *participant_values,
            ]
        )

    headers = ["#", "Date", "Payer", "Amount", *participants]
    widths = [
        max(len(headers[column]), *(len(row[column]) for row in rows))
        for column in range(len(headers))
    ]
    print("\nExpenses:")
    print("  ".join(header.ljust(width) for header, width in zip(headers, widths)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(value.ljust(width) for value, width in zip(row, widths)))

    print("\nTotals:")
    totals = book.totals()
    for person, payer_totals in totals.items():
        nonzero_totals = {
            payer: amount
            for payer, amount in payer_totals.items()
            if amount != Decimal("0.00")
        }
        for payer, amount in nonzero_totals.items():
            print(f"  {person} → {payer} {amount}")
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
