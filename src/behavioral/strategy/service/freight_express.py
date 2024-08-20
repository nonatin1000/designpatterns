from behavioral.strategy.interface.freight_interface import FreightInterface


class FreightExpress(FreightInterface):

    def calculate(self, amount: float) -> float:
        return amount * 0.1
