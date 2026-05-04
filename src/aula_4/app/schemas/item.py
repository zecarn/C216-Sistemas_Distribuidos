from pydantic import BaseModel

class Item(BaseModel):
    id: int
    nome: str
    descricao: str

class ItemCreate(BaseModel):
    nome: str
    descricao: str