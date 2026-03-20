CURSOS_VALIDOS = ["GES", "GEC", "GET", "GEP"]

alunos = {}
contadores = {}


class AlunoInatel:
    def __init__(self, nome, email, curso, matricula):
        self.nome = nome
        self.email = email
        self.curso = curso
        self.matricula = matricula


def gerar_matricula(curso):
    contadores[curso] = contadores.get(curso, 0) + 1
    return f"{curso}{contadores[curso]}"


def criar_aluno(nome, email, curso):
    if curso not in CURSOS_VALIDOS:
        raise ValueError(f"Curso inválido. Cursos disponíveis: {', '.join(CURSOS_VALIDOS)}")
    matricula = gerar_matricula(curso)
    aluno = AlunoInatel(nome, email, curso, matricula)
    alunos[matricula] = aluno
    return aluno


def listar_alunos():
    if not alunos:
        raise ValueError("Nenhum aluno cadastrado.")
    print(f"\n{'Matrícula':<10} {'Nome':<30} {'Email':<35} {'Curso'}")
    print("-" * 85)
    for aluno in alunos.values():
        print(f"{aluno.matricula:<10} {aluno.nome:<30} {aluno.email:<35} {aluno.curso}")


def buscar_aluno(matricula):
    aluno = alunos.get(matricula.upper())
    if aluno is None:
        raise ValueError("Aluno não encontrado.")
    return aluno


def atualizar_aluno(matricula, nome, email, curso):
    aluno = buscar_aluno(matricula)  # já lança ValueError se não encontrado
    if curso and curso not in CURSOS_VALIDOS:
        raise ValueError(f"Curso inválido. Cursos disponíveis: {', '.join(CURSOS_VALIDOS)}")
    if nome:
        aluno.nome = nome
    if email:
        aluno.email = email
    if curso:
        aluno.curso = curso


def deletar_aluno(matricula):
    matricula = matricula.upper()
    if matricula not in alunos:
        raise ValueError("Aluno não encontrado.")
    del alunos[matricula]
