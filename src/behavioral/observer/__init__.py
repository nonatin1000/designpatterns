"""
Padrão Observer - Sistema de Newsletter

O Observer é um padrão comportamental que define uma dependência um-para-muitos
entre objetos, de modo que quando um objeto muda seu estado, todos seus
dependentes são notificados e atualizados automaticamente.
"""

from .observer_interface import Observer
from .subject_interface import Subject
from .newsletter import Newsletter
from .observers import Cliente, Funcionario, Parceiro, Fornecedor
from .email_service import EmailService

__all__ = [
    "Observer",
    "Subject",
    "Newsletter",
    "Cliente",
    "Funcionario",
    "Parceiro",
    "Fornecedor",
    "EmailService",
]
