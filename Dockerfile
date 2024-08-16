# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /src

# Copie os arquivos de dependências
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação
COPY ./src /src

# Comando para rodar a aplicação com reload automático
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
