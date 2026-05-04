## Prática 4 - Preparando o Middleware para CRUD

Nesta prática, iremos evoluir uma aplicação simples para uma API estruturada utilizando FastAPI, com foco em operações de **CRUD** e no uso de **middlewares**.

Além disso, iremos preparar a aplicação para execução com **Docker e docker-compose**, além de testar a API utilizando o **TestClient**.

---

### Objetivos

- Implementar CRUD completo com FastAPI
- Estruturar a aplicação em camadas
- Criar e organizar middlewares
- Testar endpoints com TestClient
- Containerizar a aplicação com Docker
- Orquestrar serviços com docker-compose

---

### Estrutura do Projeto

```bash
app/
├── main.py
├── middlewares/
│   ├── logging.py
│   └── custom_header.py
├── routes/
│   └── item_routes.py
├── services/
│   └── item_service.py
├── schemas/
│   └── item.py
tests/
└── test_items.py
Dockerfile
docker-compose.yml
requirements.txt
pytest.ini
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
class ItemService:
    def __init__(self):
        self._items = []
        self._id_counter = 1

    def listar(self) -> List[Item]:
        return self._items

    def buscar_por_id(self, item_id: int) -> Item | None:
        for item in self._items:
            if item.id == item_id:
                return item
        return None

    def criar(self, item_data: ItemCreate) -> Item:
        novo_item = Item(
            id=self._id_counter,
            nome=item_data.nome,
            descricao=item_data.descricao
        )
        self._items.append(novo_item)
        self._id_counter += 1
        return novo_item

    def atualizar(self, item_id: int, item_data: ItemCreate) -> Item | None:
        item = self.buscar_por_id(item_id)
        if item:
            item.nome = item_data.nome
            item.descricao = item_data.descricao
            return item
        return None

    def deletar(self, item_id: int) -> bool:
        item = self.buscar_por_id(item_id)
        if item:
            self._items.remove(item)
            return True
        return False
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

### Testes (com TestClient)

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_item():
    response = client.post("/items", json={
        "nome": "Item Teste",
        "descricao": "Descrição teste"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Item Teste"

def test_listar_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_buscar_item():
    create = client.post("/items", json={
        "nome": "Busca",
        "descricao": "Teste"
    })
    item_id = create.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200

def test_atualizar_item():
    create = client.post("/items", json={
        "nome": "Velho",
        "descricao": "Antigo"
    })
    item_id = create.json()["id"]

    response = client.put(f"/items/{item_id}", json={
        "nome": "Novo",
        "descricao": "Atualizado"
    })

    assert response.status_code == 200
    assert response.json()["nome"] == "Novo"

def test_deletar_item():
    create = client.post("/items", json={
        "nome": "Delete",
        "descricao": "Teste"
    })
    item_id = create.json()["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
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

- CRUD com FastAPI.
- Arquitetura em camadas
- Middleware (interceptação global)
- Testes automatizados com TestClient
- Docker e docker-compose

---

### Exercício Proposto:

1. Implementar o CRUD completo de um **Gerenciador de Alunos** usando FastAPI.
2. O CRUD deve conter as seguintes funcionalidades:
    - `POST /api/v1/alunos/`: Cadastra um novo aluno.
    - `GET /api/v1/alunos/`: Lista todos os alunos.
    - `GET /api/v1/alunos/{aluno_id}`: Busca um aluno pelo ID.
    - `PATCH /api/v1/alunos/{aluno_id}`: Atualiza dados de um aluno.
    - `DELETE /api/v1/alunos/{aluno_id}`: Remove um aluno do sistema.
    - `DELETE /api/v1/alunos/`: Reseta a lista de alunos.
3. Cada aluno deve possuir os seguintes atributos:
   - Nome
   - E-mail
   - Curso (GES, GEC) **Pelo menos 2 cursos**
   - Matrícula (gerada automaticamente com base no curso, ex: 1, 2, 3, etc.)
   - ID (curso + matrícula sequencial por curso, ex: GES1, GES2, GEC1, GEC2, etc.)
     - **OBS**: Se um aluno for deletado, o ID não pode ser reutilizado.
4. Executar a API usando docker-compose (**OBRIGATÓRIO**).
5. Criar testes automatizados de API.
6. Os testes devem conter pelo menos adição de 3 alunos por curso, listagem de alunos, busca por ID, atualização de dados e remoção de alunos.
8. Tirar prints dos resultados e subir na pasta `img/` dentro do repositório.

Prints:
- Resultados dos testes.
- Logs do container contendo as chamadas na API.