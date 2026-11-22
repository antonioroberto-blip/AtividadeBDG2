from bson import ObjectId
from conexao import obter_banco

def buscar_cursos(categoria=None, preco_max=None, tag=None):
    db = obter_banco()
    filtro = {}
    if categoria:
        filtro["categoria"] = categoria
    if preco_max is not None:
        filtro["preco"] = {"$lte": preco_max}
    if tag:
        filtro["tags"] = tag
    cursos = db.cursos.find(filtro,{"modulos": 0})
    return list(cursos)

def adicionar_modulo(curso_id, modulo):
    db = obter_banco()
    resultado = db.cursos.update_one(
        {"_id": ObjectId(curso_id)},
        {"$push": {"modulos": modulo}})
    return resultado.modified_count > 0

def atualizar_progresso(matricula_id, progresso):
    db = obter_banco()
    if progresso < 0 or progresso > 100:
        raise ValueError("O progresso deve estar entre 0 e 100.")
    resultado = db.matriculas.update_one({"_id": ObjectId(matricula_id)},{"$set": {"progresso": progresso,"concluida": progresso == 100}})
    return resultado.modified_count > 0

def remover_aluno(aluno_id):
    db = obter_banco()
    aluno = db.alunos.delete_one({"_id": ObjectId(aluno_id)})
    matriculas = db.matriculas.delete_many({"aluno_id": ObjectId(aluno_id)})
    return aluno.deleted_count, matriculas.deleted_count