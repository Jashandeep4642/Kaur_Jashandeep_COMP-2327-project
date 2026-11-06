"""Provide a listener that logs processed transactions."""

from events.event_listener import EventListener
from transaction.transaction import Transaction


class LoggingListener(EventListener):
    """Print transaction details when notified."""

    def update(self, sender: object) -> None:
        """Log a transaction or reject an invalid sender."""
        if not isinstance(sender, Transaction):
            raise TypeError("sender must be a Transaction type.")

        print("TRANSACTION PROCESSED")
        print("=" * 60)
        print(sender)
        print("=" * 60)