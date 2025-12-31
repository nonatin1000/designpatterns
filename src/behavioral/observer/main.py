from fastapi import FastAPI, HTTPException
from newsletter import Newsletter
from observers import Cliente, Funcionario, Parceiro, Fornecedor
from schemas import (
    AssinanteCreate,
    AssinanteResponse,
    MensagemCreate,
    MensagemResponse,
    NewsletterStatus,
    CancelarInscricaoRequest,
    OperacaoResponse,
    TipoAssinante
)
from typing import Dict

app = FastAPI(
    title="Newsletter - Padrão Observer",
    description="API de newsletter implementando o padrão de projeto Observer",
    version="1.0.0"
)

# Instância global da newsletter (Subject)
newsletter = Newsletter()

# Dicionário para armazenar referências aos observers por email
observers_registry: Dict[str, object] = {}


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Bem-vindo à Newsletter - Padrão Observer",
        "pattern": "Observer",
        "description": "Define dependência um-para-muitos entre objetos",
        "endpoints": {
            "status": "/status",
            "inscrever": "/assinantes (POST)",
            "cancelar": "/assinantes (DELETE)",
            "publicar": "/mensagens (POST)",
            "docs": "/docs"
        }
    }


@app.get("/status", response_model=NewsletterStatus, tags=["Newsletter"])
async def get_status():
    """
    Retorna o status atual da newsletter.

    Mostra o total de assinantes, mensagens publicadas e
    lista todos os assinantes registrados.
    """
    return NewsletterStatus(
        total_assinantes=newsletter.get_total_assinantes(),
        total_mensagens=len(newsletter.get_mensagens()),
        assinantes=newsletter.get_assinantes()
    )


@app.post("/assinantes", response_model=AssinanteResponse, tags=["Assinantes"])
async def inscrever_assinante(assinante: AssinanteCreate):
    """
    Inscreve um novo assinante na newsletter.

    O padrão Observer permite que novos observers (assinantes) sejam
    adicionados dinamicamente ao Subject (newsletter). Quando o Subject
    muda de estado (nova mensagem), todos os observers são notificados
    automaticamente.

    Tipos de assinantes:
    - cliente: Cliente da empresa
    - funcionario: Funcionário
    - parceiro: Parceiro de negócios
    - fornecedor: Fornecedor

    Returns:
        Dados do assinante inscrito
    """
    # Verifica se já existe assinante com esse email
    if assinante.email in observers_registry:
        raise HTTPException(
            status_code=400,
            detail=f"Email {assinante.email} já está inscrito na newsletter"
        )

    try:
        # Cria o observer apropriado baseado no tipo
        observer_classes = {
            TipoAssinante.CLIENTE: Cliente,
            TipoAssinante.FUNCIONARIO: Funcionario,
            TipoAssinante.PARCEIRO: Parceiro,
            TipoAssinante.FORNECEDOR: Fornecedor
        }

        ObserverClass = observer_classes[assinante.tipo]
        observer = ObserverClass(assinante.nome, assinante.email, newsletter)

        # Armazena referência ao observer
        observers_registry[assinante.email] = observer

        return AssinanteResponse(
            nome=assinante.nome,
            email=assinante.email,
            tipo=assinante.tipo.value
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao inscrever assinante: {str(e)}"
        )


@app.delete("/assinantes", response_model=OperacaoResponse, tags=["Assinantes"])
async def cancelar_inscricao(request: CancelarInscricaoRequest):
    """
    Cancela a inscrição de um assinante.

    Remove o observer da lista de notificações do Subject.
    Demonstra a flexibilidade do padrão Observer em remover
    observers dinamicamente.
    """
    if request.email not in observers_registry:
        raise HTTPException(
            status_code=404,
            detail=f"Email {request.email} não encontrado na lista de assinantes"
        )

    try:
        observer = observers_registry[request.email]
        observer.cancelar_inscricao()
        del observers_registry[request.email]

        return OperacaoResponse(
            sucesso=True,
            mensagem=f"Inscrição de {request.email} cancelada com sucesso"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao cancelar inscrição: {str(e)}"
        )


@app.post("/mensagens", response_model=MensagemResponse, tags=["Mensagens"])
async def publicar_mensagem(mensagem: MensagemCreate):
    """
    Publica uma nova mensagem na newsletter.

    Quando uma mensagem é publicada, o Subject (newsletter) notifica
    automaticamente todos os observers registrados. Este é o núcleo
    do padrão Observer: mudança de estado no Subject -> notificação
    automática de todos os observers.

    Fluxo:
    1. Newsletter recebe nova mensagem
    2. Newsletter.notify_observers() é chamado
    3. Cada observer.update() é executado
    4. Observers processam a notificação (enviam email)
    """
    try:
        # Adiciona mensagem e notifica observers
        newsletter.add_mensagem(mensagem.conteudo)

        assinantes = newsletter.get_assinantes()
        nomes_assinantes = [a["nome"] for a in assinantes]

        return MensagemResponse(
            mensagem=mensagem.conteudo,
            total_notificados=len(assinantes),
            assinantes_notificados=nomes_assinantes
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao publicar mensagem: {str(e)}"
        )


@app.get("/mensagens", tags=["Mensagens"])
async def listar_mensagens():
    """
    Lista todas as mensagens publicadas na newsletter.
    """
    mensagens = newsletter.get_mensagens()
    return {
        "total": len(mensagens),
        "mensagens": mensagens
    }


@app.get("/assinantes", tags=["Assinantes"])
async def listar_assinantes():
    """
    Lista todos os assinantes da newsletter.
    """
    assinantes = newsletter.get_assinantes()
    return {
        "total": len(assinantes),
        "assinantes": assinantes
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
