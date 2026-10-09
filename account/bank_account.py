"""Provide the BankAccount class for managing a bank account.

Author: Jashandeep Kaur
"""

from decimal import Decimal

from account.client import Client
from account.account_status import AccountStatus


class BankAccount:
    """Represent a bank account with an owner, balance, and status."""

    def __init__(
        self,
        account_id: int,
        balance: Decimal,
        owner: Client,
        status: AccountStatus
    ):
        """Initialize a bank account.

        Args:
            account_id (int): The account's positive identifier.
            balance (Decimal): The initial account balance.
            owner (Client): The client who owns the account.
            status (AccountStatus): The initial account status.

        Raises:
            ValueError: If account_id is less than or equal to zero.
        """
        if account_id <= 0:
            raise ValueError(
                "account_id must be a value greater than zero."
            )

        self.__account_id = account_id
        self.__balance = balance
        self.__owner = owner
        self.__status = status

    @property
    def account_id(self) -> int:
        """Return the account identifier as an int."""
        return self.__account_id

    @property
    def balance(self) -> Decimal:
        """Return the current account balance as a Decimal."""
        return self.__balance

    @property
    def owner(self) -> Client:
        """Return the Client who owns the account."""
        return self.__owner

    @property
    def status(self) -> AccountStatus:
        """Return the current AccountStatus."""
        return self.__status

    @status.setter
    def status(self, value: AccountStatus) -> None:
        """Set the account status.

        Args:
            value (AccountStatus): The new account status.
        """
        self.__status = value

    def __update_balance(self, amount: Decimal) -> None:
        """Adjust the balance by a signed amount.

        Args:
            amount (Decimal): A positive amount to add or a negative
                amount to subtract.
        """
        self.__balance += amount

    def deposit(self, amount: Decimal) -> None:
        """Deposit a nonnegative amount into the account.

        Args:
            amount (Decimal): The amount to deposit.

        Raises:
            ValueError: If amount is negative.
        """
        if amount < 0:
            raise ValueError(
                "amount must be a value greater than or equal to zero."
            )

        self.__update_balance(amount)

    def withdraw(self, amount: Decimal) -> None:
        """Withdraw a nonnegative amount within the available balance.

        Args:
            amount (Decimal): The amount to withdraw.

        Raises:
            ValueError: If amount is negative or exceeds the balance.
        """
        if amount < 0:
            raise ValueError(
                "amount must be a value greater than or equal to zero."
            )

        if amount > self.__balance:
            raise ValueError(
                "amount cannot exceed the account balance."
            )

        self.__update_balance(-amount)

    def __str__(self) -> str:
        """Return the account number and balance formatted as currency."""
        return (
            f"Account Number: {self.__account_id} "
            f"Balance: ${self.__balance:,.2f}"
        )