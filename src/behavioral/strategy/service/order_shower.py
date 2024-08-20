from behavioral.strategy.interface.order_interface import OrderInterface


class OrderShower(OrderInterface):
    def __init__(self) -> None:
        super().__init__()
        self._name = "Shower"

    def name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name
