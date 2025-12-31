# Arquitetura do Padrão Decorator - Pizzaria

## Diagrama de Classes

```
                         Pizza (Abstract Component)
                        ┌─────────────────────────────┐
                        │ - descricao: str            │
                        │ - preco: float              │
                        │ + get_descricao(): str      │
                        │ + get_preco(): float        │
                        └─────────────────────────────┘
                                      △
                                      │
                  ┌───────────────────┴───────────────────┐
                  │                                       │
        ┌─────────┴─────────┐              ┌─────────────┴──────────────┐
        │ ConcreteComponents │              │   AcrescimoDecorator       │
        └────────────────────┘              │   (Abstract Decorator)     │
                  △                         │ - pizza: Pizza             │
                  │                         │ + get_descricao(): str     │
      ┌───────────┼───────────┐            │ + get_preco(): float       │
      │           │           │            └────────────────────────────┘
      │           │           │                         △
┌─────┴─────┐ ┌──┴───┐ ┌─────┴─────┐                  │
│PizzaFrango│ │Pizza │ │   Pizza   │         ┌────────┴────────┐
│           │ │Cala- │ │  Queijo   │         │                 │
│19.00      │ │bresa │ │           │   ┌─────┴──────┐  ┌──────┴─────┐
└───────────┘ │25.00 │ │  22.00    │   │   Borda    │  │   Massa    │
              └──────┘ └───────────┘   │ Requeijao  │  │  Integral  │
                                       │  + 8.50    │  │  + 5.00    │
                                       └────────────┘  └────────────┘
```

## Estrutura de Arquivos

```
decorator/
│
├── Componentes Base (Component & ConcreteComponents)
│   ├── pizza.py                    # Classe abstrata base
│   └── pizzas_concretas.py         # PizzaFrango, PizzaCalabresa, PizzaQueijo
│
├── Decorators (Decorator & ConcreteDecorators)
│   ├── acrescimo_decorator.py      # Classe abstrata decorator
│   └── decorators_concretos.py     # BordaRequeijao, MassaIntegral
│
├── API FastAPI
│   ├── main.py                     # Aplicação FastAPI
│   └── schemas.py                  # Modelos Pydantic
│
├── Exemplos e Testes
│   ├── exemplo.py                  # Demonstrações do padrão
│   └── test_decorator.py           # Testes unitários
│
├── Documentação
│   ├── README.md                   # Documentação principal
│   ├── ARQUITETURA.md             # Este arquivo
│   └── Decorator.pdf              # Material de referência
│
└── Módulo
    └── __init__.py                # Exportações do pacote
```

## Fluxo de Execução

### Exemplo: Pizza de Queijo com Borda e Massa Integral

```python
# 1. Criar pizza base
pizza = PizzaQueijo()
# Objeto: PizzaQueijo
# Preço: R$ 22,00

# 2. Decorar com borda
pizza = BordaRequeijao(pizza)
# Objeto: BordaRequeijao(PizzaQueijo)
# Preço: pizza.get_preco() + 8.50 = R$ 30,50

# 3. Decorar com massa
pizza = MassaIntegral(pizza)
# Objeto: MassaIntegral(BordaRequeijao(PizzaQueijo))
# Preço: pizza.get_preco() + 5.00 = R$ 35,50
```

### Chamada de Métodos (Recursão)

```
pizza.get_preco()
│
└─> MassaIntegral.get_preco()
    │
    ├─> self.pizza.get_preco() + 5.00
    │   │
    │   └─> BordaRequeijao.get_preco()
    │       │
    │       ├─> self.pizza.get_preco() + 8.50
    │       │   │
    │       │   └─> PizzaQueijo.get_preco()
    │       │       │
    │       │       └─> return 22.00
    │       │
    │       └─> return 30.50
    │
    └─> return 35.50
```

## Principais Componentes

### 1. Component (Pizza)
- Define a interface para objetos que podem ter responsabilidades adicionadas
- Classe abstrata base para pizzas e decorators

### 2. ConcreteComponent (PizzaFrango, PizzaCalabresa, PizzaQueijo)
- Implementações concretas do component
- Objetos aos quais funcionalidades podem ser adicionadas dinamicamente

