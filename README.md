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
