from typing import List
from app.schemas.item import Item, ItemCreate

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