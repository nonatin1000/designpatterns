"""
Exemplo de uso do Padrão Decorator - Sistema de Pizzaria

Este arquivo demonstra o uso do padrão Decorator sem a API,
mostrando como os decorators funcionam na prática.

Padrão Decorator:
- Permite adicionar responsabilidades a objetos dinamicamente
- Fornece alternativa flexível à herança para estender funcionalidades
- Cada decorator envolve um componente e adiciona comportamento
"""

from pizzas_concretas import PizzaFrango, PizzaCalabresa, PizzaQueijo
from decorators_concretos import BordaRequeijao, MassaIntegral


def imprimir_pizza(titulo: str, pizza):
    """Helper para imprimir informações da pizza"""
    print(f"\n{titulo}")
    print(f"Descrição: {pizza.get_descricao()}")
    print(f"Preço: R$ {pizza.get_preco():.2f}")
    print("-" * 80)


def exemplo_basico():
    """Exemplo 1: Pizza básica sem acréscimos"""
    print("\n" + "=" * 80)
    print("EXEMPLO 1: Pizza Básica (sem decorators)")
    print("=" * 80)

    pizza_queijo = PizzaQueijo()
    imprimir_pizza("Pizza de Queijo simples", pizza_queijo)


def exemplo_com_um_decorator():
    """Exemplo 2: Pizza com um acréscimo (um decorator)"""
    print("\n" + "=" * 80)
    print("EXEMPLO 2: Pizza com UM decorator")
    print("=" * 80)

    # Cria pizza base
    pizza_frango = PizzaFrango()
    imprimir_pizza("1. Pizza de Frango (base)", pizza_frango)

    # Adiciona borda de requeijão (aplica o decorator)
    pizza_com_borda = BordaRequeijao(pizza_frango)
    imprimir_pizza("2. Pizza de Frango + Borda de Requeijão", pizza_com_borda)


def exemplo_com_multiplos_decorators():
    """Exemplo 3: Pizza com múltiplos acréscimos (múltiplos decorators)"""
    print("\n" + "=" * 80)
    print("EXEMPLO 3: Pizza com MÚLTIPLOS decorators")
    print("=" * 80)

    # Cria pizza base
    pizza_queijo = PizzaQueijo()
    imprimir_pizza("1. Pizza de Queijo (base)", pizza_queijo)

    # Adiciona primeiro decorator (borda)
    pizza_com_borda = BordaRequeijao(pizza_queijo)
    imprimir_pizza("2. Pizza + Borda de Requeijão (1º decorator)", pizza_com_borda)

    # Adiciona segundo decorator (massa integral)
    # Note que estamos decorando o objeto já decorado!
    pizza_completa = MassaIntegral(pizza_com_borda)
    imprimir_pizza(
        "3. Pizza + Borda + Massa Integral (2º decorator)",
        pizza_completa
    )

    print("\nFluxo de chamadas quando pizza_completa.get_preco() é executado:")
    print("1. MassaIntegral.get_preco() é chamado")
    print("2. MassaIntegral chama self.pizza.get_preco() [que é BordaRequeijao]")
    print("3. BordaRequeijao.get_preco() chama self.pizza.get_preco() [que é PizzaQueijo]")
    print("4. PizzaQueijo.get_preco() retorna 22.00")
    print("5. BordaRequeijao adiciona 8.50 -> retorna 30.50")
    print("6. MassaIntegral adiciona 5.00 -> retorna 35.50")


