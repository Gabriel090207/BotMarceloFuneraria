import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

db = None


def iniciar_firebase():
    global db

    if not firebase_admin._apps:

        # 🔹 PRIORIDADE 1 — ENV (Render)
        cred_json = os.getenv("FIREBASE_CREDENTIALS")

        if cred_json:
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)

        else:
            # 🔹 PRIORIDADE 2 — ARQUIVO LOCAL
            caminho_arquivo = "firebase_credentials.json"

            if not os.path.exists(caminho_arquivo):
                raise Exception("Arquivo firebase_key.json não encontrado")

            cred = credentials.Certificate(caminho_arquivo)

        firebase_admin.initialize_app(cred)
        db = firestore.client()


def salvar_pedido(dados):
    iniciar_firebase()

    db.collection("pedidos").add(dados)