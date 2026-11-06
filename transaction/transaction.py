"""Provide the abstract base class for bank transactions.

Author: Jashandeep Kaur
"""

from abc import ABC, abstractmethod
from decimal import Decimal

from account.bank_account import BankAccount
from transaction.transaction_status import TransactionStatus
from fee.fee_strategy import FeeStrategy
from events.event import Event



class Transaction(ABC):
    """Define the shared attributes and interface of a transaction."""

    def __init__(
        self,
        transaction_id: str,
        amount: Decimal,
        account: BankAccount
    ):
        """Initialize a pending transaction.

        Args:
            transaction_id (str): The transaction identifier.
            amount (Decimal): The positive transaction amount.
            account (BankAccount): The source bank account.

        Raises:
            ValueError: If transaction_id is blank or amount is
                less than or equal to zero.
        """
        if transaction_id.strip() == "":
            raise ValueError("transaction_id cannot be blank.")

        if amount <= 0:
            raise ValueError("amount must be greater than zero.")

        self.__transaction_id = transaction_id
        self.__amount = amount
        self.__status = TransactionStatus.PENDING
        self.__account = account
        self.__fee_strategy = None
        self.__processed_event = Event()

    @property
    def transaction_id(self) -> str:
        """Return the transaction identifier."""
        return self.__transaction_id
      

    @property
    def amount(self) -> Decimal:
        """Return the transaction amount."""
        return self.__amount

    @property
    def status(self) -> TransactionStatus:
        """Return the current transaction status."""
        return self.__status

    @status.setter
    def status(self, value: TransactionStatus) -> None:
        """Set the transaction status.

        Args:
            value (TransactionStatus): The new transaction status.
        """
        self.__status = value

    @property
    def account(self) -> BankAccount:
        """Return the source bank account."""
        return self.__account

    @property
    def on_processed(self) -> Event:
        """Return the event raised when this transaction is processed."""
        return self.__processed_event

    def set_fee_strategy(self, fee_strategy: FeeStrategy) -> None:
        """Set the strategy used to calculate transaction fees."""
        self.__fee_strategy = fee_strategy

    @property
    def fees(self) -> Decimal:
        """Return the strategy fee, or zero when no strategy is set."""
        if self.__fee_strategy is None:
            return Decimal("0.00")

        return self.__fee_strategy.get_fee(self.amount)

    @abstractmethod
    def process(self) -> None:
        """Process the transaction using the subclass implementation."""
        pass

    def __str__(self) -> str:
        """Return the transaction details in the required format."""
        return (
            f"ID: {self.__transaction_id}\n"
            f"STATUS: {self.__status.name}\n"
            f"AMOUNT: ${self.__amount:,.2f}\n"
            f"SOURCE ACCT: {self.__account.account_id}"
        )