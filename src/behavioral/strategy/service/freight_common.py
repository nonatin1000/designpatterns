from behavioral.strategy.interface.freight_interface import FreightInterface


class FreightCommon(FreightInterface):

    def calculate(self, amount: float) -> float:
        return amount * 0.05
