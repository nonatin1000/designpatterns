from behavioral.template_method.interface.payment_interface import PaymentInterface


class PaymentDebit(PaymentInterface):

    def calculate_tax(self) -> float:
        return 4

    def calculate_discount(self) -> float:
        return self.amount * 0.05
