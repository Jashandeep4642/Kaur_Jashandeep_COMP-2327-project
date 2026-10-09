"""Define the possible bank account statuses.

Author: Jashandeep Kaur
"""

from enum import Enum


class AccountStatus(Enum):
    """Represent the states of a bank account.

    Attributes:
        INACTIVE: The account is inactive.
        ACTIVE: The account is active.
        SUSPENDED: The account is suspended.
        CLOSED: The account is closed.
    """

    INACTIVE = 0
    ACTIVE = 1
    SUSPENDED = 2
    CLOSED = 3