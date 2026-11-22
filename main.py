from bson import ObjectId
from conexao import obter_banco
from repositorio import (buscar_cursos,adicionar_modulo,atualizar_progresso,remover_aluno)

def mostrar_cursos():
    cursos = buscar_cursos()
    print("\n===== CURSOS =====")
    for curso in cursos:
        print(f"ID: {curso['_id']}\n"f"Título: {curso['titulo']}\n"f"Categoria: {curso['categoria']}\n"f"Preço: R$ {curso['preco']:.2f}\n"f"Vagas: {curso['vagas']}\n"f"Tags: {', '.join(curso['tags'])}\n""--------------------------")

def buscar():
    categoria = input("Categoria (Enter para ignorar): ")
    preco = input("Preço máximo (Enter para ignorar): ")
    tag = input("Tag (Enter para ignorar): ")
    preco_max = float(preco) if preco else None
    cursos = buscar_cursos(categoria=categoria or None,preco_max=preco_max,tag=tag or None)
    print("\n===== RESULTADO =====")
    for curso in cursos:
        print(f"{curso['_id']} - "f"{curso['titulo']} - "f"R$ {curso['preco']:.2f}")

def matricular():
    db = obter_banco()
    aluno_id = input("ID do aluno: ")
    curso_id = input("ID do curso: ")
    aluno = db.alunos.find_one({"_id": ObjectId(aluno_id)})
    curso = db.cursos.find_one({"_id": ObjectId(curso_id)})
    if not aluno:
        print("Aluno não encontrado.")
        return
    if not curso:
        print("Curso não encontrado.")
        return
    if curso["vagas"] <= 0:
        print("Curso sem vagas.")
        return
    existente = db.matriculas.find_one({"aluno_id": ObjectId(aluno_id),"curso_id": ObjectId(curso_id)})
    if existente:
        print("Aluno já está matriculado neste curso.")
        return
    db.matriculas.insert_one({"aluno_id": ObjectId(aluno_id),"curso_id": ObjectId(curso_id),"data_matricula": __import__("datetime").datetime.now(),"progresso": 0,"concluida": False})
    db.cursos.update_one({"_id": ObjectId(curso_id)},{"$inc": {"vagas": -1}})
    print("Matrícula realizada com sucesso.")

def atualizar():
    matricula_id = input("ID da matrícula: ")
    progresso = int(input("Novo progresso (0-100): "))
    try:
        sucesso = atualizar_progresso(matricula_id,progresso)
        if sucesso:
            print("Progresso atualizado.")
        else:
            print("Matrícula não encontrada.")
    except ValueError as erro:
        print(erro)

def avaliar():
    db = obter_banco()
    matricula_id = input("ID da matrícula: ")
    nota = int(input("Nota de 1 a 5: "))
    if nota < 1 or nota > 5:
        print("Nota inválida.")
        return
    matricula = db.matriculas.find_one({"_id": ObjectId(matricula_id)})
    if not matricula:
        print("Matrícula não encontrada.")
        return
    if matricula.get("progresso") != 100:
        print("O curso ainda não foi concluído.")
        return
    db.matriculas.update_one({"_id": ObjectId(matricula_id)},{"$set": {"nota": nota}})
    print("Avaliação registrada.")

def relatorios():
    db = obter_banco()
    print("\n===== RELATÓRIOS =====")
    print("\n1. Cursos por categoria:")
    pipeline = [{"$group": {"_id": "$categoria","quantidade": {"$sum": 1}}},{"$sort": {"quantidade": -1}}]
    for item in db.cursos.aggregate(pipeline):
        print(f"{item['_id']}: "f"{item['quantidade']} cursos")
    print("\n2. Total de alunos:")
    print(db.alunos.count_documents({}))
    print("\n3. Total de matrículas:")
    print(db.matriculas.count_documents({}))
    print("\n4. Matrículas concluídas:")
    print(db.matriculas.count_documents({"concluida": True}))

def excluir_aluno():
    aluno_id = input("ID do aluno: ")
    try:
        aluno, matriculas = remover_aluno(aluno_id)
        print(f"Aluno removido: {aluno}\n"f"Matrículas removidas: {matriculas}")
    except Exception:
        print("ID inválido.")

def menu():
    while True:
        print("""
=================================
      APRENDA+ - MONGODB
=================================

1 - Buscar cursos
2 - Exibir cursos
3 - Matricular aluno
4 - Atualizar progresso
5 - Avaliar curso
6 - Relatórios
7 - Remover aluno
0 - Sair
""")

        opcao = input("Escolha: ")
        if opcao == "1":
            buscar()
        elif opcao == "2":
            mostrar_cursos()
        elif opcao == "3":
            matricular()
        elif opcao == "4":
            atualizar()
        elif opcao == "5":
            avaliar()
        elif opcao == "6":
            relatorios()
        elif opcao == "7":
            excluir_aluno()
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()