from acrescimo_decorator import AcrescimoDecorator
from pizza import Pizza


class BordaRequeijao(AcrescimoDecorator):
    """
    ConcreteDecorator: Adiciona responsabilidades ao componente.
    Implementa o decorator de borda recheada de requeijão.
    """

    def __init__(self, pizza: Pizza):
        super().__init__(pizza)

    def get_descricao(self) -> str:
        """
        Retorna a descrição da pizza decorada concatenada
        com a descrição deste acréscimo.
        """
        return f"{self.pizza.get_descricao()} + Borda recheada de requeijão"

    def get_preco(self) -> float:
        """
        Retorna o preço da pizza decorada somado
        ao preço deste acréscimo.
        """
        return self.pizza.get_preco() + 8.50


class MassaIntegral(AcrescimoDecorator):
    """
    ConcreteDecorator: Implementa o decorator de massa integral.
    """

    def __init__(self, pizza: Pizza):
        super().__init__(pizza)

    def get_descricao(self) -> str:
        """
        Retorna a descrição da pizza decorada concatenada
        com a descrição deste acréscimo.
        """
        return f"{self.pizza.get_descricao()} + Massa integral"

    def get_preco(self) -> float:
        """
        Retorna o preço da pizza decorada somado
        ao preço deste acréscimo.
        """
        return self.pizza.get_preco() + 5.00
