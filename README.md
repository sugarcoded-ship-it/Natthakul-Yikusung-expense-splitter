# Expense Splitter

> This file explains who the project is for, what it should do, and how to run it.

## Purpose
A command-line tool that helps a group of friends record shared expenses and work out who should pay whom to settle up.

## Requirements
- R1: The user can record an expense with payer, participants, amount and date. The record shows each participant's share (amount ÷ number of participants).
- R2: The user can record that a participant has paid the payer back, and view for each expense who has paid and who still owes. The view also shows, for each person, the total they still owe each payer across all expenses.
- R3: Shares are calculated automatically and rounded to 2 decimals so they add up exactly to the amount. Invalid input is rejected and leaves the data unchanged: amount ≤ 0, no participants, a payer/participant who is not an existing person, an invalid repayment, or a date that is not in YYYY-MM-DD format.

## Setup and use
- Prerequisites: uv and python 3.12
- Setup:
  1. `git clone https://github.com/sugarcoded-ship-it/Natthakul-Yikusung-expense-splitter` and `cd Natthakul-Yikusung-expense-splitter`
  2. `uv sync`
- Run: `uv run python main.py`, then choose an option from the menu.
- Run tests: `uv run pytest`

## Author and acknowledgements
- Name / student ID: Natthakul Yikusung 6680972
- AI tools used: Copilot
- External code/resources: None

See PLAN.md for the implementation plan and EVIDENCE.md for results and decisions.