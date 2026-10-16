# Instructions for this repository

> This file tells the coding agent how to work on this project. It does not replace the requirements or plan.

- Read README.md, PLAN.md and the checks in EVIDENCE.md before implementing.
- Keep changes within the three requirements in README.md. Do not add extra features (no saving to files, no GUI, no user accounts).
- Use Python 3.12+ managed with uv. Add dependencies with `uv add` (never `pip install`). Use only the standard library, plus pytest as a dev dependency.
- Keep calculation and rules in `splitter.py` with no `input()` or `print()` calls. Keep all user interaction in `main.py`.
- Use the terms "payer" (the person who paid first) and "participants" (the people who share the expense) in code, comments and tests.
- Use `decimal.Decimal` for money, never `float`. Round to 2 decimal places, and make sure the shares of an expense add up exactly to its amount.
- Invalid input (amount <= 0, no participants, unknown person, invalid repayment) must raise a clear `ValueError` and leave existing data unchanged.
- Run tests with: `uv run pytest`
- Do not change an expected result merely to make a test pass. Raise any disagreement for review.
- Leave requirements, expected results, decision notes and the final judgment for the student to write.