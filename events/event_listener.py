"""Define the common interface for event listeners."""

from abc import ABC, abstractmethod


class EventListener(ABC):
    """Represent an object that responds to an event."""

    @abstractmethod
    def update(self, sender: object) -> None:
        """Respond to an event raised by the sender."""
        pass