"""
Testes básicos para o padrão Observer
"""

from newsletter import Newsletter
from observers import Cliente, Funcionario, Parceiro, Fornecedor


def test_registro_observer():
    """Testa registro de observer"""
    newsletter = Newsletter()
    cliente = Cliente("Teste", "teste@email.com", newsletter)

    assert newsletter.get_total_assinantes() == 1
    print("[OK] Test Registro Observer: PASSOU")


def test_remocao_observer():
    """Testa remoção de observer"""
    newsletter = Newsletter()
    cliente = Cliente("Teste", "teste@email.com", newsletter)
    assert newsletter.get_total_assinantes() == 1

    cliente.cancelar_inscricao()
    assert newsletter.get_total_assinantes() == 0
    print("[OK] Test Remocao Observer: PASSOU")


def test_multiplos_observers():
    """Testa múltiplos observers"""
    newsletter = Newsletter()

    Cliente("Cliente", "cliente@email.com", newsletter)
    Funcionario("Func", "func@email.com", newsletter)
    Parceiro("Parceiro", "parceiro@email.com", newsletter)

    assert newsletter.get_total_assinantes() == 3
    print("[OK] Test Multiplos Observers: PASSOU")


def test_publicacao_mensagem():
    """Testa publicação de mensagem"""
    newsletter = Newsletter()
    Cliente("Teste", "teste@email.com", newsletter)

    newsletter.add_mensagem("Teste de mensagem")
    mensagens = newsletter.get_mensagens()

    assert len(mensagens) == 1
    assert mensagens[0] == "Teste de mensagem"
    print("[OK] Test Publicacao Mensagem: PASSOU")


def test_notificacao_observers():
    """Testa notificação de observers"""
    newsletter = Newsletter()

    c1 = Cliente("C1", "c1@email.com", newsletter)
    c2 = Cliente("C2", "c2@email.com", newsletter)

    # Remove um observer
    c2.cancelar_inscricao()

    # Publica mensagem - só c1 deve estar na lista
    newsletter.add_mensagem("Teste")

    assert newsletter.get_total_assinantes() == 1
    print("[OK] Test Notificacao Observers: PASSOU")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("EXECUTANDO TESTES DO PADRÃO OBSERVER")
    print("=" * 60 + "\n")

    try:
        test_registro_observer()
        test_remocao_observer()
        test_multiplos_observers()
        test_publicacao_mensagem()
        test_notificacao_observers()

        print("\n" + "=" * 60)
        print("TODOS OS TESTES PASSARAM! [OK]")
        print("=" * 60 + "\n")
    except AssertionError as e:
        print(f"\n[ERRO] TESTE FALHOU: {e}\n")
    except Exception as e:
        print(f"\n[ERRO] ERRO: {e}\n")
