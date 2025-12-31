# Design Patterns

Este projeto é uma API de estudo de design patterns do curso Rabiscando Padrões de Projeto.

## Padrões Implementados

### Padrões Comportamentais (Behavioral)

| Padrão | Descrição | Diretório |
|--------|-----------|-----------|
| **Decorator** | Adiciona responsabilidades a objetos dinamicamente | [src/behavioral/decorator](src/behavioral/decorator) |
| **Observer** | Define dependência um-para-muitos entre objetos | [src/behavioral/observer](src/behavioral/observer) |
| **State** | Permite objeto alterar comportamento quando estado muda | [src/behavioral/state](src/behavioral/state) |
| **Template Method** | Define esqueleto de algoritmo, delegando passos | [src/behavioral/template_method](src/behavioral/template_method) |

### Padrões Estruturais (Structural)

| Padrão | Descrição | Diretório |
|--------|-----------|-----------|
| **Adapter** | Permite interfaces incompatíveis trabalharem juntas | [src/structural/adapter](src/structural/adapter) |
| **Facade** | Fornece interface unificada para subsistema complexo | [src/structural/facade](src/structural/facade) |

## Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno e de alta performance para construir APIs com Python 3.6+ baseado em standard Python type hints.
- **[Docker](https://www.docker.com/)**: Plataforma para desenvolver, enviar e executar aplicações em containers.
- **[Docker Compose](https://docs.docker.com/compose/)**: Ferramenta para definir e executar aplicações multi-container Docker.
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Biblioteca para validação de dados e configurações utilizando type hints.
- **[Python 3.11](https://www.python.org/)**: Linguagem de programação utilizada no desenvolvimento deste projeto.

## Executando o Projeto

### Usando Docker

1. Certifique-se de ter o Docker instalado em sua máquina.
2. Execute o comando abaixo para iniciar o projeto:
   ```bash
   docker-compose up --build
   ```

### Acessando a Documentação Swagger

**IMPORTANTE:** Cada padrão tem sua própria documentação Swagger!

- **Overview Principal**: http://localhost:8000/ (lista todos os padrões)
- **Swagger Principal**: http://localhost:8000/docs (mostra apenas overview)

**Swagger de cada padrão:**
- **Decorator**: http://localhost:8000/decorator/docs
- **Observer**: http://localhost:8000/observer/docs
- **State**: http://localhost:8000/state/docs
- **Adapter**: http://localhost:8000/adapter/docs
- **Facade**: http://localhost:8000/facade/docs

### Executando Padrões Individualmente

Cada padrão pode ser executado independentemente:

```bash
# Exemplos (sem dependências)
cd src/behavioral/decorator && python exemplo.py
cd src/behavioral/observer && python exemplo.py
cd src/behavioral/state && python exemplo.py
cd src/structural/adapter && python exemplo.py
cd src/structural/facade && python exemplo.py

# Testes
cd src/behavioral/decorator && python test_decorator.py
cd src/behavioral/observer && python test_observer.py
cd src/behavioral/state && python test_state.py
cd src/structural/adapter && python test_adapter.py
cd src/structural/facade && python test_facade.py

# APIs individuais
cd src/behavioral/decorator && python main.py
cd src/behavioral/observer && python main.py
cd src/behavioral/state && python main.py
cd src/structural/adapter && python main.py
cd src/structural/facade && python main.py
```

## Estrutura do Projeto

```
designpatterns/
├── src/
│   ├── behavioral/           # Padrões comportamentais
│   │   ├── decorator/        # Padrão Decorator
│   │   ├── observer/         # Padrão Observer
│   │   ├── state/            # Padrão State
│   │   └── template_method/  # Padrão Template Method
│   └── structural/           # Padrões estruturais
│       ├── adapter/          # Padrão Adapter
│       └── facade/           # Padrão Facade
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
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

## Referência

Baseado no livro **"Rabiscando Padrões de Projeto"**
