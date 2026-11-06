"""Test transaction logging and sender validation."""

import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from io import StringIO

from account.account_status import AccountStatus
from account.bank_account import BankAccount
from account.client import Client
from events.logging_listener import LoggingListener
from transaction.credit_card_transaction import CreditCardTransaction


class TestLoggingListener(unittest.TestCase):
    """Verify logging output and invalid sender handling."""

    def setUp(self):
        """Create a listener and a transaction."""
        owner = Client(1010, "Pete Zahut", "pzahut@example.com")
        account = BankAccount(
            123456, Decimal("1000.00"), owner, AccountStatus.ACTIVE
        )
        self.payment = CreditCardTransaction(
            "98765", Decimal("100.00"), account, "AUTH-123"
        )
        self.listener = LoggingListener()

    def test_update_logs_transaction(self):
        """Verify the heading, separators, and transaction details."""
        output = StringIO()

        with redirect_stdout(output):
            self.listener.update(self.payment)

        expected = (
            "TRANSACTION PROCESSED\n"
            + "=" * 60
            + "\n"
            + str(self.payment)
            + "\n"
            + "=" * 60
            + "\n"
        )
        self.assertEqual(expected, output.getvalue())

    def test_update_rejects_invalid_sender(self):
        """Verify invalid senders raise the required TypeError."""
        for sender in (None, "transaction", 123, object()):
            with self.subTest(sender=sender):
                with self.assertRaises(TypeError) as context:
                    self.listener.update(sender)

                self.assertEqual(
                    "sender must be a Transaction type.",
                    str(context.exception)
                )

    def test_successful_processing_triggers_logging(self):
        """Verify a subscribed listener logs a processed transaction."""
        self.payment.on_processed.add_listener(self.listener)
        output = StringIO()

        with redirect_stdout(output):
            self.payment.process()

        self.assertIn("TRANSACTION PROCESSED", output.getvalue())
        self.assertIn("STATUS: PROCESSED", output.getvalue())
        self.assertIn("ID: 98765", output.getvalue())

    def test_failed_processing_does_not_log(self):
        """Verify a failed transaction does not notify the listener."""
        self.payment.account.status = AccountStatus.INACTIVE
        self.payment.on_processed.add_listener(self.listener)
        output = StringIO()

        with redirect_stdout(output):
            self.payment.process()

        self.assertEqual("", output.getvalue())