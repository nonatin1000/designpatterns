# Padrão Decorator - Sistema de Pizzaria

## 📋 Descrição

Implementação do **Padrão Decorator** usando FastAPI. Este padrão estrutural permite anexar responsabilidades adicionais a um objeto dinamicamente, fornecendo uma alternativa flexível ao uso de subclasses para extensão de funcionalidades.

## 🎯 Conceito

O sistema simula uma pizzaria onde clientes podem adicionar características extras às pizzas (acréscimos). Cada acréscimo "decora" a pizza base, adicionando funcionalidade sem modificar a classe original.

### Cardápio

**Pizzas Base:**
- Pizza de Frango - R$ 19,00
- Pizza de Calabresa - R$ 25,00
- Pizza de Queijo - R$ 22,00

**Acréscimos (Decorators):**
- Borda recheada com requeijão - R$ 8,50
- Massa Integral - R$ 5,00

## 🏗️ Estrutura do Padrão

```
Pizza (Component)
├── PizzaFrango (ConcreteComponent)
├── PizzaCalabresa (ConcreteComponent)
├── PizzaQueijo (ConcreteComponent)
└── AcrescimoDecorator (Decorator)
    ├── BordaRequeijao (ConcreteDecorator)
    └── MassaIntegral (ConcreteDecorator)
```

### Componentes

1. **Pizza (Component)**: Interface base para pizzas e decorators
2. **PizzaFrango, PizzaCalabresa, PizzaQueijo (ConcreteComponent)**: Pizzas concretas
3. **AcrescimoDecorator (Decorator)**: Classe base para decorators que mantém referência à pizza
4. **BordaRequeijao, MassaIntegral (ConcreteDecorator)**: Decorators concretos que adicionam funcionalidades

## 🔄 Como Funciona

```python
# 1. Cria pizza base
pizza = PizzaQueijo()  # R$ 22,00

# 2. Adiciona borda (primeiro decorator)
pizza = BordaRequeijao(pizza)  # R$ 22,00 + R$ 8,50 = R$ 30,50

# 3. Adiciona massa integral (segundo decorator)
pizza = MassaIntegral(pizza)  # R$ 30,50 + R$ 5,00 = R$ 35,50
```

### Fluxo de Execução

Quando `pizza.get_preco()` é chamado:

```
MassaIntegral.get_preco()
  └─> self.pizza.get_preco() + 5.00
      └─> BordaRequeijao.get_preco()
          └─> self.pizza.get_preco() + 8.50
              └─> PizzaQueijo.get_preco()
                  └─> return 22.00
              ← return 30.50
          ← return 35.50
```

## 📁 Arquivos

```
decorator/
├── pizza.py                    # Classe abstrata base (Component)
├── pizzas_concretas.py         # Implementações de pizzas (ConcreteComponents)
├── acrescimo_decorator.py      # Classe abstrata decorator (Decorator)
├── decorators_concretos.py     # Implementações de acréscimos (ConcreteDecorators)
├── schemas.py                  # Modelos Pydantic para API
├── main.py                     # API FastAPI
├── exemplo.py                  # Exemplos de uso sem API
├── __init__.py                 # Exportações do módulo
└── README.md                   # Esta documentação
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12+
- Docker e Docker Compose (opcional)

### 1. Executar exemplos standalone (sem dependências)

```bash
cd src/behavioral/decorator
python exemplo.py
```

### 2. Executar testes

```bash
cd src/behavioral/decorator
python test_decorator.py
```

### 3. Executar API FastAPI

#### Opção A: Usando ambiente virtual

```bash
# Navegar para o diretório raiz do projeto
cd designpatterns

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
# source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação do decorator
cd src/behavioral/decorator
python main.py
```

#### Opção B: Usando Docker (recomendado)

```bash
# Navegar para o diretório raiz do projeto
cd designpatterns

# Build e executar com docker-compose
docker-compose up --build

# Em outro terminal, acessar o container
docker exec -it <container-name> bash
cd behavioral/decorator
python main.py
```

Acesse a documentação interativa em: http://localhost:8000/docs

## 🌐 Endpoints da API

### GET `/`
Informações sobre a API

### GET `/cardapio`
Retorna o cardápio completo

**Response:**
```json
{
  "pizzas": [
    {"nome": "Pizza de Frango", "preco": 19.00, "tipo": "frango"},
    {"nome": "Pizza de Calabresa", "preco": 25.00, "tipo": "calabresa"},
    {"nome": "Pizza de Queijo", "preco": 22.00, "tipo": "queijo"}
  ],
  "acrescimos": [
    {"nome": "Borda recheada com requeijão", "preco": 8.50, "tipo": "borda_requeijao"},
    {"nome": "Massa Integral", "preco": 5.00, "tipo": "massa_integral"}
  ]
}
```

### POST `/pizza`
Cria uma pizza customizada

**Request:**
```json
{
  "tipo_pizza": "queijo",
  "acrescimos": ["borda_requeijao", "massa_integral"]
}
```

**Response:**
```json
{
  "descricao": "Deliciosa pizza de queijo + Borda recheada de requeijão + Massa integral",
  "preco": 35.50
}
```

### GET `/pizza/exemplo/{tipo}`
Retorna exemplo de pizza completa (com todos os acréscimos)

**Exemplo:** `/pizza/exemplo/frango`

## 💡 Vantagens do Padrão

1. **Flexibilidade em tempo de execução**: Acréscimos podem ser adicionados dinamicamente
2. **Responsabilidade Única**: Cada classe tem uma responsabilidade específica
3. **Aberto/Fechado**: Novos decorators podem ser adicionados sem modificar código existente
4. **Composição sobre Herança**: Usa composição ao invés de criar subclasses para cada combinação

### Comparação

**Sem Decorator Pattern:**
- Necessário criar classes para cada combinação:
  - `PizzaFrangoBorda`
  - `PizzaFrangoBordaMassa`
  - `PizzaFrangoMassa`
  - `PizzaCalabresaBorda`
  - ... (12 classes para 3 pizzas e 2 acréscimos)

**Com Decorator Pattern:**
- 3 classes de pizza base
- 2 classes de decorator
- **Infinitas combinações possíveis!**

## 🎓 Quando Utilizar

- Adicionar comportamentos a objetos individuais de forma dinâmica
- Implementar comportamentos que podem ser fundamentais para alguns objetos e desnecessários para outros
- Evitar explosão de subclasses para suportar todas as combinações possíveis
- Quando a definição de classe está oculta ou indisponível para herança

## 📚 Referência

Baseado no livro "Rabiscando Padrões de Projeto" - Padrão Decorator
