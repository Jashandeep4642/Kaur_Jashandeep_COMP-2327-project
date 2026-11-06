"""Provide a credit card transaction with an authorization code.

Author: Jashandeep Kaur
"""

from decimal import Decimal

from account.account_status import AccountStatus
from account.bank_account import BankAccount
from transaction.transaction import Transaction
from transaction.transaction_status import TransactionStatus


class CreditCardTransaction(Transaction):
    """Process a credit card payment from a bank account."""

    def __init__(
        self,
        transaction_id: str,
        amount: Decimal,
        account: BankAccount,
        authorization_code: str
    ):
        """Initialize a pending credit card transaction.

        Args:
            transaction_id (str): The transaction identifier.
            amount (Decimal): The positive payment amount.
            account (BankAccount): The source account.
            authorization_code (str): The code issued by the vendor.

        Raises:
            ValueError: If transaction_id is blank or amount is
                less than or equal to zero.
        """
        super().__init__(transaction_id, amount, account)
        self.__authorization_code = authorization_code



    def process(self) -> None:
        """Validate and process the credit card payment.

        The source account must be active, its balance must cover
        the amount plus fees, and the authorization code must not
        be blank. Validation failure sets the status to FAILED
        without withdrawing funds. A valid pending transaction
        withdraws the amount and fees and becomes PROCESSED.
        """
        if (
            self.account.status != AccountStatus.ACTIVE
            or self.amount + self.fees > self.account.balance
            or self.__authorization_code.strip() == ""
        ):
            self.status = TransactionStatus.FAILED
            return

        if self.status == TransactionStatus.PENDING:
            self.account.withdraw(self.amount)
            self.account.withdraw(self.fees)
            self.status = TransactionStatus.PROCESSED
            self.on_processed.notify(self)

    def __str__(self) -> str:
        """Return transaction details followed by the authorization code."""
        return (
            f"{super().__str__()}\n"
            f"AUTH CODE: {self.__authorization_code}"
        )