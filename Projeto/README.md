## Executando o Projeto com Docker

### Pré-requisitos
- Docker instalado e configurado
- Docker Compose (opcional, para múltiplos serviços)

### Passos para Executar

1. **Build da imagem Docker**
    ```bash
    docker build -t nome-do-projeto:latest .
    ```

2. **Executar o container**
    ```bash
    docker run -d --name nome-container -p PORTA_EXTERNA:PORTA_INTERNA nome-do-projeto:latest
    ```

3. **Verificar o status**
    ```bash
    docker ps
    ```

4. **Ver logs**
    ```bash
    docker logs nome-container
    ```

5. **Parar o container**
    ```bash
    docker stop nome-container
    ```

### Usando Docker Compose (se aplicável)