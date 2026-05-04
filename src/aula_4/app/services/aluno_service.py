from typing import Dict, List, Optional

from app.schemas.aluno import Aluno, AlunoCreate, AlunoUpdate, Curso


class AlunoService:
    def __init__(self):
        self._alunos: List[Aluno] = []
        self._matriculas_por_curso: Dict[Curso, int] = {
            "GES": 1,
            "GEC": 1,
        }

    def listar(self) -> List[Aluno]:
        return self._alunos

    def buscar_por_id(self, aluno_id: str) -> Optional[Aluno]:
        for aluno in self._alunos:
            if aluno.id == aluno_id:
                return aluno
        return None

    def criar(self, aluno_data: AlunoCreate) -> Aluno:
        matricula = self._matriculas_por_curso[aluno_data.curso]
        novo_aluno = Aluno(
            id=f"{aluno_data.curso}{matricula}",
            nome=aluno_data.nome,
            email=aluno_data.email,
            curso=aluno_data.curso,
            matricula=matricula,
        )

        self._alunos.append(novo_aluno)
        self._matriculas_por_curso[aluno_data.curso] += 1
        return novo_aluno

    def atualizar(self, aluno_id: str, aluno_data: AlunoUpdate) -> Optional[Aluno]:
        aluno = self.buscar_por_id(aluno_id)
        if not aluno:
            return None

        dados_atualizados = aluno_data.dict(exclude_unset=True)
        novo_curso = dados_atualizados.pop("curso", None)

        if novo_curso and novo_curso != aluno.curso:
            nova_matricula = self._matriculas_por_curso[novo_curso]
            aluno.curso = novo_curso
            aluno.matricula = nova_matricula
            aluno.id = f"{novo_curso}{nova_matricula}"
            self._matriculas_por_curso[novo_curso] += 1

        for campo, valor in dados_atualizados.items():
            setattr(aluno, campo, valor)

        return aluno

    def deletar(self, aluno_id: str) -> bool:
        aluno = self.buscar_por_id(aluno_id)
        if not aluno:
            return False

        self._alunos.remove(aluno)
        return True

    def resetar(self) -> None:
        self._alunos.clear()
        self._matriculas_por_curso = {
            "GES": 1,
            "GEC": 1,
        }
