from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def setup_function():
    client.delete("/api/v1/alunos/")


def criar_aluno(nome: str, curso: str):
    return client.post(
        "/api/v1/alunos/",
        json={
            "nome": nome,
            "email": f"{nome.lower().replace(' ', '.')}@inatel.br",
            "curso": curso,
        },
    )


def test_adicionar_tres_alunos_por_curso():
    ges1 = client.post("/api/v1/alunos/", json={"nome": "Ana Lima", "email": "ana.lima@inatel.br", "curso": "GES"})
    ges2 = client.post("/api/v1/alunos/", json={"nome": "Bruno Souza", "email": "bruno.souza@inatel.br", "curso": "GES"})
    ges3 = client.post("/api/v1/alunos/", json={"nome": "Carla Mendes", "email": "carla.mendes@inatel.br", "curso": "GES"})

    gec1 = client.post("/api/v1/alunos/", json={"nome": "Diego Rocha", "email": "diego.rocha@inatel.br", "curso": "GEC"})
    gec2 = client.post("/api/v1/alunos/", json={"nome": "Elisa Ferreira", "email": "elisa.ferreira@inatel.br", "curso": "GEC"})
    gec3 = client.post("/api/v1/alunos/", json={"nome": "Felipe Costa", "email": "felipe.costa@inatel.br", "curso": "GEC"})

    assert ges1.status_code == 201
    assert ges1.json() == {"id": "GES1", "nome": "Ana Lima", "email": "ana.lima@inatel.br", "curso": "GES", "matricula": 1}

    assert ges2.status_code == 201
    assert ges2.json() == {"id": "GES2", "nome": "Bruno Souza", "email": "bruno.souza@inatel.br", "curso": "GES", "matricula": 2}

    assert ges3.status_code == 201
    assert ges3.json() == {"id": "GES3", "nome": "Carla Mendes", "email": "carla.mendes@inatel.br", "curso": "GES", "matricula": 3}

    assert gec1.status_code == 201
    assert gec1.json() == {"id": "GEC1", "nome": "Diego Rocha", "email": "diego.rocha@inatel.br", "curso": "GEC", "matricula": 1}

    assert gec2.status_code == 201
    assert gec2.json() == {"id": "GEC2", "nome": "Elisa Ferreira", "email": "elisa.ferreira@inatel.br", "curso": "GEC", "matricula": 2}

    assert gec3.status_code == 201
    assert gec3.json() == {"id": "GEC3", "nome": "Felipe Costa", "email": "felipe.costa@inatel.br", "curso": "GEC", "matricula": 3}


def test_listar_alunos():
    criar_aluno("Ana Lima", "GES")
    criar_aluno("Bruno Souza", "GES")
    criar_aluno("Carla Mendes", "GES")
    criar_aluno("Diego Rocha", "GEC")
    criar_aluno("Elisa Ferreira", "GEC")
    criar_aluno("Felipe Costa", "GEC")

    response = client.get("/api/v1/alunos/")
    alunos = response.json()

    assert response.status_code == 200
    assert len(alunos) == 6
    ids = [a["id"] for a in alunos]
    assert all(i in ids for i in ["GES1", "GES2", "GES3", "GEC1", "GEC2", "GEC3"])


def test_buscar_aluno_por_id():
    create = criar_aluno("Carla Souza", "GES")
    aluno_id = create.json()["id"]

    response = client.get(f"/api/v1/alunos/{aluno_id}")

    assert response.status_code == 200
    assert response.json()["id"] == aluno_id
    assert response.json()["nome"] == "Carla Souza"


def test_atualizar_dados_do_aluno():
    create = criar_aluno("Diego Antigo", "GEC")
    aluno_id = create.json()["id"]

    response = client.patch(
        f"/api/v1/alunos/{aluno_id}",
        json={
            "nome": "Diego Atualizado",
            "email": "diego.atualizado@inatel.br",
        },
    )

    assert response.status_code == 200
    assert response.json()["nome"] == "Diego Atualizado"
    assert response.json()["email"] == "diego.atualizado@inatel.br"
    assert response.json()["id"] == aluno_id


def test_atualizar_curso_gera_nova_matricula_e_id():
    criar_aluno("Aluno GES Existente", "GES")
    create = criar_aluno("Elisa GEC", "GEC")

    response = client.patch(
        f"/api/v1/alunos/{create.json()['id']}",
        json={"curso": "GES"},
    )

    assert response.status_code == 200
    assert response.json()["curso"] == "GES"
    assert response.json()["matricula"] == 2
    assert response.json()["id"] == "GES2"


def test_remover_aluno_sem_reutilizar_id():
    criar_aluno("Eduarda Um", "GES")
    removido = client.delete("/api/v1/alunos/GES1")
    novo = criar_aluno("Eduarda Dois", "GES")

    assert removido.status_code == 200
    assert novo.status_code == 201
    assert novo.json()["id"] == "GES2"


def test_resetar_lista_de_alunos():
    criar_aluno("Fabio GES", "GES")
    criar_aluno("Fabio GEC", "GEC")

    reset = client.delete("/api/v1/alunos/")
    lista = client.get("/api/v1/alunos/")

    assert reset.status_code == 200
    assert lista.status_code == 200
    assert lista.json() == []
