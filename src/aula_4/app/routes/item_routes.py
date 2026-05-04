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