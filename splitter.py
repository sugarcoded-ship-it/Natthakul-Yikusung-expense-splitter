from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Person:
    name: str


@dataclass
class Expense:
    payer: str
    participants: list[str]
    amount: Decimal
    date: str
    shares: dict[str, Decimal]


class ExpenseBook:
    def __init__(self) -> None:
        self.people: dict[str, Person] = {}
        self.expenses: list[Expense] = []

    def add_person(self, name: str) -> Person:
        name = name.strip()
        if not name:
            raise ValueError("Person name cannot be empty.")
        if name in self.people:
            raise ValueError(f"Person already exists: {name}")

        person = Person(name=name)
        self.people[name] = person
        return person

    def add_expense(
        self,
        payer: str,
        amount: Decimal,
        participants: list[str],
        date: str,
    ) -> Expense:
        participant_names = list(participants)
        if not isinstance(amount, Decimal) or not amount.is_finite():
            raise ValueError("Expense amount must be a finite Decimal.")
        if amount <= 0:
            raise ValueError("Expense amount must be greater than zero.")
        if amount.as_tuple().exponent < -2:
            raise ValueError("Expense amount cannot have more than two decimal places.")
        if not participant_names:
            raise ValueError("Expense must have at least one participant.")
        if len(set(participant_names)) != len(participant_names):
            raise ValueError("Expense participants must be unique.")
        if payer not in self.people:
            raise ValueError(f"Unknown payer: {payer}")
        unknown_participants = [
            name for name in participant_names if name not in self.people
        ]
        if unknown_participants:
            raise ValueError(f"Unknown participant: {unknown_participants[0]}")
        if not date.strip():
            raise ValueError("Expense date cannot be empty.")

        total_cents = int(amount * 100)
        base_share_cents, leftover_cents = divmod(
            total_cents, len(participant_names)
        )
        shares = {
            name: (
                Decimal(base_share_cents + (index < leftover_cents)) / 100
            ).quantize(Decimal("0.01"))
            for index, name in enumerate(participant_names)
        }
        expense = Expense(
            payer=payer,
            participants=participant_names,
            amount=amount,
            date=date,
            shares=shares,
        )
        self.expenses.append(expense)
        return expense
