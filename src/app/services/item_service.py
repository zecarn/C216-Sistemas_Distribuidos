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