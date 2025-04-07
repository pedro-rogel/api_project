# Aqui nós pegamos a imagem base do python na versao 3.9
FROM python:3.9-slim 

# Aqui iremos definir uma pasta (diretório) dentro do container
WORKDIR /api_project

# Agora, iremos copiar todos os arquivos da nossa aplicação 
COPY . .

# Iremos rodar o comando para instalar as dependências da aplicação
RUN pip install -r requirements.txt

# Agoro, iremos rodar o comando quando o container iniciar
CMD ["python", "app.py"]

# Aqui, estamos expondo a porta 8080
EXPOSE 8080