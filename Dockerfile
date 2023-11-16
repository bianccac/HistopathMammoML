# Use a imagem base do Python
FROM python:3.9

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Copia todos os arquivos do diretório local para o contêiner
COPY . .

# Comando para executar o aplicativo Flask
CMD ["python", "app.py"]

