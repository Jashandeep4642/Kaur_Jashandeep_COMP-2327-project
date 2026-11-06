"""Provide a percentage fee strategy with a minimum base fee."""

from decimal import Decimal
from fee.fee_strategy import FeeStrategy


class BasePercentageFeeStrategy(FeeStrategy):
    """Charge the greater of the base fee or percentage fee."""

    def __init__(self, base_fee: Decimal, percentage: Decimal):
        """Initialize the base fee and percentage."""
        if base_fee < 0:
            raise ValueError(
                "base_fee must be greater than or equal to zero."
            )

        if not 0 <= percentage <= 1:
            raise ValueError(
                "percentage must be a value between 0 and 1 (inclusive)."
            )

        self.__base_fee = Decimal(str(base_fee))
        self.__percentage = Decimal(str(percentage))

    def get_fee(self, transaction_amount: Decimal) -> Decimal:
        """Return the greater fee rounded to two decimal places."""
        percentage_fee = transaction_amount * self.__percentage
        return round(max(self.__base_fee, percentage_fee), 2)