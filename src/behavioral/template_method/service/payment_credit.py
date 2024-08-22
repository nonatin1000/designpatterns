from behavioral.template_method.interface.payment_interface import PaymentInterface


class PaymentCredit(PaymentInterface):

    def calculate_tax(self) -> float:
        return self.amount * 0.05

    def calculate_discount(self) -> float:
        if self.amount > 300:
            return self.amount * 0.02
        return 0.0
