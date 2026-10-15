
import unittest

from Src.susu import SusuGroup


class MembershipLockTests(unittest.TestCase):

    def test_cannot_add_member_after_contributions_begin(self):
        group = SusuGroup("100")
        group.add_member("Miracle")

        group.record_contribution("Miracle", "50")

        with self.assertRaises(ValueError):
            group.add_member("Ada")


if __name__ == "__main__":
    unittest.main()
