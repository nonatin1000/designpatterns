# Padrão Observer - Sistema de Newsletter

## 📋 Descrição

Implementação do **Padrão Observer** usando FastAPI. Este padrão comportamental define uma dependência um-para-muitos entre objetos, de modo que quando um objeto muda seu estado, todos seus dependentes são notificados e atualizados automaticamente.

## 🎯 Conceito

O sistema simula uma newsletter empresarial onde diferentes tipos de assinantes (clientes, funcionários, parceiros e fornecedores) podem se inscrever para receber emails de notícias. Quando uma nova mensagem é publicada, todos os assinantes são notificados automaticamente.

### Participantes

**Subject (Newsletter):**
- Mantém lista de observers
- Permite adicionar/remover observers
- Notifica observers sobre mudanças de estado

**Observers (Assinantes):**
- Cliente - Clientes da empresa
- Funcionário - Funcionários internos
- Parceiro - Parceiros de negócios
- Fornecedor - Fornecedores

## 🏗️ Estrutura do Padrão

```
<<interface>> Subject          <<interface>> Observer
├── register_observer()       ├── update()
├── remove_observer()         ├── get_nome()
└── notify_observers()        └── get_email()
        △                              △
        │                              │
    Newsletter                   ┌─────┴─────┬─────────┬──────────┐
                                 │           │         │          │
                            Cliente  Funcionario  Parceiro  Fornecedor
```

## 🔄 Como Funciona

```python
# 1. Criar newsletter (Subject)
newsletter = Newsletter()

# 2. Assinantes se inscrevem (Observers)
cliente = Cliente("João", "joao@email.com", newsletter)
funcionario = Funcionario("Maria", "maria@empresa.com", newsletter)

# 3. Newsletter publica mensagem
newsletter.add_mensagem("Novidades!")

# 4. Todos os assinantes são notificados automaticamente
#    Observer.update() é chamado para cada assinante
```

## 📁 Arquivos

```
observer/
├── observer_interface.py      # Interface Observer
├── subject_interface.py       # Interface Subject
├── newsletter.py              # ConcreteSubject (Newsletter)
├── observers.py               # ConcreteObservers (Cliente, etc)
├── email_service.py           # Serviço de notificação
├── schemas.py                 # Modelos Pydantic
├── main.py                    # API FastAPI
├── exemplo.py                 # Exemplos de uso
├── test_observer.py           # Testes unitários
└── README.md                  # Esta documentação
```

## 🚀 Como Executar

### 1. Executar exemplos (sem dependências)

```bash
cd src/behavioral/observer
python exemplo.py
```

### 2. Executar testes

```bash
cd src/behavioral/observer
python test_observer.py
```

### 3. Executar API FastAPI

```bash
# Navegar para raiz do projeto
cd designpatterns

# Instalar dependências (se ainda não instalou)
pip install -r requirements.txt

# Executar API
cd src/behavioral/observer
python main.py
```

Acesse: http://localhost:8000/docs

## 🌐 Endpoints da API

### GET `/status`
Retorna status da newsletter (total assinantes, mensagens)

### POST `/assinantes`
Inscreve novo assinante

**Request:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "tipo": "cliente"
}
```

### DELETE `/assinantes`
Cancela inscrição

**Request:**
```json
{
  "email": "joao@email.com"
}
```

### POST `/mensagens`
Publica nova mensagem (notifica todos)

**Request:**
```json
{
  "conteudo": "Novidades! Confira nossos produtos!"
}
```

## 💡 Vantagens do Padrão

1. **Acoplamento Mínimo**: Subject e Observers se conhecem apenas através de interfaces
2. **Comunicação Broadcast**: Subject não precisa saber quantos observers existem
3. **Adição/Remoção Dinâmica**: Observers podem ser adicionados/removidos em tempo de execução
4. **Open/Closed Principle**: Novos observers podem ser adicionados sem modificar o Subject

## 🎓 Quando Utilizar

- Quando mudança em um objeto requer mudança em outros (quantidade desconhecida)
- Quando objeto deve notificar outros sem conhecê-los (baixo acoplamento)
- Quando abstração tem dois aspectos dependentes que devem variar independentemente

## 📊 Princípios SOLID Aplicados

1. **Programação para Abstrações**: Interfaces Subject e Observer
2. **Objetos Levemente Acoplados**: Subject só conhece interface Observer
3. **Open/Closed**: Novos observers sem modificar Subject
4. **Composição sobre Herança**: Subject compõe lista de observers dinamicamente

## 📚 Referência

Baseado no livro "Rabiscando Padrões de Projeto" - Padrão Observer
