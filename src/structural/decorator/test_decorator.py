"""
Testes básicos para o padrão Decorator
"""

from pizzas_concretas import PizzaFrango, PizzaCalabresa, PizzaQueijo
from decorators_concretos import BordaRequeijao, MassaIntegral


def test_pizza_frango():
    """Testa pizza de frango sem acréscimos"""
    pizza = PizzaFrango()
    assert pizza.get_preco() == 19.00
    assert pizza.get_descricao() == "Deliciosa pizza de frango"
    print("[OK] Test Pizza Frango: PASSOU")


def test_pizza_calabresa():
    """Testa pizza de calabresa sem acréscimos"""
    pizza = PizzaCalabresa()
    assert pizza.get_preco() == 25.00
    assert pizza.get_descricao() == "Deliciosa pizza de calabresa"
    print("[OK] Test Pizza Calabresa: PASSOU")


def test_pizza_queijo():
    """Testa pizza de queijo sem acréscimos"""
    pizza = PizzaQueijo()
    assert pizza.get_preco() == 22.00
    assert pizza.get_descricao() == "Deliciosa pizza de queijo"
    print("[OK] Test Pizza Queijo: PASSOU")


def test_decorator_borda():
    """Testa decorator de borda"""
    pizza = PizzaQueijo()
    pizza_com_borda = BordaRequeijao(pizza)

    assert pizza_com_borda.get_preco() == 30.50  # 22.00 + 8.50
    assert "Borda recheada de requeijão" in pizza_com_borda.get_descricao()
    print("[OK] Test Decorator Borda: PASSOU")


def test_decorator_massa():
    """Testa decorator de massa integral"""
    pizza = PizzaFrango()
    pizza_com_massa = MassaIntegral(pizza)

    assert pizza_com_massa.get_preco() == 24.00  # 19.00 + 5.00
    assert "Massa integral" in pizza_com_massa.get_descricao()
    print("[OK] Test Decorator Massa: PASSOU")


def test_multiplos_decorators():
    """Testa múltiplos decorators na mesma pizza"""
    pizza = PizzaQueijo()
    pizza = BordaRequeijao(pizza)
    pizza = MassaIntegral(pizza)

    assert pizza.get_preco() == 35.50  # 22.00 + 8.50 + 5.00
    assert "queijo" in pizza.get_descricao()
    assert "Borda recheada de requeijão" in pizza.get_descricao()
    assert "Massa integral" in pizza.get_descricao()
    print("[OK] Test Multiplos Decorators: PASSOU")


def test_ordem_decorators():
    """Testa que a ordem dos decorators não afeta o preço final"""
    # Ordem 1: Borda -> Massa
    pizza1 = PizzaCalabresa()
    pizza1 = BordaRequeijao(pizza1)
    pizza1 = MassaIntegral(pizza1)

    # Ordem 2: Massa -> Borda
    pizza2 = PizzaCalabresa()
    pizza2 = MassaIntegral(pizza2)
    pizza2 = BordaRequeijao(pizza2)

    assert pizza1.get_preco() == pizza2.get_preco()
    print("[OK] Test Ordem Decorators: PASSOU")


def test_todas_combinacoes():
    """Testa todas as combinações possíveis"""
    pizzas = [PizzaFrango(), PizzaCalabresa(), PizzaQueijo()]
    precos_base = [19.00, 25.00, 22.00]

    for i, pizza in enumerate(pizzas):
        # Pizza simples
        assert pizza.get_preco() == precos_base[i]

        # Pizza com borda
        com_borda = BordaRequeijao(pizza.__class__())
        assert com_borda.get_preco() == precos_base[i] + 8.50

        # Pizza com massa
        com_massa = MassaIntegral(pizza.__class__())
        assert com_massa.get_preco() == precos_base[i] + 5.00

        # Pizza completa
        completa = MassaIntegral(BordaRequeijao(pizza.__class__()))
        assert completa.get_preco() == precos_base[i] + 13.50

    print("[OK] Test Todas Combinacoes: PASSOU")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("EXECUTANDO TESTES DO PADRÃO DECORATOR")
    print("=" * 60 + "\n")

    try:
        test_pizza_frango()
        test_pizza_calabresa()
        test_pizza_queijo()
        test_decorator_borda()
        test_decorator_massa()
        test_multiplos_decorators()
        test_ordem_decorators()
        test_todas_combinacoes()

        print("\n" + "=" * 60)
        print("TODOS OS TESTES PASSARAM! [OK]")
        print("=" * 60 + "\n")
    except AssertionError as e:
        print(f"\n[ERRO] TESTE FALHOU: {e}\n")
    except Exception as e:
        print(f"\n[ERRO] ERRO: {e}\n")
