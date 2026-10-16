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
