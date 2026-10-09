"""Provide unit tests for the TransactionStatus enumeration.

Author: Jashandeep Kaur
"""

import unittest

from transaction.transaction_status import TransactionStatus


class TestTransactionStatus(unittest.TestCase):
    """Test the values defined by TransactionStatus."""

    def test_transaction_status_values_initialized(self):
        """Verify all transaction statuses have the required values."""
        self.assertEqual(1, TransactionStatus.PENDING.value)
        self.assertEqual(2, TransactionStatus.PROCESSED.value)
        self.assertEqual(3, TransactionStatus.FAILED.value)