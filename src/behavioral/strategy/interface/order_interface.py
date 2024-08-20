from abc import ABC, abstractmethod

from behavioral.strategy.interface.freight_interface import FreightInterface


class OrderInterface(ABC):
    def __init__(self) -> None:
        self._amount: float = 0.0
        self._type_frieght: FreightInterface = None

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, amount: float) -> None:
        self._amount = amount

    def set_type_freight(self, frieght: FreightInterface) -> None:
        self._type_frieght = frieght

    def calculate_freight(self) -> float:
        return self._type_frieght.calculate(self._amount)

    @abstractmethod
    def name(self) -> str:
        pass


# src
#     behavioral
#         strategy
#             interface
#                 freight_interface.py
#             service
#                 freight_common.py
#                 freight_express.py
#                 order_eletronic.py
#                 order_shower.py
#                 order_interface.py
#             __init__.py
#         __init__.py
# main.py
# docker-compose.yml
# Dockefile.yml
# requirements.txt