"""Define the possible transaction statuses.

Author: Jashandeep Kaur
"""

from enum import Enum


class TransactionStatus(Enum):
    """Represent the stages of a bank transaction.

    Attributes:
        PENDING: The transaction has not been processed.
        PROCESSED: The transaction completed successfully.
        FAILED: The transaction failed validation.
    """

    PENDING = 1
    PROCESSED = 2
    FAILED = 3