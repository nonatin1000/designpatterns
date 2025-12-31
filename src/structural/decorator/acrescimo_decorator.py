from abc import abstractmethod
from pizza import Pizza


class AcrescimoDecorator(Pizza):
    """
    Decorator: Classe abstrata para todos os decorators.
    Mantém uma referência a um objeto Component e define uma interface
    que está em conformidade com a interface do Component.
    """

    def __init__(self, pizza: Pizza):
        super().__init__()
        self.pizza = pizza

    @abstractmethod
    def get_descricao(self) -> str:
        """
        Cada decorator deve implementar sua própria descrição
        para concatenar com a descrição da pizza decorada.
        """
        pass

    @abstractmethod
    def get_preco(self) -> float:
        """
        Cada decorator deve implementar seu próprio preço
        para somar ao preço da pizza decorada.
        """
        pass
