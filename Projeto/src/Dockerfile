# Define a imagem base
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /aula_1

# Copia um arquivo para o diretório de trabalho no container
#COPY main.py services.py ./

# Copia todos os arquivos do diretório app para o diretório de trabalho no container
COPY ./aula_1 .

# Define o comando de execução ao iniciar o container
CMD ["python", "main.py"]
