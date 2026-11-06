"""Provide unit tests for credit card transactions.

Author: Jashandeep Kaur
"""

import unittest
from decimal import Decimal

from account.account_status import AccountStatus
from account.bank_account import BankAccount
from account.client import Client
from transaction.credit_card_transaction import CreditCardTransaction
from transaction.transaction_status import TransactionStatus
from fee.percentage_fee_strategy import PercentageFeeStrategy

class TestCreditCardTransaction(unittest.TestCase):
    """Test credit card initialization, fees, and processing."""

    def setUp(self):
        """Create a fresh active account and payment for each test."""
        owner = Client(1010, "Pete Zahut", "pzahut@example.com")
        self.account = BankAccount(
            123456, Decimal("1000.00"), owner, AccountStatus.ACTIVE
        )
        self.payment = CreditCardTransaction(
            "98765", Decimal("100.00"), self.account, "AUTH-123"
        )

        self.payment = CreditCardTransaction(
            "98765", Decimal("100.00"), self.account, "AUTH-123"
        )
        self.payment.set_fee_strategy(
            PercentageFeeStrategy(Decimal("0.02"))
        )

    # Constructor tests

    def test_init_transaction_id_blank(self):
        """Verify a blank identifier raises the required error."""
        with self.assertRaises(ValueError) as context:
            CreditCardTransaction(
                "   ", Decimal("100.00"), self.account, "AUTH-123"
            )

        self.assertEqual(
            "transaction_id cannot be blank.",
            str(context.exception)
        )

    def test_init_amount_negative(self):
        """Verify a negative amount raises the required error."""
        with self.assertRaises(ValueError) as context:
            CreditCardTransaction(
                "98765", Decimal("-1.00"), self.account, "AUTH-123"
            )

        self.assertEqual(
            "amount must be greater than zero.",
            str(context.exception)
        )

    def test_init_amount_zero(self):
        """Verify zero raises the required error."""
        with self.assertRaises(ValueError) as context:
            CreditCardTransaction(
                "98765", Decimal("0.00"), self.account, "AUTH-123"
            )

        self.assertEqual(
            "amount must be greater than zero.",
            str(context.exception)
        )

    def test_init_new_instance(self):
        """Verify all inherited and subclass attributes are initialized."""
        self.assertEqual(
            "98765", self.payment._Transaction__transaction_id
        )
        self.assertEqual(
            Decimal("100.00"), self.payment._Transaction__amount
        )
        self.assertEqual(
            TransactionStatus.PENDING,
            self.payment._Transaction__status
        )
        self.assertIs(
            self.account, self.payment._Transaction__account
        )
        self.assertEqual(
            "AUTH-123",
            self.payment._CreditCardTransaction__authorization_code
        )

    # Fee test

    def test_fees_returns_two_percent(self):
        """Verify the fee equals 2% of the payment amount."""
        self.assertEqual(Decimal("2.00"), self.payment.fees)

    # Processing tests

    def test_process_account_not_active(self):
        """Verify an inactive account fails without withdrawing funds."""
        self.account.status = AccountStatus.INACTIVE

        self.payment.process()

        self.assertEqual(TransactionStatus.FAILED, self.payment.status)
        self.assertEqual(Decimal("1000.00"), self.account.balance)

    def test_process_amount_and_fee_exceed_balance(self):
        """Verify insufficient funds fail without withdrawing funds."""
        payment = CreditCardTransaction(
            "98765", Decimal("1000.00"), self.account, "AUTH-123"
        )

        payment.set_fee_strategy(
            PercentageFeeStrategy(Decimal("0.02"))
        )

        payment.process()

        self.assertEqual(TransactionStatus.FAILED, payment.status)
        self.assertEqual(Decimal("1000.00"), self.account.balance)
        
    def test_process_authorization_code_blank(self):
        """Verify a blank authorization code fails without moving funds."""
        payment = CreditCardTransaction(
            "98765", Decimal("100.00"), self.account, "   "
        )

        payment.process()

        self.assertEqual(TransactionStatus.FAILED, payment.status)
        self.assertEqual(Decimal("1000.00"), self.account.balance)

    def test_process_valid_transaction(self):
        """Verify processing withdraws the amount and fee and sets status."""
        self.payment.process()

        self.assertEqual(Decimal("898.00"), self.account.balance)
        self.assertEqual(
            TransactionStatus.PROCESSED, self.payment.status
        )

    # String representation test

    def test_str_returns_required_format(self):
        """Verify the complete payment string matches the required format."""
        payment = CreditCardTransaction(
            "98765", Decimal("2983.35"), self.account, "AUTH-123"
        )

        self.assertEqual(
            "ID: 98765\n"
            "STATUS: PENDING\n"
            "AMOUNT: $2,983.35\n"
            "SOURCE ACCT: 123456\n"
            "AUTH CODE: AUTH-123",
            str(payment)
        )