"""Observer interface and concrete observer implementations.

This module defines the Observer pattern components for a newsletter subscription system.
Observers (subscribers) are notified automatically when the Subject (newsletter) changes state.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .subject import Subject


class Observer(ABC):
    """Observer interface defining the update contract.

    All observers must implement the update() method to receive notifications
    from the Subject when its state changes.

    In the newsletter context, observers are subscribers (clients, employees,
    partners, suppliers) who receive email notifications.
    """

    @abstractmethod
    def update(self, message: str) -> None:
        """Receive notification from Subject about state change.

        Args:
            message: Notification message from the Subject
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get observer's name.

        Returns:
            Observer's name
        """
        pass

    @abstractmethod
    def get_email(self) -> str:
        """Get observer's email address.

        Returns:
            Observer's email
        """
        pass


class BaseSubscriber(Observer):
    """Base class for newsletter subscribers (ConcreteObserver).

    This base class provides common functionality for all subscriber types,
    reducing code duplication. Specific subscriber types (Client, Employee, etc.)
    inherit from this class.

    Attributes:
        name: Subscriber's name
        email: Subscriber's email address
        subject: The Subject (Newsletter) being observed
    """

    def __init__(self, name: str, email: str, subject: "Subject"):
        """Initialize subscriber and register with the subject.

        Args:
            name: Subscriber's name
            email: Subscriber's email address
            subject: Subject (Newsletter) to subscribe to
        """
        if not name or not email:
            raise ValueError("Name and email cannot be empty")

        self._name = name
        self._email = email
        self._subject = subject
        # Auto-register with the subject
        self._subject.register_observer(self)

    def update(self, message: str) -> None:
        """Process notification by simulating email send.

        Args:
            message: Message received from Subject
        """
        # In a real system, this would send an actual email
        print(f"[EMAIL] Email sent to {self._name} <{self._email}>")
        print(f"   Message: {message}")

    def get_name(self) -> str:
        """Get subscriber's name.

        Returns:
            Subscriber's name
        """
        return self._name

    def get_email(self) -> str:
        """Get subscriber's email.

        Returns:
            Subscriber's email address
        """
        return self._email

    def unsubscribe(self) -> None:
        """Remove this subscriber from the subject's observer list."""
        self._subject.remove_observer(self)

    def __repr__(self) -> str:
        """String representation of the subscriber.

        Returns:
            String with subscriber details
        """
        return f"{self.__class__.__name__}(name='{self._name}', email='{self._email}')"


class ClientSubscriber(BaseSubscriber):
    """Client subscriber (ConcreteObserver).

    Represents a company client who subscribes to the newsletter.
    Clients receive notifications about company news, promotions, etc.
    """
    pass


class EmployeeSubscriber(BaseSubscriber):
    """Employee subscriber (ConcreteObserver).

    Represents a company employee who subscribes to the newsletter.
    Employees receive internal communications and company updates.
    """
    pass


class PartnerSubscriber(BaseSubscriber):
    """Partner subscriber (ConcreteObserver).

    Represents a business partner who subscribes to the newsletter.
    Partners receive partnership-related news and updates.
    """
    pass


class SupplierSubscriber(BaseSubscriber):
    """Supplier subscriber (ConcreteObserver).

    Represents a company supplier who subscribes to the newsletter.
    Suppliers receive supply chain related communications.
    """
    pass
