
import unittest
from decimal import Decimal

from Src.susu import SusuGroup


class TestSusuGroup(unittest.TestCase):

    def setUp(self):
        self.group = SusuGroup("50.00")
        self.group.add_member("Ama")
        self.group.add_member("Kofi")
        self.group.add_member("Esi")

    def test_group_creation(self):
        self.assertEqual(
            self.group.weekly_contribution,
            Decimal("50.00")
        )
        self.assertEqual(self.group.current_week, 1)

    def test_duplicate_member_is_rejected(self):
        with self.assertRaises(ValueError):
            self.group.add_member("ama")

    def test_partial_payment(self):
        self.group.record_contribution("Esi", "30.00")

        report = self.group.get_report()

        self.assertEqual(
            report["members"]["Esi"]["paid"],
            Decimal("30.00")
        )
        self.assertEqual(
            report["members"]["Esi"]["owes"],
            Decimal("20.00")
        )

    def test_week_cannot_close_when_member_owes(self):
        self.group.record_contribution("Ama", "50.00")
        self.group.record_contribution("Kofi", "50.00")
        self.group.record_contribution("Esi", "30.00")

        result = self.group.close_week()

        self.assertFalse(result["closed"])
        self.assertIsNone(result["payout"])
        self.assertEqual(
            result["owing"]["Esi"],
            Decimal("20.00")
        )
        self.assertEqual(self.group.current_week, 1)

    def test_full_payment_allows_payout(self):
        for member in self.group.members:
            self.group.record_contribution(member, "50.00")

        result = self.group.close_week()

        self.assertTrue(result["closed"])
        self.assertEqual(result["payout"]["recipient"], "Ama")
        self.assertEqual(
            result["payout"]["amount"],
            Decimal("150.00")
        )
        self.assertEqual(self.group.current_week, 2)

    def test_payment_above_outstanding_balance_is_rejected(self):
        self.group.record_contribution("Ama", "30.00")

        with self.assertRaises(ValueError):
            self.group.record_contribution("Ama", "21.00")

    def test_unknown_member_is_rejected(self):
        with self.assertRaises(ValueError):
            self.group.record_contribution("Unknown", "10.00")

    def test_zero_and_negative_payments_are_rejected(self):
        for amount in ("0.00", "-10.00"):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.group.record_contribution("Ama", amount)

    def test_payout_order_advances(self):
        for expected_recipient in ("Ama", "Kofi"):
            for member in self.group.members:
                self.group.record_contribution(member, "50.00")

            result = self.group.close_week()

            self.assertTrue(result["closed"])
            self.assertEqual(
                result["payout"]["recipient"],
                expected_recipient
            )

    def test_invalid_weekly_contribution_is_rejected(self):
        for amount in ("0.00", "-50.00"):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    SusuGroup(amount)


if __name__ == "__main__":
    unittest.main()
