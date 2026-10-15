# Design Notes and Assumptions

## 1. Weekly Contribution
Each group has one fixed weekly contribution amount, entered when the program starts. The amount must be greater than zero.

## 2. Member Registration
- Members are added in the order they join.
- Member names must not be empty.
- Names are treated as case-insensitive for duplicate checking.
- Membership is locked once the first contribution is recorded.

## 3. Contributions
- Members can pay in full or make partial payments.
- Payments must be greater than zero.
- Payments cannot exceed the member's outstanding balance.
- Money is represented using Python's `Decimal` to avoid floating-point rounding errors.
- Monetary amounts are limited to two decimal places.

## 4. Closing a Week
- A week can only close when every registered member has paid the full weekly contribution.
- If any member owes money, the week remains open.
- When the week closes, the total pot is calculated as the weekly contribution multiplied by the number of members.

## 5. Payout Rotation
- The first member added receives the first payout.
- Each successful weekly payout goes to the next member in joining order.
- After the last member receives a payout, the rotation starts again from the first member.

## 6. Reports
The report displays the current week, each member's paid amount, outstanding balance, and the payout history.

## 7. Validation
The program rejects unknown members, duplicate members, empty names, invalid monetary amounts, zero or negative payments, and overpayments.
