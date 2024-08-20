from abc import ABC, abstractmethod


class FreightInterface(ABC):

    @abstractmethod
    def calculate(self, amount: float) -> float:
        pass
