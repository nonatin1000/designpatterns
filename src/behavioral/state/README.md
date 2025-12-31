# Padrão State - Sistema de Pedidos E-commerce

## 📋 Descrição

Implementação do **Padrão State** usando FastAPI. Este padrão comportamental permite que um objeto altere seu comportamento quando seu estado interno muda. O objeto parecerá ter mudado de classe.

## 🎯 Conceito

O sistema simula pedidos de um e-commerce onde cada pedido passa por diferentes estados (Aguardando Pagamento, Pago, Cancelado, Enviado). Cada estado tem comportamentos específicos para as transições disponíveis.

## 🔄 Máquina de Estados

```
┌─────────────────────┐
│ Aguardando Pagamento│◄── Estado Inicial
└──────┬──────┬───────┘
       │      │
 Pagar │      │ Cancelar
       │      │
       ▼      ▼
    ┌─────┐ ┌──────────┐
    │Pago │ │Cancelado │◄── Estados Finais
    └─┬─┬─┘ └──────────┘
      │ │
      │ └─Cancelar
      │
Despachar
      │
      ▼
 ┌────────┐
 │Enviado │◄── Estado Final
 └────────┘
```

### Transições Válidas

- **Aguardando Pagamento** →  Pagar → **Pago**
- **Aguardando Pagamento** → Cancelar → **Cancelado**
- **Pago** → Cancelar → **Cancelado**
- **Pago** → Despachar → **Enviado**

## 🏗️ Estrutura do Padrão

```
Context (Pedido)                State (Interface)
├── estado_atual: State        ├── sucesso_ao_pagar()
├── sucesso_ao_pagar()         ├── cancelar_pedido()
├── cancelar_pedido()          └── despachar_pedido()
└── despachar_pedido()                  △
                                        │
            ┌───────────────────────────┼───────────────────┐
            │                           │                   │
  AguardandoPagamento           PagoState         CanceladoState
       State                  EnviadoState
```

## 📁 Arquivos

```
state/
├── state_interface.py    # Interface State
├── estados.py            # 4 ConcreteStates
├── pedido.py            # Context (Pedido)
├── schemas.py           # Modelos Pydantic
├── main.py              # API FastAPI
├── exemplo.py           # Exemplos de uso
├── test_state.py        # Testes unitários
└── README.md            # Esta documentação
```

## 🚀 Como Executar

### 1. Exemplos (sem dependências)

```bash
cd src/behavioral/state
python exemplo.py
```

### 2. Testes

```bash
cd src/behavioral/state
python test_state.py
```

### 3. API FastAPI

```bash
cd designpatterns
pip install -r requirements.txt
cd src/behavioral/state
python main.py
```

Acesse: http://localhost:8000/docs

## 🌐 Endpoints da API

### POST `/pedidos`
Cria novo pedido (estado inicial: Aguardando Pagamento)

**Request:**
```json
{
  "itens": ["Notebook", "Mouse"],
  "valor_total": 2500.00
}
```

### POST `/pedidos/{id}/pagar`
Transição: Sucesso ao Pagar (Aguardando → Pago)

### POST `/pedidos/{id}/cancelar`
Transição: Cancelar Pedido

### POST `/pedidos/{id}/despachar`
Transição: Despachar Pedido (Pago → Enviado)

### GET `/pedidos/{id}`
Obtém informações do pedido

## 💡 Vantagens do Padrão

1. **Elimina Condicionais Complexas**: Cada estado encapsula seu comportamento
2. **Transições Explícitas**: Mudanças de estado são claras e rastreáveis
3. **Fácil Extensão**: Novos estados podem ser adicionados facilmente
4. **Single Responsibility**: Cada estado tem uma responsabilidade específica

## 🎓 Quando Utilizar

- Comportamento do objeto depende do estado interno
- Operações possuem condicionais grandes baseadas no estado
- Transições de estado complexas e bem definidas

## 📊 Comparação: Sem vs Com State Pattern

### Sem State Pattern
```python
def pagar(self):
    if self.estado == AGUARDANDO:
        self.estado = PAGO
    elif self.estado == PAGO:
        raise Exception("Já pago")
    # ... muitas condicionais
```

### Com State Pattern
```python
def pagar(self):
    self.estado_atual.sucesso_ao_pagar()  # Delega para o estado
```

## 📚 Referência

Baseado no livro "Rabiscando Padrões de Projeto" - Padrão State
