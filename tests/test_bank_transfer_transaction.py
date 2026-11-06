"""Provide unit tests for bank transfer transactions.

Author: Jashandeep Kaur
"""

import unittest
from decimal import Decimal

from account.account_status import AccountStatus
from account.bank_account import BankAccount
from account.client import Client
from transaction.bank_transfer_transaction import BankTransferTransaction
from transaction.transaction_status import TransactionStatus
from fee.base_percentage_fee_strategy import BasePercentageFeeStrategy

class TestBankTransferTransaction(unittest.TestCase):
    """Test bank transfer initialization, fees, and processing."""

    def setUp(self):
        """Create fresh active accounts and a transfer for each test."""
        owner = Client(1010, "Pete Zahut", "pzahut@example.com")
        self.source = BankAccount(
            123456, Decimal("1000.00"), owner, AccountStatus.ACTIVE
        )
        self.target = BankAccount(
            676767, Decimal("500.00"), owner, AccountStatus.ACTIVE
        )
        self.transfer = BankTransferTransaction(
            "98765", Decimal("100.00"), self.source, self.target
        )
        self.transfer.set_fee_strategy(
            BasePercentageFeeStrategy(Decimal("1.00"), Decimal("0.007"))
        )

    # Constructor tests

    def test_init_transaction_id_blank(self):
        """Verify a blank identifier raises the required error."""
        with self.assertRaises(ValueError) as context:
            BankTransferTransaction(
                "   ", Decimal("100.00"), self.source, self.target
            )

        self.assertEqual(
            "transaction_id cannot be blank.",
            str(context.exception)
        )

    def test_init_amount_negative(self):
        """Verify a negative amount raises the required error."""
        with self.assertRaises(ValueError) as context:
            BankTransferTransaction(
                "98765", Decimal("-1.00"), self.source, self.target
            )

        self.assertEqual(
            "amount must be greater than zero.",
            str(context.exception)
        )

    def test_init_amount_zero(self):
        """Verify zero raises the required error."""
        with self.assertRaises(ValueError) as context:
            BankTransferTransaction(
                "98765", Decimal("0.00"), self.source, self.target
            )

        self.assertEqual(
            "amount must be greater than zero.",
            str(context.exception)
        )

    def test_init_new_instance(self):
        """Verify all inherited and subclass attributes are initialized."""
        self.assertEqual(
            "98765", self.transfer._Transaction__transaction_id
        )
        self.assertEqual(
            Decimal("100.00"), self.transfer._Transaction__amount
        )
        self.assertEqual(
            TransactionStatus.PENDING,
            self.transfer._Transaction__status
        )
        self.assertIs(
            self.source, self.transfer._Transaction__account
        )
        self.assertIs(
            self.target,
            self.transfer._BankTransferTransaction__target_account
        )

    # Fee tests

    def test_fees_returns_base_fee(self):
        """Verify the $1 minimum applies when the percentage is smaller."""
        self.assertEqual(Decimal("1.00"), self.transfer.fees)

    def test_fees_returns_percentage(self):
        """Verify the fee is 0.7% when it exceeds the minimum."""
        transfer = BankTransferTransaction(
            "98765", Decimal("500.00"), self.source, self.target
        )
        
        transfer.set_fee_strategy(
            BasePercentageFeeStrategy(Decimal("1.00"), Decimal("0.007"))
        )

        self.assertEqual(Decimal("3.50"), transfer.fees)

    # Processing tests

    def test_process_source_not_active(self):
        """Verify an inactive source fails without moving funds."""
        self.source.status = AccountStatus.INACTIVE

        self.transfer.process()

        self.assertEqual(
            TransactionStatus.FAILED, self.transfer.status
        )
        self.assertEqual(Decimal("1000.00"), self.source.balance)
        self.assertEqual(Decimal("500.00"), self.target.balance)

    def test_process_target_not_active(self):
        """Verify an inactive target fails without moving funds."""
        self.target.status = AccountStatus.INACTIVE

        self.transfer.process()

        self.assertEqual(
            TransactionStatus.FAILED, self.transfer.status
        )
        self.assertEqual(Decimal("1000.00"), self.source.balance)
        self.assertEqual(Decimal("500.00"), self.target.balance)

    def test_process_amount_and_fee_exceed_balance(self):
        """Verify insufficient funds fail without moving funds."""
        transfer = BankTransferTransaction(
            "98765", Decimal("1000.00"), self.source, self.target
        )

        transfer.set_fee_strategy(
            BasePercentageFeeStrategy(Decimal("1.00"), Decimal("0.007"))
        )

        transfer.process()

        self.assertEqual(TransactionStatus.FAILED, transfer.status)
        self.assertEqual(Decimal("1000.00"), self.source.balance)
        self.assertEqual(Decimal("500.00"), self.target.balance)

    def test_process_valid_transaction(self):
        """Verify processing debits fees, credits funds, and sets status."""
        self.transfer.process()

        self.assertEqual(Decimal("899.00"), self.source.balance)
        self.assertEqual(Decimal("600.00"), self.target.balance)
        self.assertEqual(
            TransactionStatus.PROCESSED, self.transfer.status
        )

    # String representation test

    def test_str_returns_required_format(self):
        """Verify the complete transfer string matches the required format."""
        transfer = BankTransferTransaction(
            "98765", Decimal("2983.35"), self.source, self.target
        )

        self.assertEqual(
            "ID: 98765\n"
            "STATUS: PENDING\n"
            "AMOUNT: $2,983.35\n"
            "SOURCE ACCT: 123456 --> TARGET ACCT: 676767",
            str(transfer)
        )