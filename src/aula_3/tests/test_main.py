from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}


def test_query_param():
    response = client.get("/api/v1/hello?name=Matheus")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Matheus"}


def test_path_param():
    response = client.get("/api/v1/hello/Matheus")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Matheus"}


def test_post():
    response = client.post(
        "/api/v1/hello",
        json={"name": "Matheus"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Matheus"}

def test_post_invalid():
    response = client.post("/api/v1/hello", json={})
    assert response.status_code == 422


def test_put():
    response = client.put(
        "/api/v1/update",
        json={"name": "Matheus"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Recurso atualizado com o nome: Matheus"}


def test_delete():
    response = client.delete("/api/v1/delete?name=Matheus")
    assert response.status_code == 200
    assert response.json() == {"message": "Recurso deletado com o nome: Matheus"}


def test_patch():
    response = client.patch(
        "/api/v1/patch",
        json={"name": "Matheus"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Modificação parcial aplicada ao recurso com o nome: Matheus"}


# --- query param ausente ---

def test_query_param_missing():
    response = client.get("/api/v1/hello")
    assert response.status_code == 422


# --- body inválido (campo obrigatório ausente) ---

def test_put_invalid():
    response = client.put("/api/v1/update", json={})
    assert response.status_code == 422


def test_patch_invalid():
    response = client.patch("/api/v1/patch", json={})
    assert response.status_code == 422


def test_delete_missing_param():
    response = client.delete("/api/v1/delete")
    assert response.status_code == 422


# --- rotas inexistentes ---

def test_not_found():
    response = client.get("/nao-existe")
    assert response.status_code == 404


# --- método HTTP errado ---

def test_wrong_method_on_root():
    response = client.post("/")
    assert response.status_code == 405


# --- nomes com espaço e caracteres especiais ---

def test_path_param_with_spaces():
    response = client.get("/api/v1/hello/João Silva")
    assert response.status_code == 200
    assert "João Silva" in response.json()["message"]


def test_query_param_with_special_chars():
    response = client.get("/api/v1/hello?name=Ana%20Lima")
    assert response.status_code == 200
    assert "Ana Lima" in response.json()["message"]


# --- tipo de conteúdo da resposta ---

def test_response_content_type():
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"