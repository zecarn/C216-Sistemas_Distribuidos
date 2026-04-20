from services import criar_aluno, listar_alunos, buscar_aluno, atualizar_aluno, deletar_aluno, CURSOS_VALIDOS


def menu():
    print("\n=== Sistema de Alunos INATEL ===")
    print("1. Cadastrar aluno")
    print("2. Listar alunos")
    print("3. Buscar aluno")
    print("4. Atualizar aluno")
    print("5. Deletar aluno")
    print("0. Sair")
    return input("Escolha uma opção: ").strip()


def opcao_cadastrar():
    print("\n--- Cadastrar Aluno ---")
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    print(f"Cursos disponíveis: {', '.join(CURSOS_VALIDOS)}")
    curso = input("Curso: ").strip().upper()
    try:
        aluno = criar_aluno(nome, email, curso)
        print(f"Aluno cadastrado com sucesso! Matrícula: {aluno.matricula}")
    except ValueError as e:
        print(f"Erro: {e}")


def opcao_listar():
    print("\n--- Lista de Alunos ---")
    try:
        listar_alunos()
    except ValueError as e:
        print(e)


def opcao_buscar():
    print("\n--- Buscar Aluno ---")
    matricula = input("Matrícula: ").strip()
    try:
        aluno = buscar_aluno(matricula)
        print(f"\nMatrícula : {aluno.matricula}")
        print(f"Nome      : {aluno.nome}")
        print(f"Email     : {aluno.email}")
        print(f"Curso     : {aluno.curso}")
    except ValueError as e:
        print(e)


def opcao_atualizar():
    print("\n--- Atualizar Aluno ---")
    matricula = input("Matrícula do aluno a atualizar: ").strip()
    try:
        aluno = buscar_aluno(matricula)
        print("Deixe em branco para manter o valor atual.")
        nome = input(f"Nome [{aluno.nome}]: ").strip()
        email = input(f"Email [{aluno.email}]: ").strip()
        print(f"Cursos disponíveis: {', '.join(CURSOS_VALIDOS)}")
        curso = input(f"Curso [{aluno.curso}]: ").strip().upper()
        atualizar_aluno(matricula, nome, email, curso)
        print("Aluno atualizado com sucesso!")
    except ValueError as e:
        print(f"Erro: {e}")


def opcao_deletar():
    print("\n--- Deletar Aluno ---")
    matricula = input("Matrícula do aluno a deletar: ").strip()
    try:
        deletar_aluno(matricula)
        print("Aluno deletado com sucesso!")
    except ValueError as e:
        print(e)


def main():
    opcoes = {
        "1": opcao_cadastrar,
        "2": opcao_listar,
        "3": opcao_buscar,
        "4": opcao_atualizar,
        "5": opcao_deletar,
    }

    while True:
        opcao = menu()
        if opcao == "0":
            print("Saindo... Até logo!")
            break
        elif opcao in opcoes:
            opcoes[opcao]()
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
