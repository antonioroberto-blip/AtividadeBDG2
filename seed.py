import random
from datetime import datetime
from faker import Faker
from bson import ObjectId
from conexao import obter_banco
fake = Faker("pt_BR")

CATEGORIAS = ["Programação","Dados","Design","Negócios","Marketing"]
TITULOS = ["Python para Iniciantes","Python para Análise de Dados","Java Básico","JavaScript Moderno","C# para Iniciantes","Banco de Dados","MongoDB na Prática","SQL Completo","HTML e CSS","Desenvolvimento Web","Power BI","Excel Avançado","Introdução à IA","Machine Learning","Gestão de Projetos","Marketing Digital","Redes Sociais","UX Design","UI Design","Photoshop Básico","Empreendedorismo","Finanças Pessoais","Lógica de Programação","Algoritmos","Git e GitHub","React","Node.js","Django","Análise de Negócios","Comunicação Profissional"]

def gerar_modulos():
    quantidade = random.randint(2, 4)
    modulos = []
    for i in range(1, quantidade + 1):
        modulos.append({"ordem": i,"titulo": f"Módulo {i}","aulas": [f"Aula {i}.1",f"Aula {i}.2",f"Aula {i}.3"]})
    return modulos

def criar_cursos(db):
    cursos = []
    for i in range(30):
        cursos.append({"titulo": TITULOS[i],"categoria": random.choice(CATEGORIAS),"carga_horaria": random.choice([10, 20, 30, 40, 60]),"preco": round(random.uniform(49.90, 499.90), 2),"vagas": random.randint(5, 50),"tags": ["iniciante",random.choice(["online", "pratico", "completo"])],"instrutor": {"nome": fake.name(),"email": fake.email()},"modulos": gerar_modulos()})
    resultado = db.cursos.insert_many(cursos)
    print(f"{len(resultado.inserted_ids)} cursos inseridos.")
    return resultado.inserted_ids

def criar_alunos(db):
    alunos = []
    for i in range(10):
        alunos.append({"nome": fake.name(),"email": f"aluno{i + 1}@email.com","data_cadastro": datetime.now()})
    resultado = db.alunos.insert_many(alunos)
    print(f"{len(resultado.inserted_ids)} alunos inseridos.")
    return resultado.inserted_ids

def criar_matriculas(db, alunos_ids, cursos_ids):
    matriculas = []
    pares_usados = set()
    while len(matriculas) < 30:
        aluno_id = random.choice(alunos_ids)
        curso_id = random.choice(cursos_ids)
        par = (str(aluno_id), str(curso_id))
        if par in pares_usados:
            continue
        pares_usados.add(par)
        progresso = random.randint(0, 100)
        concluida = progresso == 100
        matricula = {"aluno_id": aluno_id,"curso_id": curso_id,"data_matricula": datetime.now(),"progresso": progresso,"concluida": concluida}
        if concluida:
            matricula["nota"] = random.randint(1, 5)
        matriculas.append(matricula)
    db.matriculas.insert_many(matriculas)
    print(f"{len(matriculas)} matrículas inseridas.")

def executar_seed():
    db = obter_banco()
    # Idempotência:
    # apaga os dados anteriores antes de inserir novamente.
    db.cursos.delete_many({})
    db.alunos.delete_many({})
    db.matriculas.delete_many({})
    print("Dados antigos removidos.")
    cursos_ids = criar_cursos(db)
    alunos_ids = criar_alunos(db)
    criar_matriculas(db,alunos_ids,cursos_ids)
    print("\nSeed executado com sucesso!")
if __name__ == "__main__":
    executar_seed()