"""Define the common interface for transaction fee strategies."""

from abc import ABC, abstractmethod
from decimal import Decimal


class FeeStrategy(ABC):
    """Represent a strategy for calculating transaction fees."""

    @abstractmethod
    def get_fee(self, transaction_amount: Decimal) -> Decimal:
        """Return the fee charged for the given transaction amount."""
        pass