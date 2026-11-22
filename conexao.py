import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

def obter_banco():
    uri = os.getenv("MONGO_URI")
    nome_banco = os.getenv("MONGO_DB")
    if not uri or not nome_banco:
        raise Exception("MONGO_URI ou MONGO_DB não configurados.")
    cliente = MongoClient(uri)
    return cliente[nome_banco]