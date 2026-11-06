"""Provide a percentage-based transaction fee strategy."""

from decimal import Decimal
from fee.fee_strategy import FeeStrategy


class PercentageFeeStrategy(FeeStrategy):
    """Calculate a fee as a percentage of the transaction amount."""

    def __init__(self, percentage: Decimal):
        """Initialize the strategy with a percentage between zero and one."""
        if not 0 <= percentage <= 1:
            raise ValueError(
                "percentage must be a value between 0 and 1 (inclusive)."
            )

        self.__percentage = Decimal(str(percentage))

    def get_fee(self, transaction_amount: Decimal) -> Decimal:
        """Return the percentage fee rounded to two decimal places."""
        return round(transaction_amount * self.__percentage, 2)