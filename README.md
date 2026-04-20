## Executando o Projeto com Docker

### Pré-requisitos
- Docker instalado e configurado
- Docker Compose (opcional, para múltiplos serviços)

### Passos para Executar

1. **Build da imagem Docker**
    ```bash
    docker build -t sistema_faculdade .
    ```

2. **Executar o container**
    ```bash
    docker run -it sistema_faculdade
    ```

3. **Verificar o status**
    ```bash
    docker ps
    ```

4. **Parar o container**
    ```bash
    docker stop sistema_faculadde
    ```

### Usando Docker Compose (se aplicável)