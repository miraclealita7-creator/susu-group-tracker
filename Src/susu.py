
from decimal import Decimal, InvalidOperation


class SusuGroup:
    """Manage one rotating savings group."""

    def __init__(self, weekly_contribution):
        self.weekly_contribution = self._to_money(
            weekly_contribution
        )

        if self.weekly_contribution <= Decimal("0.00"):
            raise ValueError("Weekly contribution must be positive.")

        self.members = []
        self.member_names = set()
        self.current_week = 1
        self.membership_locked = False
        self.payments = {}
        self.payout_history = []

    @staticmethod
    def _to_money(amount):
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Enter a valid monetary amount.") from None

        if not value.is_finite():
            raise ValueError("Amount must be finite.")

        if value.as_tuple().exponent < -2:
            raise ValueError(
                "Money cannot have more than 2 decimal places."
            )

        return value.quantize(Decimal("0.01"))

    def add_member(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Member name cannot be empty.")

        if self.membership_locked:
            raise ValueError(
                "Cannot add members after contributions begin."
            )

        clean_name = name.strip()
        normalized_name = clean_name.casefold()

        if normalized_name in self.member_names:
            raise ValueError("This member already exists.")

        self.members.append(clean_name)
        self.member_names.add(normalized_name)
        self.payments[clean_name] = Decimal("0.00")

    def record_contribution(self, member_name, amount):
        if member_name not in self.payments:
            raise ValueError("Unknown member.")

        payment = self._to_money(amount)

        if payment <= Decimal("0.00"):
            raise ValueError("Payment must be positive.")

        already_paid = self.payments[member_name]
        outstanding = self.weekly_contribution - already_paid

        if payment > outstanding:
            raise ValueError(
                "Payment exceeds the outstanding balance."
            )

        self.payments[member_name] += payment
        self.membership_locked = True

    def close_week(self):
        if not self.members:
            raise ValueError(
                "Add at least one member before closing a week."
            )

        owing = self.get_outstanding_balances()

        if owing:
            return {
                "closed": False,
                "week": self.current_week,
                "owing": owing,
                "payout": None,
            }

        recipient_index = (
            len(self.payout_history) % len(self.members)
        )
        recipient = self.members[recipient_index]
        pot = self.weekly_contribution * len(self.members)

        payout = {
            "week": self.current_week,
            "recipient": recipient,
            "amount": pot,
        }

        self.payout_history.append(payout)
        closed_week = self.current_week
        self.current_week += 1

        self.payments = {
            member: Decimal("0.00")
            for member in self.members
        }

        return {
            "closed": True,
            "week": closed_week,
            "owing": {},
            "payout": payout,
        }

    def get_outstanding_balances(self):
        return {
            member: self.weekly_contribution - paid
            for member, paid in self.payments.items()
            if paid < self.weekly_contribution
        }

    def get_report(self):
        return {
            "current_week": self.current_week,
            "weekly_contribution": self.weekly_contribution,
            "members": {
                member: {
                    "paid": self.payments[member],
                    "owes": (
                        self.weekly_contribution
                        - self.payments[member]
                    ),
                }
                for member in self.members
            },
            "payout_history": list(self.payout_history),
        }

