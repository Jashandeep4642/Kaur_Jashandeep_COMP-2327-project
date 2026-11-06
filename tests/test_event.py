"""Test event subscriptions and notifications."""

import unittest
from unittest.mock import Mock

from events.event import Event
from events.event_listener import EventListener


class TestEvent(unittest.TestCase):
    """Verify listeners receive the correct event notifications."""

    def setUp(self):
        """Create an event, listener, and sender for each test."""
        self.event = Event()
        self.listener = Mock(spec=EventListener)
        self.sender = object()

    def test_notify_without_listeners(self):
        """Verify an event with no listeners completes normally."""
        self.event.notify(self.sender)

    def test_add_listener_receives_notification(self):
        """Verify a subscribed listener receives the sender."""
        self.event.add_listener(self.listener)

        self.event.notify(self.sender)

        self.listener.update.assert_called_once_with(self.sender)

    def test_notify_multiple_listeners(self):
        """Verify all subscribed listeners receive the sender."""
        second_listener = Mock(spec=EventListener)
        self.event.add_listener(self.listener)
        self.event.add_listener(second_listener)

        self.event.notify(self.sender)

        self.listener.update.assert_called_once_with(self.sender)
        second_listener.update.assert_called_once_with(self.sender)

    def test_removed_listener_is_not_notified(self):
        """Verify removing a listener stops its notifications."""
        self.event.add_listener(self.listener)
        self.event.remove_listener(self.listener)

        self.event.notify(self.sender)

        self.listener.update.assert_not_called()

    def test_remove_unregistered_listener(self):
        """Verify removing an unregistered listener raises no error."""
        self.event.remove_listener(self.listener)

        self.event.notify(self.sender)

        self.listener.update.assert_not_called()

    def test_removing_one_listener_keeps_other_listener(self):
        """Verify remaining listeners still receive notifications."""
        second_listener = Mock(spec=EventListener)
        self.event.add_listener(self.listener)
        self.event.add_listener(second_listener)
        self.event.remove_listener(self.listener)

        self.event.notify(self.sender)

        self.listener.update.assert_not_called()
        second_listener.update.assert_called_once_with(self.sender)


class TestEventListener(unittest.TestCase):
    """Verify the event listener interface is abstract."""

    def test_cannot_instantiate_abstract_listener(self):
        """Verify listeners must implement the update method."""
        with self.assertRaises(TypeError):
            EventListener()