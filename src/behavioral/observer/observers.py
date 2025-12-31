from observer_interface import Observer
from subject_interface import Subject
from email_service import EmailService


class Cliente(Observer):
    """
    ConcreteObserver: Cliente que se inscreve na newsletter.

    Implementa a interface Observer para receber notificações
    quando uma nova mensagem é publicada na newsletter.
    """

    def __init__(self, nome: str, email: str, subject: Subject):
        """
        Inicializa o cliente e o registra no subject.

        Args:
            nome: Nome do cliente
            email: Email do cliente
            subject: Subject (Newsletter) ao qual o cliente irá se inscrever
        """
        self.nome = nome
        self.email = email
        self.subject = subject
        # Auto-registro no subject
        self.subject.register_observer(self)

    def update(self, mensagem: str) -> None:
        """
        Recebe a notificação do Subject e processa (envia email).

        Args:
            mensagem: Mensagem recebida do Subject
        """
        EmailService.enviar_email(self, mensagem)

    def get_nome(self) -> str:
        return self.nome

    def get_email(self) -> str:
        return self.email

    def cancelar_inscricao(self) -> None:
        """Remove este cliente da lista de observadores"""
        self.subject.remove_observer(self)


class Funcionario(Observer):
    """ConcreteObserver: Funcionário da empresa"""

    def __init__(self, nome: str, email: str, subject: Subject):
        self.nome = nome
        self.email = email
        self.subject = subject
        self.subject.register_observer(self)

    def update(self, mensagem: str) -> None:
        EmailService.enviar_email(self, mensagem)

    def get_nome(self) -> str:
        return self.nome

    def get_email(self) -> str:
        return self.email

    def cancelar_inscricao(self) -> None:
        self.subject.remove_observer(self)


class Parceiro(Observer):
    """ConcreteObserver: Parceiro de negócios"""

    def __init__(self, nome: str, email: str, subject: Subject):
        self.nome = nome
        self.email = email
        self.subject = subject
        self.subject.register_observer(self)

    def update(self, mensagem: str) -> None:
        EmailService.enviar_email(self, mensagem)

    def get_nome(self) -> str:
        return self.nome

    def get_email(self) -> str:
        return self.email

    def cancelar_inscricao(self) -> None:
        self.subject.remove_observer(self)


class Fornecedor(Observer):
    """ConcreteObserver: Fornecedor da empresa"""

    def __init__(self, nome: str, email: str, subject: Subject):
        self.nome = nome
        self.email = email
        self.subject = subject
        self.subject.register_observer(self)

    def update(self, mensagem: str) -> None:
        EmailService.enviar_email(self, mensagem)

    def get_nome(self) -> str:
        return self.nome

    def get_email(self) -> str:
        return self.email

    def cancelar_inscricao(self) -> None:
        self.subject.remove_observer(self)
