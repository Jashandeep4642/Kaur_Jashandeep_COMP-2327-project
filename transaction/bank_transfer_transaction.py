"""Provide a transaction that transfers funds between bank accounts.

Author: Jashandeep Kaur
"""

from decimal import Decimal

from account.account_status import AccountStatus
from account.bank_account import BankAccount
from transaction.transaction import Transaction
from transaction.transaction_status import TransactionStatus


class BankTransferTransaction(Transaction):
    """Transfer an amount from a source account to a target account."""

    def __init__(
        self,
        transaction_id: str,
        amount: Decimal,
        account: BankAccount,
        target_account: BankAccount
    ):
        """Initialize a pending bank transfer.

        Args:
            transaction_id (str): The transaction identifier.
            amount (Decimal): The positive amount to transfer.
            account (BankAccount): The source account.
            target_account (BankAccount): The receiving account.

        Raises:
            ValueError: If transaction_id is blank or amount is
                less than or equal to zero.
        """
        super().__init__(transaction_id, amount, account)
        self.__target_account = target_account

    @property
    def fees(self) -> Decimal:
        """Return the larger of $1.00 or 0.7% of the amount."""
        return max(Decimal("1.00"), self.amount * Decimal("0.007"))

    def process(self) -> None:
        """Validate and process the bank transfer.

        Both accounts must be active, and the source balance must
        cover the amount plus fees. Validation failure sets the
        status to FAILED without moving funds. A valid pending
        transfer debits the source, credits the target, and sets
        the status to PROCESSED.
        """
        if (
            self.account.status != AccountStatus.ACTIVE
            or self.__target_account.status != AccountStatus.ACTIVE
            or self.amount + self.fees > self.account.balance
        ):
            self.status = TransactionStatus.FAILED
            return

        if self.status == TransactionStatus.PENDING:
            self.account.withdraw(self.amount)
            self.account.withdraw(self.fees)
            self.__target_account.deposit(self.amount)
            self.status = TransactionStatus.PROCESSED

    def __str__(self) -> str:
        """Return transaction details with the target account ID."""
        return (
            f"{super().__str__()} --> "
            f"TARGET ACCT: {self.__target_account.account_id}"
        )