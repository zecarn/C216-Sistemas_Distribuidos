from typing import Literal, Optional

from pydantic import BaseModel


Curso = Literal["GES", "GEC"]


class Aluno(BaseModel):
    id: str
    nome: str
    email: str
    curso: Curso
    matricula: int


class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: Curso


class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    curso: Optional[Curso] = None
