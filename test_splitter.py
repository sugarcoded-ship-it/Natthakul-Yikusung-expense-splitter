from decimal import Decimal

import pytest

from splitter import ExpenseBook


def test_add_expense_normal_case() -> None:
    book = ExpenseBook()
    for name in ["A", "B", "C"]:
        book.add_person(name)

    expense = book.add_expense(
        payer="A",
        amount=Decimal("300.00"),
        participants=["A", "B", "C"],
        date="2026-10-16",
    )

    assert expense.payer == "A"
    assert expense.amount == Decimal("300.00")
    assert expense.participants == ["A", "B", "C"]
    assert expense.date == "2026-10-16"
    assert expense.shares == {
        "A": Decimal("100.00"),
        "B": Decimal("100.00"),
        "C": Decimal("100.00"),
    }
    assert {key: str(value) for key, value in expense.shares.items()} == {
        "A": "100.00",
        "B": "100.00",
        "C": "100.00",
    }


def test_add_expense_negative_amount_leaves_expense_list_empty() -> None:
    book = ExpenseBook()
    for name in ["A", "B", "C"]:
        book.add_person(name)

    with pytest.raises(ValueError):
        book.add_expense(
            payer="A",
            amount=Decimal("-50"),
            participants=["A", "B"],
            date="2026-10-16",
        )

    assert book.expenses == []


def test_adding_same_person_twice_raises_value_error() -> None:
    book = ExpenseBook()
    book.add_person("A")

    with pytest.raises(ValueError):
        book.add_person("A")


def test_add_expense_with_no_participants_leaves_expenses_unchanged() -> None:
    book = ExpenseBook()
    book.add_person("A")
    original_expenses = list(book.expenses)

    with pytest.raises(ValueError):
        book.add_expense(
            payer="A",
            amount=Decimal("10.00"),
            participants=[],
            date="2026-10-16",
        )

    assert book.expenses == original_expenses


def test_add_expense_with_unknown_payer_leaves_expenses_unchanged() -> None:
    book = ExpenseBook()
    book.add_person("A")
    original_expenses = list(book.expenses)

    with pytest.raises(ValueError):
        book.add_expense(
            payer="B",
            amount=Decimal("10.00"),
            participants=["A"],
            date="2026-10-16",
        )

    assert book.expenses == original_expenses


def test_add_expense_with_unknown_participant_leaves_expenses_unchanged() -> None:
    book = ExpenseBook()
    book.add_person("A")
    original_expenses = list(book.expenses)

    with pytest.raises(ValueError):
        book.add_expense(
            payer="A",
            amount=Decimal("10.00"),
            participants=["A", "B"],
            date="2026-10-16",
        )

    assert book.expenses == original_expenses


def test_add_expense_with_duplicate_participants_leaves_expenses_unchanged() -> None:
    book = ExpenseBook()
    book.add_person("A")
    original_expenses = list(book.expenses)

    with pytest.raises(ValueError):
        book.add_expense(
            payer="A",
            amount=Decimal("10.00"),
            participants=["A", "A"],
            date="2026-10-16",
        )

    assert book.expenses == original_expenses


def test_add_expense_with_more_than_two_decimal_places_leaves_expenses_unchanged() -> None:
    book = ExpenseBook()
    book.add_person("A")
    original_expenses = list(book.expenses)

    with pytest.raises(ValueError):
        book.add_expense(
            payer="A",
            amount=Decimal("10.005"),
            participants=["A"],
            date="2026-10-16",
        )

    assert book.expenses == original_expenses


def test_add_expense_with_nan_amount_leaves_expenses_unchanged() -> None:
    book = ExpenseBook()
    book.add_person("A")
    original_expenses = list(book.expenses)

    with pytest.raises(ValueError):
        book.add_expense(
            payer="A",
            amount=Decimal("NaN"),
            participants=["A"],
            date="2026-10-16",
        )

    assert book.expenses == original_expenses


def test_add_expense_with_infinite_amount_leaves_expenses_unchanged() -> None:
    book = ExpenseBook()
    book.add_person("A")
    original_expenses = list(book.expenses)

    with pytest.raises(ValueError):
        book.add_expense(
            payer="A",
            amount=Decimal("Infinity"),
            participants=["A"],
            date="2026-10-16",
        )

    assert book.expenses == original_expenses


def test_add_expense_with_float_amount_leaves_expenses_unchanged() -> None:
    book = ExpenseBook()
    book.add_person("A")
    original_expenses = list(book.expenses)

    with pytest.raises(ValueError):
        book.add_expense(
            payer="A",
            amount=10.5,
            participants=["A"],
            date="2026-10-16",
        )

    assert book.expenses == original_expenses


def test_add_expense_with_empty_date_leaves_expenses_unchanged() -> None:
    book = ExpenseBook()
    book.add_person("A")
    original_expenses = list(book.expenses)

    with pytest.raises(ValueError):
        book.add_expense(
            payer="A",
            amount=Decimal("10.00"),
            participants=["A"],
            date="  ",
        )

    assert book.expenses == original_expenses


