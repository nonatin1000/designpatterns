# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Defina variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Defina o diretório de trabalho no contêiner
WORKDIR /src

# Copie os arquivos de dependências
COPY requirements.txt .

# Instale wget para healthcheck e dependências
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação
COPY ./src /src

# Exponha a porta
EXPOSE 8000

# Healthcheck (usando wget que vem na imagem slim)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/ || exit 1

# Comando para rodar a aplicação (sem --reload para produção)
# O --reload será adicionado via docker-compose para desenvolvimento
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
