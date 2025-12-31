"""Testes para o padrão State"""

from pedido import Pedido


def test_estado_inicial():
    """Testa que pedido inicia em Aguardando Pagamento"""
    pedido = Pedido(itens=["Item1"], valor_total=100.0)
    assert pedido.get_estado_nome() == "Aguardando Pagamento"
    print("[OK] Test Estado Inicial: PASSOU")


def test_transicao_pagar():
    """Testa transição de pagamento"""
    pedido = Pedido(itens=["Item1"], valor_total=100.0)
    pedido.sucesso_ao_pagar()
    assert pedido.get_estado_nome() == "Pago"
    print("[OK] Test Transicao Pagar: PASSOU")


def test_transicao_despachar():
    """Testa transição de despacho"""
    pedido = Pedido(itens=["Item1"], valor_total=100.0)
    pedido.sucesso_ao_pagar()
    pedido.despachar_pedido()
    assert pedido.get_estado_nome() == "Enviado"
    print("[OK] Test Transicao Despachar: PASSOU")


def test_cancelar_aguardando():
    """Testa cancelamento de pedido aguardando pagamento"""
    pedido = Pedido(itens=["Item1"], valor_total=100.0)
    pedido.cancelar_pedido()
    assert pedido.get_estado_nome() == "Cancelado"
    print("[OK] Test Cancelar Aguardando: PASSOU")


def test_transicao_invalida():
    """Testa que transições inválidas geram exceção"""
    pedido = Pedido(itens=["Item1"], valor_total=100.0)

    try:
        pedido.despachar_pedido()  # Não pode despachar sem pagar
        assert False, "Deveria ter lançado exceção"
    except Exception:
        assert pedido.get_estado_nome() == "Aguardando Pagamento"
        print("[OK] Test Transicao Invalida: PASSOU")


def test_historico():
    """Testa registro de histórico de estados"""
    pedido = Pedido(itens=["Item1"], valor_total=100.0)
    pedido.sucesso_ao_pagar()

    historico = pedido.get_historico()
    assert len(historico) >= 2
    print("[OK] Test Historico: PASSOU")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("EXECUTANDO TESTES DO PADRAO STATE")
    print("=" * 60 + "\n")

    try:
        test_estado_inicial()
        test_transicao_pagar()
        test_transicao_despachar()
        test_cancelar_aguardando()
        test_transicao_invalida()
        test_historico()

        print("\n" + "=" * 60)
        print("TODOS OS TESTES PASSARAM! [OK]")
        print("=" * 60 + "\n")
    except AssertionError as e:
        print(f"\n[ERRO] TESTE FALHOU: {e}\n")
    except Exception as e:
        print(f"\n[ERRO] ERRO: {e}\n")
