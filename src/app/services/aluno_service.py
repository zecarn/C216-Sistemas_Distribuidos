from app.db.connection import get_connection


class AlunoService:

    async def listar(self):
        conn = await get_connection()
        try:
            rows = await conn.fetch("SELECT * FROM alunos ORDER BY curso, matricula")
            return [dict(row) for row in rows]
        finally:
            await conn.close()

    async def buscar_por_id(self, aluno_id: str):
        conn = await get_connection()
        try:
            row = await conn.fetchrow("SELECT * FROM alunos WHERE id=$1", aluno_id)
            return dict(row) if row else None
        finally:
            await conn.close()

    async def criar(self, aluno):
        conn = await get_connection()
        try:
            matricula = await conn.fetchval(
                "UPDATE matricula_sequence SET ultimo = ultimo + 1 WHERE curso=$1 RETURNING ultimo",
                aluno.curso
            )
            aluno_id = f"{aluno.curso}{matricula}"
            row = await conn.fetchrow(
                "INSERT INTO alunos (id, nome, email, matricula, curso) VALUES ($1, $2, $3, $4, $5) RETURNING *",
                aluno_id, aluno.nome, aluno.email, matricula, aluno.curso
            )
            return dict(row)
        finally:
            await conn.close()

    async def atualizar(self, aluno_id: str, aluno):
        conn = await get_connection()
        try:
            atual = await conn.fetchrow("SELECT * FROM alunos WHERE id=$1", aluno_id)
            if not atual:
                return None

            nome = aluno.nome if aluno.nome is not None else atual["nome"]
            email = aluno.email if aluno.email is not None else atual["email"]
            curso = aluno.curso if aluno.curso is not None else atual["curso"]

            novo_id = aluno_id
            matricula = atual["matricula"]
            if curso != atual["curso"]:
                matricula = await conn.fetchval(
                    "UPDATE matricula_sequence SET ultimo = ultimo + 1 WHERE curso=$1 RETURNING ultimo",
                    curso
                )
                novo_id = f"{curso}{matricula}"

            row = await conn.fetchrow(
                """
                UPDATE alunos
                SET id=$1, nome=$2, email=$3, matricula=$4, curso=$5
                WHERE id=$6
                RETURNING *
                """,
                novo_id, nome, email, matricula, curso, aluno_id
            )
            return dict(row) if row else None
        finally:
            await conn.close()

    async def deletar(self, aluno_id: str):
        conn = await get_connection()
        try:
            result = await conn.execute("DELETE FROM alunos WHERE id=$1", aluno_id)
            return result == "DELETE 1"
        finally:
            await conn.close()

    async def resetar(self):
        conn = await get_connection()
        try:
            await conn.execute("DELETE FROM alunos")
            await conn.execute("UPDATE matricula_sequence SET ultimo = 0")
        finally:
            await conn.close()
