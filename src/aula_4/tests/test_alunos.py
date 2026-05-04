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
    alunos_ges = [criar_aluno(f"Aluno GES {i}", "GES") for i in range(1, 4)]
    alunos_gec = [criar_aluno(f"Aluno GEC {i}", "GEC") for i in range(1, 4)]

    assert [response.status_code for response in alunos_ges + alunos_gec] == [201] * 6
    assert [response.json()["id"] for response in alunos_ges] == ["GES1", "GES2", "GES3"]
    assert [response.json()["id"] for response in alunos_gec] == ["GEC1", "GEC2", "GEC3"]
    assert [response.json()["matricula"] for response in alunos_ges] == [1, 2, 3]
    assert [response.json()["matricula"] for response in alunos_gec] == [1, 2, 3]


def test_listar_alunos():
    criar_aluno("Ana Silva", "GES")
    criar_aluno("Bruno Lima", "GEC")

    response = client.get("/api/v1/alunos/")

    assert response.status_code == 200
    assert len(response.json()) == 2


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
