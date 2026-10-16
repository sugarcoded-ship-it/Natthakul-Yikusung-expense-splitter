from dataclasses import dataclass, field
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
    repayments: dict[str, Decimal] = field(default_factory=dict)


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

        stored_amount = amount.quantize(Decimal("0.01"))
        total_cents = int(stored_amount * 100)
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
            amount=stored_amount,
            date=date,
            shares=shares,
        )
        self.expenses.append(expense)
        return expense

    def record_repayment(
        self,
        expense_index: int,
        from_person: str,
        amount: Decimal,
    ) -> None:
        if not isinstance(amount, Decimal) or not amount.is_finite():
            raise ValueError("Repayment amount must be a finite Decimal.")
        if amount.as_tuple().exponent < -2:
            raise ValueError(
                "Repayment amount cannot have more than two decimal places."
            )
        if amount <= 0:
            raise ValueError("Repayment amount must be greater than zero.")
        if not isinstance(expense_index, int) or not (
            0 <= expense_index < len(self.expenses)
        ):
            raise ValueError(f"Unknown expense index: {expense_index}")

        expense = self.expenses[expense_index]
        if from_person not in expense.participants:
            raise ValueError(
                f"{from_person} is not a participant in this expense"
            )
        if from_person == expense.payer:
            raise ValueError("The payer cannot repay themselves.")

        repayment_amount = amount.quantize(Decimal("0.01"))
        already_paid = expense.repayments.get(from_person, Decimal("0.00"))
        still_owes = expense.shares[from_person] - already_paid
        if repayment_amount > still_owes:
            raise ValueError("Repayment exceeds the amount still owed.")

        expense.repayments[from_person] = already_paid + repayment_amount

    def status(self, expense_index: int) -> dict[str, dict[str, Decimal]]:
        if not isinstance(expense_index, int) or not (
            0 <= expense_index < len(self.expenses)
        ):
            raise ValueError(f"Unknown expense index: {expense_index}")

        expense = self.expenses[expense_index]
        return {
            participant: {
                "paid": expense.repayments.get(participant, Decimal("0.00")),
                "owes": expense.shares[participant]
                - expense.repayments.get(participant, Decimal("0.00")),
            }
            for participant in expense.participants
            if participant != expense.payer
        }

    def totals(self) -> dict[str, dict[str, Decimal]]:
        owed_totals: dict[str, dict[str, Decimal]] = {}
        for expense in self.expenses:
            for participant in expense.participants:
                if participant == expense.payer:
                    continue
                remaining = expense.shares[participant] - expense.repayments.get(
                    participant, Decimal("0.00")
                )
                payer_totals = owed_totals.setdefault(participant, {})
                payer_totals[expense.payer] = (
                    payer_totals.get(expense.payer, Decimal("0.00")) + remaining
                ).quantize(Decimal("0.01"))
        return owed_totals
