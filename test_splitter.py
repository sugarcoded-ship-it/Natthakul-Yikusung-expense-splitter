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