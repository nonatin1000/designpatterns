from behavioral.template_method.interface.payment_interface import PaymentInterface


class PaymentCash(PaymentInterface):

    def calculate_discount(self) -> float:
        return self.amount * 0.1
