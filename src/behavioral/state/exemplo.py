"""Exemplo de uso do Padrão State - Sistema de Pedidos E-commerce"""

from pedido import Pedido


def exemplo_fluxo_completo():
    """Exemplo 1: Fluxo completo de um pedido"""
    print("\n" + "=" * 80)
    print("EXEMPLO 1: Fluxo Completo do Pedido")
    print("=" * 80)

    pedido = Pedido(itens=["Notebook", "Mouse"], valor_total=2500.00)
    print(f"\nEstado atual: {pedido.get_estado_nome()}\n")

    # Pagar pedido
    pedido.sucesso_ao_pagar()
    print(f"\nEstado atual: {pedido.get_estado_nome()}\n")

    # Despachar pedido
    pedido.despachar_pedido()
    print(f"\nEstado atual: {pedido.get_estado_nome()}\n")


def exemplo_cancelamento():
    """Exemplo 2: Cancelamento de pedido"""
    print("\n" + "=" * 80)
    print("EXEMPLO 2: Cancelamento de Pedido")
    print("=" * 80)

    pedido = Pedido(itens=["Teclado"], valor_total=150.00)
    print(f"\nEstado: {pedido.get_estado_nome()}")

    pedido.cancelar_pedido()
    print(f"\nEstado: {pedido.get_estado_nome()}\n")


def exemplo_transicao_invalida():
    """Exemplo 3: Tentativa de transição inválida"""
    print("\n" + "=" * 80)
    print("EXEMPLO 3: Transicao Invalida (captura de erro)")
    print("=" * 80)

    pedido = Pedido(itens=["Monitor"], valor_total=800.00)

    try:
        # Tentar despachar sem pagar
        pedido.despachar_pedido()
    except Exception as e:
        print(f"\nErro esperado capturado: {e}\n")


def exemplo_historico():
    """Exemplo 4: Histórico de mudanças de estado"""
    print("\n" + "=" * 80)
    print("EXEMPLO 4: Historico de Estados")
    print("=" * 80)

    pedido = Pedido(itens=["Smartphone"], valor_total=1500.00)
    pedido.sucesso_ao_pagar()
    pedido.despachar_pedido()

    print("\nHistorico de mudancas de estado:")
    for registro in pedido.get_historico():
        print(f"  - {registro}")
    print()


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print(" " * 25 + "PADRAO STATE - EXEMPLOS")
    print(" " * 22 + "Sistema de Pedidos E-commerce")
    print("=" * 80)

    exemplo_fluxo_completo()
    exemplo_cancelamento()
    exemplo_transicao_invalida()
    exemplo_historico()

    print("=" * 80)
    print("Para testar a API: python main.py")
    print("Acesse: http://localhost:8000/docs")
    print("=" * 80 + "\n")
