from pizza import Pizza


class PizzaFrango(Pizza):
    """
    ConcreteComponent: Implementação concreta de uma pizza.
    Define um objeto ao qual responsabilidades adicionais podem ser atribuídas.
    """

    def __init__(self):
        super().__init__()
        self.descricao = "Deliciosa pizza de frango"
        self.preco = 19.00

    def get_descricao(self) -> str:
        return self.descricao

    def get_preco(self) -> float:
        return self.preco


class PizzaCalabresa(Pizza):
    """ConcreteComponent: Pizza de calabresa"""

    def __init__(self):
        super().__init__()
        self.descricao = "Deliciosa pizza de calabresa"
        self.preco = 25.00

    def get_descricao(self) -> str:
        return self.descricao

    def get_preco(self) -> float:
        return self.preco


class PizzaQueijo(Pizza):
    """ConcreteComponent: Pizza de queijo"""

    def __init__(self):
        super().__init__()
        self.descricao = "Deliciosa pizza de queijo"
        self.preco = 22.00

    def get_descricao(self) -> str:
        return self.descricao

    def get_preco(self) -> float:
        return self.preco
