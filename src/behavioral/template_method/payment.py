"""Payment classes implementing the Template Method pattern.

This module defines the Payment abstract class (Template) and concrete payment types
for different payment methods (Credit, Debit, Cash).

The Template Method pattern defines the skeleton of an algorithm (process_payment),
deferring some steps to subclasses (calculate_tax, calculate_discount).
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gateway import Gateway


class Payment(ABC):
    """Abstract base class for payments (Template in Template Method pattern).

    This class defines the template method process_payment() that orchestrates
    the payment processing algorithm. Subclasses must implement the varying
    steps (calculate_discount) and can optionally override hooks (calculate_tax).

    The template method ensures all payments follow the same processing flow:
    1. Calculate tax
    2. Calculate discount
    3. Compute final amount (amount + tax - discount)
    4. Process charge through gateway

    Attributes:
        amount: Payment value in Brazilian Reais (BRL)
        gateway: Payment gateway for processing charges
    """

    def __init__(self, amount: float, gateway: "Gateway") -> None:
        """Initialize a new payment.

        Args:
            amount: Payment value in BRL
            gateway: Gateway instance for processing payments

        Raises:
            ValueError: If amount is negative
        """
        if amount < 0:
            raise ValueError("Payment amount cannot be negative")
        self._amount = amount
        self._gateway = gateway

    @property
    def amount(self) -> float:
        """Get the payment amount.

        Returns:
            Payment value in BRL
        """
        return self._amount

    @amount.setter
    def amount(self, value: float) -> None:
        """Set the payment amount.

        Args:
            value: Payment value in BRL

        Raises:
            ValueError: If amount is negative
        """
        if value < 0:
            raise ValueError("Payment amount cannot be negative")
        self._amount = value

    def calculate_tax(self) -> float:
        """Calculate gateway processing tax (Hook method).

        This is a hook method with a default implementation that can be
        overridden by subclasses. The default implementation returns 0
        (no tax), which is appropriate for cash payments.

        Returns:
            Tax amount in BRL (default: 0)
        """
        return 0.0

    @abstractmethod
    def calculate_discount(self) -> float:
        """Calculate discount amount (Abstract method).

        This is an abstract primitive operation that must be implemented
        by all concrete subclasses according to their specific rules.

        Returns:
            Discount amount in BRL
        """
        pass

    def process_payment(self) -> tuple[bool, float]:
        """Process the payment through gateway (Template Method).

        This is the template method that defines the payment processing algorithm.
        It is marked as final (by convention) to prevent subclasses from changing
        the algorithm structure.

        The algorithm follows these steps:
        1. Calculate tax using calculate_tax()
        2. Calculate discount using calculate_discount()
        3. Compute final amount: amount + tax - discount
        4. Process charge through gateway

        Returns:
            Tuple of (success: bool, final_amount: float)
        """
        tax = self.calculate_tax()
        discount = self.calculate_discount()
        final_amount = self._amount + tax - discount
        success = self._gateway.charge(final_amount)
        return success, final_amount

    def __repr__(self) -> str:
        """String representation of the payment.

        Returns:
            String with payment details
        """
        return (
            f"{self.__class__.__name__}("
            f"amount=R$ {self._amount:.2f}, "
            f"gateway={self._gateway.__class__.__name__})"
        )


class CreditPayment(Payment):
    """Payment using credit card.

    Credit card payments have:
    - Tax: 5% of payment amount (gateway fee)
    - Discount: 2% only for amounts greater than R$ 300

    Examples:
        Amount R$ 1000: tax=R$ 50, discount=R$ 20, final=R$ 1030
        Amount R$ 200: tax=R$ 10, discount=R$ 0, final=R$ 210
    """

    # Constants for credit payment rules
    TAX_RATE = 0.05  # 5% gateway fee
    DISCOUNT_RATE = 0.02  # 2% discount
    DISCOUNT_THRESHOLD = 300.0  # Minimum amount for discount

    def calculate_tax(self) -> float:
        """Calculate credit card gateway tax.

        Returns:
            5% of payment amount
        """
        return self.amount * self.TAX_RATE

    def calculate_discount(self) -> float:
        """Calculate credit card discount.

        Credit cards offer 2% discount only for purchases over R$ 300.

        Returns:
            2% of amount if > R$ 300, otherwise 0
        """
        if self.amount > self.DISCOUNT_THRESHOLD:
            return self.amount * self.DISCOUNT_RATE
        return 0.0


class DebitPayment(Payment):
    """Payment using debit card.

    Debit card payments have:
    - Tax: Fixed R$ 4.00 fee (gateway fee)
    - Discount: 5% of payment amount

    Examples:
        Amount R$ 1000: tax=R$ 4, discount=R$ 50, final=R$ 954
        Amount R$ 100: tax=R$ 4, discount=R$ 5, final=R$ 99
    """

    # Constants for debit payment rules
    TAX_AMOUNT = 4.0  # Fixed R$ 4 gateway fee
    DISCOUNT_RATE = 0.05  # 5% discount

    def calculate_tax(self) -> float:
        """Calculate debit card gateway tax.

        Returns:
            Fixed amount of R$ 4.00
        """
        return self.TAX_AMOUNT

    def calculate_discount(self) -> float:
        """Calculate debit card discount.

        Returns:
            5% of payment amount
        """
        return self.amount * self.DISCOUNT_RATE


class CashPayment(Payment):
    """Payment using cash.

    Cash payments have:
    - Tax: R$ 0 (no gateway fee)
    - Discount: 10% of payment amount (best discount!)

    Examples:
        Amount R$ 1000: tax=R$ 0, discount=R$ 100, final=R$ 900
        Amount R$ 50: tax=R$ 0, discount=R$ 5, final=R$ 45
    """

    # Constants for cash payment rules
    DISCOUNT_RATE = 0.10  # 10% discount (best option)

    def calculate_discount(self) -> float:
        """Calculate cash payment discount.

        Cash payments offer the best discount: 10% of amount.

        Returns:
            10% of payment amount
        """
        return self.amount * self.DISCOUNT_RATE
