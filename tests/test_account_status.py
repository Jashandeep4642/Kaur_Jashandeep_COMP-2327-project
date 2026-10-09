"""Provide unit tests for the AccountStatus enumeration.

Author: Jashandeep Kaur
"""

import unittest

from account.account_status import AccountStatus


class TestAccountStatus(unittest.TestCase):
    """Test the values defined by AccountStatus."""

    def test_account_status_values_initialized(self):
        """Verify all four statuses have the expected integer values."""
        self.assertEqual(0, AccountStatus.INACTIVE.value)
        self.assertEqual(1, AccountStatus.ACTIVE.value)
        self.assertEqual(2, AccountStatus.SUSPENDED.value)
        self.assertEqual(3, AccountStatus.CLOSED.value)