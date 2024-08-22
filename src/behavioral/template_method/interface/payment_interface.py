from abc import ABC, abstractmethod

from behavioral.template_method.service.gateway import Gateway


class PaymentInterface(ABC):

    def __init__(self, amount: float, gateway: Gateway) -> None:
        self._amount = amount
        self._gateway = gateway

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, amount: float) -> None:
        self._amount = amount

    def calculate_tax(self) -> float:
        return 0

    @abstractmethod
    def calculate_discount(self) -> float:
        pass

    def execute_charge(self) -> bool:
        total = self._amount + self.calculate_tax() - self.calculate_discount()
        return self._gateway.charge(total)
