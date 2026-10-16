# Implementation plan

> This file records my project-specific steps reviewed before coding. Replace the prompts below with the agreed plan; refer to R1–R3 rather than copying the requirements here.

## Steps
1. Create `splitter.py` with the data structures (dataclasses for a person's name and an expense) and an `ExpenseBook` class that holds people and expenses, with `add_person`. Create an empty `test_splitter.py`. Run `uv run pytest` once to confirm the setup works.
2. Implement `add_expense(payer, amount, participants, date)` in `splitter.py` for R1. It stores the payer, participants, amount and date, and rejects an unknown person, no participants, or amount <= 0 without changing the data (R3). Write the tests for C1 (normal case) and C2 (negative amount) with this step, using the expected results already in EVIDENCE.md.
3. Implement the share calculation for R3 using `Decimal`: split the amount into cents, and give any leftover cents one at a time to participants in the order listed, so shares add up exactly to the amount. Test C4 (100.00 among A, B and C gives 33.34, 33.33, 33.33).
4. Implement `record_repayment(expense, from_person, amount)` and a status view for R2. Repayments go to the expense's payer. Reject a person who is not a participant, the payer repaying themselves, and an amount that is <= 0 or more than the person still owes. Test C3 (A records that B paid 100.00) and C5 (D is not a participant, so it is rejected). Also add a totals view that sums, for each person, what they still owe each payer across all expenses (no netting). Test C6.
5. Create `main.py`, a text menu for the user: add person, add expense, record repayment, view expenses and who still owes. It only calls `splitter.py` and prints results, with no calculation of its own. Check C1 and C2 by hand through the menu too.
6. Run all tests with `uv run pytest` and record the result in EVIDENCE.md. Then try a realistic task from start to finish: enter a real group dinner or trip with 3 to 4 people and 5 to 6 expenses, record a few repayments, and judge whether the output is useful.

## Later changes, if any
Added per-person totals to R2 because the Purpose promises "who should pay whom", but the per-expense view alone didn't show it.