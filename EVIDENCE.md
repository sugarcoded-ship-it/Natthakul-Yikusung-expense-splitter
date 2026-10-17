# Checks and decisions

> This file records what I checked, what actually happened, and why I accepted or changed the work. It does not repeat setup instructions or the implementation plan.

## Concrete checks
Write the first two expectations before implementation. Fill in actual results after running them.

| Check / requirement | Given | When | Expected result | Actual result / pass or fail |
|---|---|---|---|---|
| C1 / R1, R3 — normal case | There is no record | Record an expense: payer A, amount 300.00, participants A, B and C, date 2026-10-16 | The record shows payer A, amount 300.00, date 2026-10-16, and a share of 100.00 for each of A, B and C | Pass. Option 4 shows one row: date 2026-10-16, payer A, amount 300.00, and a share of 100.00 under each of A, B and C. Test `test_add_expense_normal_case` passes. |
| C2 / R3 — boundary or failure case | People A, B and C exist, and no expenses are recorded. | Record an expense: payer A, amount -50, participants A and B | `ValueError` is raised, and the expense list is still empty. The menu shows an error message | Pass. Menu shows "Error: Expense amount must be greater than zero." and asks for the amount again; no expense is recorded. Test `test_add_expense_negative_amount_leaves_expense_list_empty` passes. |
| C3 / R2 | The expense from C1 exists | A records that B paid 100.00 | B shows as paid, and C still owes A 100.00 | Pass. Option 4 shows B as "100.00 / paid 100.00 / owes 0.00" and C as "100.00 / paid 0.00 / owes 100.00"; Totals show only "C → A 100.00". Test `test_c3_repayment_updates_status` passes. |
| C4 / R3, rounding | An expense of 100.00 shared by A, B and C | Calculate the shares | The shares add up to exactly 100.00 (for example A 33.34, B 33.33, C 33.33, because the first participant listed takes the extra cent) | Pass. Shares are A 33.34, B 33.33, C 33.33, total 100.00. Test `test_calculates_c4_shares_with_leftover_cent_for_first_participant` passes. |
| C5 / R2, R3 | The expense from C1 exists | A records that D paid 50.00 | Program raises `ValueError` and data stays unchanged | Pass. `ValueError` "D is not a participant in this expense"; repayments unchanged. Test `test_c5_repayment_by_nonparticipant_leaves_data_unchanged` passes. |
| C6 / R2 | Expense 1: payer A, 300.00, participants A, B, C. Expense 2: payer A, 90.00, participants B, C. B has repaid 100.00 on expense 1 | View total per person | B owes A 45.00, and C owes A 145.00 | Pass. Totals are B owes A 45.00, C owes A 145.00. Test `test_c6_totals_sum_remaining_amounts_without_netting` passes. |
| C7 / R1, R3 | People A and B exist, and there are no expenses | Record an expense with date 2026-13-40 | `ValueError` is raised, and the expense list is still empty | Pass. Menu shows "Error: Expense date must be a valid YYYY-MM-DD date." and asks for the date again; no expense is recorded. Test `test_c7_invalid_date_leaves_expenses_unchanged` passes. |

## Two review decisions
- Plan decision: I did not approve adding trips (separate groups) because it is not in R1–R3 and AGENTS.md says no extra features. I kept one group and listed it as a limitation.
- Code decision: In `splitter.py` `add_expense`, shares showed as `100` instead of `100.00`, but the tests still passed because Decimal compares values, not decimal places. I asked Copilot to round shares to 2 decimals and to check the text in the tests.

## Automated tests
- Test file and behaviour checked: `test_splitter.py` covers C1–C7, plus invalid input that must raise `ValueError` and leave data unchanged: duplicate person, no participants, unknown payer or participant, duplicate participants, more than 2 decimals, NaN, Infinity, float amount, empty date, repayment with no expenses, overpayment, and the payer repaying themselves. It also checks a 0.01 split, a repayment made in two parts, and that amounts and shares are stored with 2 decimals.
- Command I ran: `uv run pytest`
- Final result: 27 passed, 0 failed.
- Correction and rerun, if needed: After review I asked for fixes and reran the tests each time. Shares displayed as `100` instead of `100.00` (tests missed it because Decimal equality ignores decimal places, so text checks were added). `Decimal("NaN")`, `Infinity` and floats crashed instead of raising `ValueError`. A changed error message was wrongly applied to `add_expense` as well and was reverted. Real use showed record repayment could loop forever when the person had already paid. Added cancel with Enter and amount_owed in `splitter.py`.

## Realistic use and final judgment
- Task I tried: A weekend trip with 4 people (me, Ben, Cara, Dan): hotel 1200.00, dinner 450.00, taxi 100.00, snacks 85.50 and tickets 60.00, with different people sharing each one. Then I recorded 2 repayments (Ben paid me 300.00 for the hotel, Dan paid Ben 50.00 for dinner) and viewed who still owes.
- Outcome:  All totals matched what I worked out by hand, for example Dan → You 342.75 (300.00 hotel + 42.75 snacks). Re-asking a wrong amount or date, and the "already paid" message, made it easy to use. But the expense table was about 165 characters wide with 4 people, so it wrapped in my terminal and was hard to read. The totals also show me owing Ben 112.50 while Ben owes me 42.75, instead of one payment of 69.75.
- Judgment: Partly done. R1–R3 work and all 27 tests pass, but the main view is hard to read for a real group of 4, and without netting it doesn't fully answer "who should pay whom" from the Purpose.
- Remaining limitation or unfinished work: Totals are not netted between two people, so friends make more payments than needed. Netting the totals would be the next step. Data is also lost when the program closes.