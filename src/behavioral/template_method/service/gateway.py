import random


class Gateway:

    def charge(self, amount: float) -> bool:
        return random.choice([True, False]), amount
