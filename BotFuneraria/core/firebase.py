import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# 🔥 inicializa automático

if not firebase_admin._apps:

    cred_json = os.getenv("FIREBASE_CREDENTIALS")

    if cred_json:
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)

    else:
        caminho_arquivo = "firebase_credentials.json"

        if not os.path.exists(caminho_arquivo):
            raise Exception("Arquivo firebase_credentials.json não encontrado")

        cred = credentials.Certificate(caminho_arquivo)

    firebase_admin.initialize_app(cred)

# 🔥 db sempre pronto
db = firestore.client()


def salvar_pedido(dados):
    db.collection("pedidos").add(dados)


def buscar_servicos_funerarios():

    docs = db.collection("servicos").stream()

    lista = []

    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        lista.append(item)

    lista.sort(key=lambda x: x.get("nome", ""))

    return lista