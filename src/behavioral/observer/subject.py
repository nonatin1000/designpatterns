"""Subject interface and Newsletter implementation.

This module defines the Subject pattern component - the observable object
that maintains a list of observers and notifies them of state changes.
"""

from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .observer import Observer


class Subject(ABC):
    """Subject interface for observable objects.

    A Subject must be capable of:
    - Adding observers to its notification list
    - Removing observers from its notification list
    - Notifying all registered observers about state changes
    """

    @abstractmethod
    def register_observer(self, observer: "Observer") -> None:
        """Register an observer to receive notifications.

        Args:
            observer: The observer to register
        """
        pass

    @abstractmethod
    def remove_observer(self, observer: "Observer") -> None:
        """Remove an observer from the notification list.

        Args:
            observer: The observer to remove
        """
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        """Notify all registered observers about a state change."""
        pass


class Newsletter(Subject):
    """Newsletter (ConcreteSubject) that notifies observers about new messages.

    Implements the Subject interface, maintaining a list of observers
    and automatically notifying them when a new message is published.

    This demonstrates the Observer pattern's one-to-many dependency:
    when Newsletter's state changes (new message), all subscribers
    are notified automatically.

    Attributes:
        _observers: List of registered observers
        _messages: List of published messages
    """

    def __init__(self):
        """Initialize newsletter with empty lists of observers and messages."""
        self._observers: List["Observer"] = []
        self._messages: List[str] = []

    def register_observer(self, observer: "Observer") -> None:
        """Add an observer to the notification list.

        Args:
            observer: The observer to register

        Note:
            Duplicate registrations are prevented - each observer
            can only be registered once.
        """
        if observer not in self._observers:
            self._observers.append(observer)
        else:
            print(f"[WARNING] {observer.get_name()} is already subscribed")

    def remove_observer(self, observer: "Observer") -> None:
        """Remove an observer from the notification list.

        Args:
            observer: The observer to remove
        """
        if observer in self._observers:
            self._observers.remove(observer)
        else:
            print(f"[WARNING] {observer.get_name()} is not subscribed")

    def notify_observers(self) -> None:
        """Notify all observers about the latest newsletter message.

        This method is called automatically when a new message is published.
        Each observer's update() method is invoked with the latest message.
        """
        if not self._messages:
            return

        last_message = self._messages[-1]

        for observer in self._observers:
            observer.update(last_message)

    def publish_message(self, message: str) -> None:
        """Publish a new message and notify all observers.

        This is the key method that triggers the Observer pattern:
        1. Message is added to the newsletter
        2. All observers are automatically notified
        3. Each observer processes the notification (sends email)

        Args:
            message: Content of the message to publish
        """
        if not message:
            raise ValueError("Message cannot be empty")

        self._messages.append(message)
        self.notify_observers()

    def get_messages(self) -> List[str]:
        """Get all published messages.

        Returns:
            Copy of all published messages
        """
        return self._messages.copy()

    def get_subscriber_count(self) -> int:
        """Get total number of subscribers.

        Returns:
            Number of registered observers
        """
        return len(self._observers)

    def get_subscribers(self) -> List[dict]:
        """Get information about all subscribers.

        Returns:
            List of dicts with name and email of each subscriber
        """
        return [
            {
                "name": obs.get_name(),
                "email": obs.get_email()
            }
            for obs in self._observers
        ]

    def __repr__(self) -> str:
        """String representation of the newsletter.

        Returns:
            String with newsletter stats
        """
        return (
            f"Newsletter("
            f"subscribers={len(self._observers)}, "
            f"messages={len(self._messages)})"
        )
