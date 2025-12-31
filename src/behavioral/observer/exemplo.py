"""
Exemplo de uso do Padrão Observer - Sistema de Newsletter
"""

from newsletter import Newsletter
from observers import Cliente, Funcionario, Parceiro, Fornecedor


def exemplo_basico():
    """Exemplo 1: Funcionamento básico do Observer"""
    print("\n" + "=" * 80)
    print("EXEMPLO 1: Funcionamento Básico do Observer")
    print("=" * 80)

    # Cria a Newsletter (Subject)
    newsletter = Newsletter()

    # Cria assinantes (Observers) que se auto-registram
    cliente1 = Cliente("João Silva", "joao@email.com", newsletter)
    funcionario1 = Funcionario("Maria Santos", "maria@empresa.com", newsletter)

    # Publica primeira mensagem - notifica todos
    newsletter.add_mensagem("Bem-vindos à nossa newsletter!")


def exemplo_dinamico():
    """Exemplo 2: Adição e remoção dinâmica de observers"""
    print("\n" + "=" * 80)
    print("EXEMPLO 2: Adicão e Remoção Dinâmica")
    print("=" * 80)

    newsletter = Newsletter()

    # Adiciona assinantes
    cliente = Cliente("Cliente 1", "cliente1@email.com", newsletter)
    parceiro = Parceiro("Parceiro 1", "parceiro1@email.com", newsletter)
    fornecedor = Fornecedor("Fornecedor 1", "fornecedor1@email.com", newsletter)

    # Primeira mensagem - todos recebem
    newsletter.add_mensagem("Primeira mensagem")

    print("\n" + "#" * 80 + "\n")

    # Remove um assinante
    parceiro.cancelar_inscricao()

    # Segunda mensagem - parceiro não recebe
    newsletter.add_mensagem("Segunda mensagem")


def exemplo_completo():
    """Exemplo 3: Cenário completo"""
    print("\n" + "=" * 80)
    print("EXEMPLO 3: Cenário Completo")
    print("=" * 80)

    newsletter = Newsletter()

    # Múltiplos assinantes de tipos diferentes
    Cliente("Cliente A", "clienteA@email.com", newsletter)
    Cliente("Cliente B", "clienteB@email.com", newsletter)
    Funcionario("Funcionário 1", "func1@empresa.com", newsletter)
    Parceiro("Parceiro Tech", "contato@tech.com", newsletter)
    Fornecedor("Fornecedor XYZ", "vendas@xyz.com", newsletter)

    # Publica mensagem para todos
    newsletter.add_mensagem("Novidades! Confira nossos novos produtos!")


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print(" " * 20 + "PADRÃO OBSERVER - EXEMPLOS")
    print(" " * 22 + "Sistema de Newsletter")
    print("=" * 80)

    exemplo_basico()
    exemplo_dinamico()
    exemplo_completo()

    print("\n" + "=" * 80)
    print("Para testar a API FastAPI, execute: python main.py")
    print("Depois acesse: http://localhost:8000/docs")
    print("=" * 80 + "\n")
