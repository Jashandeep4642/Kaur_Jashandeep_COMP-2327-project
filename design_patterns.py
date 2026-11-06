"""Demonstrate the Strategy and Observer design patterns."""

from decimal import Decimal

from account.client import Client
from account.bank_account import BankAccount
from account.account_status import AccountStatus
from transaction.credit_card_transaction import CreditCardTransaction
from fee.base_percentage_fee_strategy import BasePercentageFeeStrategy
from fee.percentage_fee_strategy import PercentageFeeStrategy
from events.logging_listener import LoggingListener

__author__ = "Jashandeep Kaur"
__version__ = "1.0"


def main() -> None:
    """Demonstrate changing fee strategies and notifying a listener."""

    # 1. Create a transaction instance.
    client = Client(1, "Jashandeep Kaur", "jashan@yahoo.com")
    account = BankAccount(
        1001, Decimal("1000.00"), client, AccountStatus.ACTIVE
    )
    transaction = CreditCardTransaction(
        "TXN001", Decimal("100.00"), account, "AUTH001"
    )

    # 2. Print the transaction fee.
    print(transaction.fees)

    # 3. Create a new instance of a fee strategy. The transaction fee
    # is determined by base or percentage, depending which is higher.
    # The base fee is $1.25 and the percentage of the transaction
    # amount is 0.7%.
    strategy = BasePercentageFeeStrategy(
        Decimal("1.25"), Decimal("0.007")
    )

    # 4. Update the transaction instance such that it will use the fee
    # strategy to calculate the fees.
    transaction.set_fee_strategy(strategy)

    # 5. Print the transaction fees. Formatting is not required.
    print(transaction.fees)

    # 6. Update the transaction instance such that the fee strategy will
    # determine the fee based only on percentage of the transaction
    # amount. The fee is .35% of the transaction amount.
    transaction.set_fee_strategy(
        PercentageFeeStrategy(Decimal("0.0035"))
    )

    # 7. Print the transaction fees. Formatting is not required.
    print(transaction.fees)

    # 8. Create a logging listener instance.
    listener = LoggingListener()

    # 9. Using the listener, subscribe to the event.
    transaction.on_processed.add_listener(listener)

    # 10. Invoke the method to raise the event.
    transaction.process()


if __name__ == "__main__":
    main()