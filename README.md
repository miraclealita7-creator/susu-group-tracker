# Susu Group Tracker

## Overview
Susu Group Tracker is a command-line application for managing a rotating savings group. It records members, weekly contributions, outstanding balances, and payout history.

## Features
- Create a group with a fixed weekly contribution in GHS.
- Add unique members in joining order.
- Record full and partial contributions.
- Prevent overpayments and reject invalid payments.
- Prevent a week from closing while members still owe money.
- Pay the weekly pot to members in joining order.
- Display current-week reports and payout history.
- Use Python's `Decimal` for accurate money calculations.

## Requirements
- Python 3.11 or later

## How to Run
1. Open a terminal in the project folder.
2. Run `python main.py`.
3. Enter the fixed weekly contribution when prompted.
4. Follow the menu to manage members, payments, weekly payouts, and reports.

## How to Run Tests
Run the automated tests from the project root:

`python -m unittest discover -s Tests -v`

## Technology
- Python
- Decimal for monetary calculations
- unittest for automated testing

## Author
Project developed as part of a software development challenge.
## Example Usage

For example, if the weekly contribution is GHS 100 and the group has two members, the weekly pot will be GHS 200 once both members have paid in full.

The first member to join receives the first payout. The next member receives the following week's payout.

If a member has only paid part of their contribution, the tracker displays the outstanding balance and prevents the week from closing.

## Validation and Testing

The automated test suite covers:
- Valid and invalid group creation
- Duplicate and unknown members
- Full and partial payments
- Zero, negative, and excessive payments
- Preventing a week from closing when contributions are outstanding
- Payout rotation and week advancement
- Locking membership after contributions begin
