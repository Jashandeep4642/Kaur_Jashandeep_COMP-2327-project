"""Provide unit tests for the BankAccount class.

Author: Jashandeep Kaur
"""

import unittest
from decimal import Decimal

from account.bank_account import BankAccount
from account.account_status import AccountStatus
from account.client import Client


class TestBankAccount(unittest.TestCase):
    """Test BankAccount initialization, properties, and methods."""

    def setUp(self):
        """Create a client and a fresh account before each test."""
        self.owner = Client(
            1010,
            "Pete Zahut",
            "pzahut@yarrow-mullain.ca"
        )
        self.account = BankAccount(
            20019,
            Decimal("1000.00"),
            self.owner,
            AccountStatus.ACTIVE
        )

    # Constructor tests

    def test_init_account_id_less_than_zero(self):
        """Verify a negative account ID raises the expected error."""
        with self.assertRaises(ValueError) as context:
            BankAccount(
                -1,
                Decimal("1000.00"),
                self.owner,
                AccountStatus.ACTIVE
            )

        self.assertEqual(
            "account_id must be a value greater than zero.",
            str(context.exception)
        )

    def test_init_account_id_zero(self):
        """Verify an account ID of zero raises the expected error."""
        with self.assertRaises(ValueError) as context:
            BankAccount(
                0,
                Decimal("1000.00"),
                self.owner,
                AccountStatus.ACTIVE
            )

        self.assertEqual(
            "account_id must be a value greater than zero.",
            str(context.exception)
        )

    def test_init_new_instance(self):
        """Verify the constructor initializes all private attributes."""
        account = BankAccount(
            20019,
            Decimal("1000.00"),
            self.owner,
            AccountStatus.ACTIVE
        )

        self.assertEqual(20019, account._BankAccount__account_id)
        self.assertEqual(
            Decimal("1000.00"),
            account._BankAccount__balance
        )
        self.assertEqual(
            self.owner,
            account._BankAccount__owner
        )
        self.assertEqual(
            AccountStatus.ACTIVE,
            account._BankAccount__status
        )

    # Property tests

    def test_account_id_returns_current_state(self):
        """Verify account_id returns the stored identifier."""
        self.assertEqual(20019, self.account.account_id)

    def test_balance_returns_current_state(self):
        """Verify balance returns the stored balance."""
        self.assertEqual(
            Decimal("1000.00"),
            self.account.balance
        )

    def test_owner_returns_current_state(self):
        """Verify owner returns the stored client."""
        self.assertEqual(self.owner, self.account.owner)

    def test_status_returns_current_state(self):
        """Verify status returns the stored account status."""
        self.assertEqual(
            AccountStatus.ACTIVE,
            self.account.status
        )

    def test_status_setter_updates_status(self):
        """Verify the status setter updates the private status."""
        self.account.status = AccountStatus.SUSPENDED

        self.assertEqual(
            AccountStatus.SUSPENDED,
            self.account._BankAccount__status
        )

    # Private balance update tests

    def test_update_balance_increase_with_positive_amount(self):
        """Verify a positive adjustment increases the balance."""
        self.account._BankAccount__update_balance(Decimal("100.00"))

        self.assertEqual(
            Decimal("1100.00"),
            self.account._BankAccount__balance
        )

    def test_update_balance_decrease_with_negative_amount(self):
        """Verify a negative adjustment decreases the balance."""
        self.account._BankAccount__update_balance(Decimal("-100.00"))

        self.assertEqual(
            Decimal("900.00"),
            self.account._BankAccount__balance
        )

    # Deposit tests

    def test_deposit_amount_less_than_zero(self):
        """Verify a negative deposit raises the expected error."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(Decimal("-100.00"))

        self.assertEqual(
            "amount must be a value greater than or equal to zero.",
            str(context.exception)
        )

    def test_deposit_amount_zero(self):
        """Verify depositing zero leaves the balance unchanged."""
        self.account.deposit(Decimal("0.00"))

        self.assertEqual(
            Decimal("1000.00"),
            self.account._BankAccount__balance
        )

    def test_deposit_increase_balance_by_amount(self):
        """Verify a deposit increases the balance by its amount."""
        self.account.deposit(Decimal("100.00"))

        self.assertEqual(
            Decimal("1100.00"),
            self.account._BankAccount__balance
        )

    # Withdrawal tests

    def test_withdraw_amount_less_than_zero(self):
        """Verify a negative withdrawal raises the expected error."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(Decimal("-100.00"))

        self.assertEqual(
            "amount must be a value greater than or equal to zero.",
            str(context.exception)
        )

    def test_withdraw_amount_zero(self):
        """Verify withdrawing zero leaves the balance unchanged."""
        self.account.withdraw(Decimal("0.00"))

        self.assertEqual(
            Decimal("1000.00"),
            self.account._BankAccount__balance
        )

    def test_withdraw_amount_greater_than_balance(self):
        """Verify an excessive withdrawal raises the expected error."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(Decimal("1100.00"))

        self.assertEqual(
            "amount cannot exceed the account balance.",
            str(context.exception)
        )

    def test_withdraw_decrease_balance_by_amount(self):
        """Verify a withdrawal decreases the balance by its amount."""
        self.account.withdraw(Decimal("100.00"))

        self.assertEqual(
            Decimal("900.00"),
            self.account._BankAccount__balance
        )

    # String representation test

    def test_str_returns_string_representation(self):
        """Verify the account number and currency formatting."""
        account = BankAccount(
            20019,
            Decimal("6764.67"),
            self.owner,
            AccountStatus.ACTIVE
        )

        self.assertEqual(
            "Account Number: 20019 Balance: $6,764.67",
            str(account)
        )