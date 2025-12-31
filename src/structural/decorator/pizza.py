from abc import ABC, abstractmethod


class Pizza(ABC):
    """
    Component: Interface/classe abstrata base para todas as pizzas.
    Define a interface comum para objetos que podem ter responsabilidades
    adicionadas dinamicamente.
    """

    def __init__(self):
        self.descricao: str = "Descrição não definida"
        self.preco: float = 0.0

    @abstractmethod
    def get_descricao(self) -> str:
        """Retorna a descrição da pizza"""
        pass

    @abstractmethod
    def get_preco(self) -> float:
        """Retorna o preço da pizza"""
        pass