### 3. Decorator (AcrescimoDecorator)
- Mantém referência a um objeto Component
- Define interface que está em conformidade com a interface do Component
- Classe abstrata base para todos os decorators

### 4. ConcreteDecorator (BordaRequeijao, MassaIntegral)
- Adiciona responsabilidades ao component
- Implementa comportamento adicional antes/depois de delegar ao component decorado

## API FastAPI

### Endpoints

```
GET  /                     - Informações da API
GET  /cardapio            - Lista pizzas e acréscimos
POST /pizza               - Cria pizza customizada
GET  /pizza/exemplo/{tipo} - Exemplo de pizza completa
```

### Schemas Pydantic

- **TipoPizza**: Enum com tipos de pizza (frango, calabresa, queijo)
- **TipoAcrescimo**: Enum com acréscimos (borda_requeijao, massa_integral)
- **PedidoPizzaRequest**: Request para criar pizza
- **PizzaResponse**: Response com descrição e preço
- **CardapioResponse**: Response com cardápio completo

## Vantagens Observadas

### 1. Flexibilidade
- Acréscimos adicionados em tempo de execução
- Combinações dinâmicas sem explosão de classes

### 2. Responsabilidade Única
- Cada classe tem uma responsabilidade específica
- Pizza cuida do produto base
- Decorator cuida dos acréscimos

### 3. Aberto/Fechado (Open/Closed Principle)
- Aberto para extensão (novos decorators)
- Fechado para modificação (não altera classes existentes)

### 4. Composição sobre Herança
- Usa composição ao invés de herança
- Evita hierarquia de classes complexa

## Comparação: Com vs Sem Decorator

### Sem Decorator (Herança)
```
PizzaFrango
PizzaFrangoBorda
PizzaFrangoBordaMassa
PizzaFrangoMassa
PizzaCalabresa
PizzaCalabresaBorda
PizzaCalabresaBordaMassa
PizzaCalabresaMassa
PizzaQueijo
PizzaQueijoBorda
PizzaQueijoBordaMassa
PizzaQueijoMassa
```
**Total: 12 classes** para 3 pizzas e 2 acréscimos

### Com Decorator (Composição)
```
Pizza (abstrata)
├── PizzaFrango
├── PizzaCalabresa
└── PizzaQueijo

AcrescimoDecorator (abstrata)
├── BordaRequeijao
└── MassaIntegral
```
**Total: 5 classes** + infinitas combinações possíveis

**Redução: 58% menos classes**

## Exemplos de Uso

### 1. Pizza Simples
```python
pizza = PizzaFrango()
print(pizza.get_preco())      # 19.00
print(pizza.get_descricao())  # "Deliciosa pizza de frango"
```

### 2. Pizza com Um Acréscimo
```python
pizza = PizzaQueijo()
pizza = BordaRequeijao(pizza)
print(pizza.get_preco())      # 30.50
```

### 3. Pizza com Múltiplos Acréscimos
```python
pizza = PizzaCalabresa()
pizza = BordaRequeijao(pizza)
pizza = MassaIntegral(pizza)
print(pizza.get_preco())      # 38.50
```

### 4. Via API REST
```bash
curl -X POST http://localhost:8000/pizza \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_pizza": "queijo",
    "acrescimos": ["borda_requeijao", "massa_integral"]
  }'
```

Response:
```json
{
  "descricao": "Deliciosa pizza de queijo + Borda recheada de requeijão + Massa integral",
  "preco": 35.50
}
```

## Extensibilidade

### Adicionar Nova Pizza
```python
class PizzaVegetariana(Pizza):
    def __init__(self):
        super().__init__()
        self.descricao = "Pizza vegetariana"
        self.preco = 24.00

    def get_descricao(self) -> str:
        return self.descricao

    def get_preco(self) -> float:
        return self.preco
```

### Adicionar Novo Acréscimo
```python
class Catupiry(AcrescimoDecorator):
    def get_descricao(self) -> str:
        return f"{self.pizza.get_descricao()} + Catupiry"

    def get_preco(self) -> float:
        return self.pizza.get_preco() + 6.00
```

Nenhuma modificação nas classes existentes é necessária!