def exemplo_ordem_importa():
    """Exemplo 4: Demonstra que a ordem dos decorators não afeta o resultado final"""
    print("\n" + "=" * 80)
    print("EXEMPLO 4: Ordem dos decorators")
    print("=" * 80)

    # Ordem 1: Borda -> Massa
    pizza1 = PizzaCalabresa()
    pizza1 = BordaRequeijao(pizza1)
    pizza1 = MassaIntegral(pizza1)
    imprimir_pizza("Ordem 1: Calabresa -> Borda -> Massa", pizza1)

    # Ordem 2: Massa -> Borda
    pizza2 = PizzaCalabresa()
    pizza2 = MassaIntegral(pizza2)
    pizza2 = BordaRequeijao(pizza2)
    imprimir_pizza("Ordem 2: Calabresa -> Massa -> Borda", pizza2)

    print(f"\nO preço é o mesmo? {pizza1.get_preco() == pizza2.get_preco()}")
    print("Mas as descrições são diferentes!")


def exemplo_comparacao_todas_pizzas():
    """Exemplo 5: Compara todas as pizzas com todos os acréscimos"""
    print("\n" + "=" * 80)
    print("EXEMPLO 5: Comparação de todas as combinações")
    print("=" * 80)

    pizzas = [
        ("Frango", PizzaFrango()),
        ("Calabresa", PizzaCalabresa()),
        ("Queijo", PizzaQueijo())
    ]

    for nome, pizza_base in pizzas:
        # Pizza simples
        print(f"\n{nome} simples: R$ {pizza_base.get_preco():.2f}")

        # Pizza com borda
        com_borda = BordaRequeijao(pizza_base.__class__())
        print(f"{nome} + Borda: R$ {com_borda.get_preco():.2f}")

        # Pizza com massa
        com_massa = MassaIntegral(pizza_base.__class__())
        print(f"{nome} + Massa: R$ {com_massa.get_preco():.2f}")

        # Pizza completa
        completa = MassaIntegral(BordaRequeijao(pizza_base.__class__()))
        print(f"{nome} + Borda + Massa: R$ {completa.get_preco():.2f}")


def exemplo_vantagens_decorator():
    """Exemplo 6: Demonstra as vantagens do padrão"""
    print("\n" + "=" * 80)
    print("EXEMPLO 6: Vantagens do Padrão Decorator")
    print("=" * 80)

    print("\nVANTAGENS:")
    print("1. Flexibilidade: Acréscimos podem ser adicionados em tempo de execução")
    print("2. Responsabilidade única: Cada classe tem uma responsabilidade")
    print("3. Aberto/Fechado: Pode adicionar novos decorators sem modificar código existente")
    print("4. Composição: Usa composição ao invés de herança")

    print("\nSEM o padrão Decorator, precisaríamos criar classes como:")
    print("  - PizzaFrangoBorda")
    print("  - PizzaFrangoBordaMassa")
    print("  - PizzaFrangoMassa")
    print("  - PizzaCalabresaBorda")
    print("  - PizzaCalabresaBordaMassa")
    print("  - ... (explosão de classes!)")

    print("\nCOM o padrão Decorator:")
    print("  - 3 classes de pizza base")
    print("  - 2 classes de decorator")
    print("  - Infinitas combinações possíveis!")

    total_sem_decorator = 3 * (2**2)  # 3 pizzas × 2^2 combinações de acréscimos
    total_com_decorator = 3 + 2  # 3 pizzas + 2 decorators

    print(f"\nClasses necessárias SEM decorator: {total_sem_decorator}")
    print(f"Classes necessárias COM decorator: {total_com_decorator}")
    print(f"Redução: {((total_sem_decorator - total_com_decorator) / total_sem_decorator * 100):.0f}%")


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print(" " * 20 + "PADRÃO DECORATOR - EXEMPLOS")
    print(" " * 25 + "Sistema de Pizzaria")
    print("=" * 80)

    exemplo_basico()
    exemplo_com_um_decorator()
    exemplo_com_multiplos_decorators()
    exemplo_ordem_importa()
    exemplo_comparacao_todas_pizzas()
    exemplo_vantagens_decorator()

    print("\n" + "=" * 80)
    print("Para testar a API FastAPI, execute: python main.py")
    print("Depois acesse: http://localhost:8000/docs")
    print("=" * 80 + "\n")
