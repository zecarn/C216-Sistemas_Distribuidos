### Prática 5 - Persistência com PostgreSQL (FastAPI + asyncpg)

Nesta prática, iremos evoluir a API de itens desenvolvida na prática 4a, substituindo o armazenamento em memória por **persistência real utilizando PostgreSQL**.

Além disso, iremos manter:

- Arquitetura em camadas (routes, services, schemas)
- Middlewares organizados
- Testes automatizados com TestClient
- Execução via docker-compose com múltiplos serviços

---

### Objetivos

- Integrar FastAPI com PostgreSQL
- Utilizar `asyncpg` para acesso assíncrono ao banco
- Persistir dados de forma real
- Manter organização do projeto
- Executar API + banco com docker-compose
- Testar endpoints com TestClient

---

### Estrutura do Projeto

```bash
app/
├── db/
│   ├── connection.py
│   └── init.sql
├── middlewares/
├── routes/
├── services/
├── schemas/
├── main.py
tests/
Dockerfile
docker-compose.yml
requirements.txt
pytest.ini
```

---

### Script SQL

```python
DROP TABLE IF EXISTS items;

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL
);
```

---

### Conexão com o DB

```python
import asyncpg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/items_db"
)

async def get_connection():
    return await asyncpg.connect(DATABASE_URL)
```

---

### Schema

```python
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    nome: str
    descricao: str

class ItemCreate(BaseModel):
    nome: str
    descricao: str
```

---

### Service

```python
from app.db.connection import get_connection

class ItemService:

    async def listar(self):
        conn = await get_connection()
        try:
            rows = await conn.fetch("SELECT * FROM items ORDER BY id")
            return [dict(row) for row in rows]
        finally:
            await conn.close()

    async def buscar_por_id(self, item_id: int):
        conn = await get_connection()
        try:
            row = await conn.fetchrow(
                "SELECT * FROM items WHERE id=$1", item_id
            )
            return dict(row) if row else None
        finally:
            await conn.close()

    async def criar(self, item):
        conn = await get_connection()
        try:
            row = await conn.fetchrow(
                "INSERT INTO items (nome, descricao) VALUES ($1, $2) RETURNING *",
                item.nome, item.descricao
            )
            return dict(row)
        finally:
            await conn.close()

    async def atualizar(self, item_id, item):
        conn = await get_connection()
        try:
            row = await conn.fetchrow(
                """
                UPDATE items
                SET nome=$1, descricao=$2
                WHERE id=$3
                RETURNING *
                """,
                item.nome, item.descricao, item_id
            )
            return dict(row) if row else None
        finally:
            await conn.close()

    async def deletar(self, item_id):
        conn = await get_connection()
        try:
            result = await conn.execute(
                "DELETE FROM items WHERE id=$1", item_id
            )
            return result == "DELETE 1"
        finally:
            await conn.close()
```

---

### Routes

```python
from fastapi import APIRouter, HTTPException
from app.schemas.item import Item, ItemCreate
from app.services.item_service import ItemService

router = APIRouter()
service = ItemService()

@router.get("/items", response_model=list[Item])
def listar_items():
    return service.listar()

@router.get("/items/{item_id}", response_model=Item)
def buscar_item(item_id: int):
    item = service.buscar_por_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

@router.post("/items", response_model=Item)
def criar_item(item: ItemCreate):
    return service.criar(item)

@router.put("/items/{item_id}", response_model=Item)
def atualizar_item(item_id: int, item: ItemCreate):
    atualizado = service.atualizar(item_id, item)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return atualizado

@router.delete("/items/{item_id}")
def deletar_item(item_id: int):
    sucesso = service.deletar(item_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"mensagem": "Item deletado com sucesso"}
```

---

### Middleware

logging.py
```python
from fastapi import Request
import time

async def log_requests(request: Request, call_next):
    inicio = time.time()

    print(f"➡️ {request.method} {request.url}")

    response = await call_next(request)

    duracao = time.time() - inicio
    print(f"⬅️ {response.status_code} - {duracao:.4f}s")

    return response
```

custom_header.py
```python
from fastapi import Request

async def add_custom_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Version"] = "1.0"
    return response
```

---

### Main

```python
from fastapi import FastAPI

from app.routes.item_routes import router as item_router
from app.middlewares.logging import log_requests
from app.middlewares.custom_header import add_custom_header

app = FastAPI(
    title="Middleware CRUD API",
    description="API para estudo de middleware e operações CRUD com FastAPI",
    version="1.0.0"
)

app.middleware("http")(log_requests)
app.middleware("http")(add_custom_header)

app.include_router(item_router)

@app.get("/")
def root():
    return {"mensagem": "API funcionando 🚀"}
```

---

### Execução

```bash
docker compose up --build
```

ou só os testes:
```bash
docker compose run tests
```

---

### Conceitos Trabalhados

- Persistência com PostgreSQL
- Acesso assíncrono com asyncpg
- Arquitetura em camadas
- Middleware aplicado ao banco
- docker-compose com múltiplos serviços

---

### Exercício Proposto:

1. Adaptar sua API para PostgreSQL.
2. Criar testes automatizados de API.
3. Os testes devem conter pelo menos adição de 3 alunos por curso, listagem de alunos, busca por ID, atualização de dados e remoção de alunos.
4. Validar persistência dos dados.
5. Tirar prints dos resultados e subir na pasta `img/` dentro do repositório.

Prints:
- Resultados dos testes.
- Logs do container contendo as chamadas na API.