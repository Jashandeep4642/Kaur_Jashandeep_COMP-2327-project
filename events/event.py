"""Provide an event that notifies registered listeners."""

from events.event_listener import EventListener


class Event:
    """Manage listeners and notify them when an event occurs."""

    def __init__(self):
        """Initialize an event with no listeners."""
        self.__listeners = []

    def add_listener(self, listener: EventListener) -> None:
        """Add a listener to this event."""
        self.__listeners.append(listener)

    def remove_listener(self, listener: EventListener) -> None:
        """Remove a listener if it is registered."""
        if listener in self.__listeners:
            self.__listeners.remove(listener)

    def notify(self, sender: object) -> None:
        """Notify each listener, passing the event sender."""
        for listener in self.__listeners:
            listener.update(sender)