def test_calculates_c4_shares_with_leftover_cent_for_first_participant() -> None:
    book = ExpenseBook()
    for name in ["A", "B", "C"]:
        book.add_person(name)

    expense = book.add_expense(
        payer="A",
        amount=Decimal("100.00"),
        participants=["A", "B", "C"],
        date="2026-10-16",
    )

    assert expense.shares == {
        "A": Decimal("33.34"),
        "B": Decimal("33.33"),
        "C": Decimal("33.33"),
    }
    assert {key: str(value) for key, value in expense.shares.items()} == {
        "A": "33.34",
        "B": "33.33",
        "C": "33.33",
    }
    assert sum(expense.shares.values(), Decimal("0.00")) == Decimal("100.00")


def test_calculates_one_cent_share_for_two_participants() -> None:
    book = ExpenseBook()
    for name in ["A", "B"]:
        book.add_person(name)

    expense = book.add_expense(
        payer="A",
        amount=Decimal("0.01"),
        participants=["A", "B"],
        date="2026-10-16",
    )

    assert expense.shares == {
        "A": Decimal("0.01"),
        "B": Decimal("0.00"),
    }
    assert {key: str(value) for key, value in expense.shares.items()} == {
        "A": "0.01",
        "B": "0.00",
    }


def test_c3_repayment_updates_status() -> None:
    book = ExpenseBook()
    for name in ["A", "B", "C"]:
        book.add_person(name)
    book.add_expense(
        payer="A",
        amount=Decimal("300.00"),
        participants=["A", "B", "C"],
        date="2026-10-16",
    )

    book.record_repayment(0, "B", Decimal("100.00"))

    assert book.status(0) == {
        "B": {"paid": Decimal("100.00"), "owes": Decimal("0.00")},
        "C": {"paid": Decimal("0.00"), "owes": Decimal("100.00")},
    }


def test_repayment_in_two_payments_fully_pays_participant_share() -> None:
    book = ExpenseBook()
    for name in ["A", "B", "C"]:
        book.add_person(name)
    book.add_expense(
        payer="A",
        amount=Decimal("300.00"),
        participants=["A", "B", "C"],
        date="2026-10-16",
    )

    book.record_repayment(0, "B", Decimal("40.00"))
    book.record_repayment(0, "B", Decimal("60.00"))

    assert book.status(0)["B"] == {
        "paid": Decimal("100.00"),
        "owes": Decimal("0.00"),
    }


def test_add_expense_stores_amount_with_two_decimal_places() -> None:
    book = ExpenseBook()
    book.add_person("A")

    expense = book.add_expense(
        payer="A",
        amount=Decimal("300"),
        participants=["A"],
        date="2026-10-16",
    )

    assert str(expense.amount) == "300.00"


def test_c5_repayment_by_nonparticipant_leaves_data_unchanged() -> None:
    book = ExpenseBook()
    for name in ["A", "B", "C", "D"]:
        book.add_person(name)
    book.add_expense(
        payer="A",
        amount=Decimal("300.00"),
        participants=["A", "B", "C"],
        date="2026-10-16",
    )
    original_expenses = list(book.expenses)
    original_repayments = dict(book.expenses[0].repayments)

    with pytest.raises(ValueError):
        book.record_repayment(0, "D", Decimal("50.00"))

    assert book.expenses == original_expenses
    assert book.expenses[0].repayments == original_repayments


def test_c6_totals_sum_remaining_amounts_without_netting() -> None:
    book = ExpenseBook()
    for name in ["A", "B", "C"]:
        book.add_person(name)
    book.add_expense(
        payer="A",
        amount=Decimal("300.00"),
        participants=["A", "B", "C"],
        date="2026-10-16",
    )
    book.add_expense(
        payer="A",
        amount=Decimal("90.00"),
        participants=["B", "C"],
        date="2026-10-16",
    )
    book.record_repayment(0, "B", Decimal("100.00"))

    assert book.totals() == {
        "B": {"A": Decimal("45.00")},
        "C": {"A": Decimal("145.00")},
    }


def test_repayment_with_no_expenses_leaves_data_unchanged() -> None:
    book = ExpenseBook()
    original_expenses = list(book.expenses)

    with pytest.raises(ValueError):
        book.record_repayment(0, "A", Decimal("1.00"))

    assert book.expenses == original_expenses


def test_overpayment_leaves_data_unchanged() -> None:
    book = ExpenseBook()
    for name in ["A", "B"]:
        book.add_person(name)
    book.add_expense(
        payer="A",
        amount=Decimal("10.00"),
        participants=["A", "B"],
        date="2026-10-16",
    )
    original_expenses = list(book.expenses)
    original_repayments = dict(book.expenses[0].repayments)

    with pytest.raises(ValueError):
        book.record_repayment(0, "B", Decimal("5.01"))

    assert book.expenses == original_expenses
    assert book.expenses[0].repayments == original_repayments


def test_payer_repaying_themselves_leaves_data_unchanged() -> None:
    book = ExpenseBook()
    book.add_person("A")
    book.add_expense(
        payer="A",
        amount=Decimal("10.00"),
        participants=["A"],
        date="2026-10-16",
    )
    original_expenses = list(book.expenses)
    original_repayments = dict(book.expenses[0].repayments)

    with pytest.raises(ValueError):
        book.record_repayment(0, "A", Decimal("1.00"))

    assert book.expenses == original_expenses
    assert book.expenses[0].repayments == original_repayments