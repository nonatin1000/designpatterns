# Design Patterns

Este projeto é uma API de estudo de design patterns do curso Rabiscando Padrões de Projeto.

## Padrões Implementados

### Padrões Comportamentais (Behavioral)

| Padrão | Descrição | Diretório | Testes |
|--------|-----------|-----------|--------|
| **Strategy** | Define família de algoritmos intercambiáveis | [src/behavioral/strategy](src/behavioral/strategy) | ✅ 23 testes |
| **Template Method** | Define esqueleto de algoritmo, delegando passos | [src/behavioral/template_method](src/behavioral/template_method) | ✅ 24 testes |
| **Observer** | Define dependência um-para-muitos entre objetos | [src/behavioral/observer](src/behavioral/observer) | ✅ 40 testes |
| **State** | Permite objeto alterar comportamento quando estado muda | [src/behavioral/state](src/behavioral/state) | ✅ 30 testes |

### Padrões Estruturais (Structural)

| Padrão | Descrição | Diretório | Testes |
|--------|-----------|-----------|--------|
| **Adapter** | Permite interfaces incompatíveis trabalharem juntas | [src/structural/adapter](src/structural/adapter) | ✅ 26 testes |
| **Decorator** | Adiciona responsabilidades a objetos dinamicamente | [src/structural/decorator](src/structural/decorator) | ✅ 17 testes |
| **Facade** | Fornece interface unificada para subsistema complexo | [src/structural/facade](src/structural/facade) | ✅ 25 testes |

**Total: 185 testes com cobertura completa!**

## Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno e de alta performance para construir APIs com Python 3.6+ baseado em standard Python type hints.
- **[Docker](https://www.docker.com/)**: Plataforma para desenvolver, enviar e executar aplicações em containers.
- **[Docker Compose](https://docs.docker.com/compose/)**: Ferramenta para definir e executar aplicações multi-container Docker.
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Biblioteca para validação de dados e configurações utilizando type hints.
- **[Python 3.11](https://www.python.org/)**: Linguagem de programação utilizada no desenvolvimento deste projeto.

## Executando o Projeto

### Pré-requisitos

- Docker e Docker Compose instalados
- (Opcional) Make para usar comandos simplificados

### Usando Docker (Recomendado)

#### Desenvolvimento (com auto-reload)

```bash
# Iniciar o projeto
docker-compose up --build

# Ou usando Make
make up-build
```

O auto-reload está **habilitado** - qualquer alteração no código será refletida automaticamente!

#### Produção

```bash
# Usando docker-compose de produção
docker-compose -f docker-compose.prod.yml up --build -d

# Ou usando Make
make prod-up
```

### Usando Make (Comandos Simplificados)

```bash
# Ver todos os comandos disponíveis
make help

# Comandos principais
make build          # Constrói a imagem
make up             # Inicia em desenvolvimento
make down           # Para os containers
make logs           # Mostra os logs
make shell          # Abre shell no container
make test           # Executa todos os testes
make clean          # Limpa tudo
```

### Executando Localmente (sem Docker)

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
cd src
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Acessando a Documentação Swagger

**IMPORTANTE:** Cada padrão tem sua própria documentação Swagger!

- **Overview Principal**: http://localhost:8000/ (lista todos os padrões)
- **Swagger Principal**: http://localhost:8000/docs (mostra apenas overview)

**Swagger de cada padrão:**
- **Strategy**: http://localhost:8000/strategy/docs
- **Template Method**: http://localhost:8000/template-method/docs
- **Observer**: http://localhost:8000/observer/docs
- **State**: http://localhost:8000/state/docs
- **Adapter**: http://localhost:8000/adapter/docs
- **Decorator**: http://localhost:8000/decorator/docs
- **Facade**: http://localhost:8000/facade/docs

### Executando Padrões Individualmente

Cada padrão pode ser executado independentemente:

```bash
# Exemplos (sem dependências)
cd src/behavioral/strategy && python main.py
cd src/behavioral/template_method && python main.py
cd src/behavioral/observer && python main.py
cd src/behavioral/state && python main.py
cd src/structural/adapter && python main.py
cd src/structural/decorator && python main.py
cd src/structural/facade && python main.py

# Testes individuais
make test-state
make test-strategy
make test-observer
make test-template
make test-adapter
make test-decorator
make test-facade
```

## Estrutura do Projeto

```
designpatterns/
├── src/
│   ├── behavioral/           # Padrões comportamentais
│   │   ├── strategy/         # Padrão Strategy
│   │   ├── template_method/  # Padrão Template Method
│   │   ├── observer/         # Padrão Observer
│   │   └── state/            # Padrão State
│   ├── structural/           # Padrões estruturais
│   │   ├── adapter/          # Padrão Adapter
│   │   ├── decorator/        # Padrão Decorator
│   │   └── facade/           # Padrão Facade
│   └── main.py               # Aplicação principal FastAPI
├── requirements.txt
├── Dockerfile
├── docker-compose.yml         # Desenvolvimento (com auto-reload)
├── docker-compose.prod.yml    # Produção (sem auto-reload)
├── Makefile                   # Comandos simplificados
├── .dockerignore
├── .gitignore
└── README.md
```

## Recursos de Cada Padrão

Cada padrão implementado inclui:

✓ **Código fonte** com implementação completa do padrão  
✓ **FastAPI** com endpoints RESTful  
✓ **Pydantic schemas** para validação  
✓ **Testes unitários** com cobertura completa  
✓ **Exemplos práticos** de uso  
✓ **Documentação** detalhada em README  

## Auto-Reload (Hot Reload)

O projeto está configurado com **auto-reload** em modo desenvolvimento:

- ✅ **docker-compose.yml**: Usa `--reload` e `--reload-dir /src`
- ✅ **Volume mount**: `./src:/src` permite alterações em tempo real
- ✅ **Exclusão de cache**: `/src/__pycache__` não é sobrescrito

**Como funciona:**
1. Qualquer alteração em arquivos `.py` dentro de `src/`
2. O Uvicorn detecta automaticamente
3. A aplicação recarrega sem precisar reiniciar o container

## Variáveis de Ambiente

Crie um arquivo `.env` baseado em `.env.example`:

```bash
cp .env.example .env
```

Variáveis disponíveis:
- `PORT`: Porta da aplicação (padrão: 8000)
- `ENVIRONMENT`: Ambiente (development/production)
- `LOG_LEVEL`: Nível de log (INFO, DEBUG, etc.)

## Health Check

O container possui health check configurado:

```bash
# Verificar status
docker-compose ps

# Verificar health
docker inspect design_patterns_api | grep -A 10 Health
```

## Desenvolvimento

### Adicionando um Novo Padrão

1. Crie o diretório em `src/behavioral/` ou `src/structural/`
2. Implemente o padrão seguindo a estrutura existente
3. Crie `main.py` com router FastAPI
4. Adicione o router em `src/main.py`
5. Crie testes em `test_*.py`
6. Atualize este README

### Executando Testes

```bash
# Todos os testes (recomendado)
make test
# ou diretamente
python run_tests.py

# Teste específico
make test-state
make test-strategy
make test-observer
make test-template
make test-adapter
make test-decorator
make test-facade
```

## Produção

Para produção, use `docker-compose.prod.yml`:

- ❌ Sem auto-reload (performance)
- ✅ Múltiplos workers (4 workers)
- ✅ Restart automático
- ✅ Health checks
- ✅ Sem volumes (código copiado no build)

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Referência

Baseado no livro **"Rabiscando Padrões de Projeto"**
