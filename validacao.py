from conexao import obter_banco

def configurar_validacao():
    db = obter_banco()
    if "cursos" in db.list_collection_names():
        db.cursos.drop()
    db.create_collection("cursos",validator={"$jsonSchema": {"bsonType": "object","required": ["titulo","categoria","preco","vagas","modulos"],"properties": {"titulo": {"bsonType": "string"},"categoria": {"bsonType": "string"},"preco": {"bsonType": ["int", "long", "double", "decimal"],"minimum": 0},"vagas": {"bsonType": ["int", "long"],"minimum": 0},"modulos": {"bsonType": "array"}}}},validationLevel="strict",validationAction="error")
    print("Coleção cursos criada com validação.")
if __name__ == "__main__":
    configurar_validacao()