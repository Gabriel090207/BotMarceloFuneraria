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
    _, referencia = db.collection("pedidos").add(dados)
    return referencia.id


def assumir_atendimento_pedido(pedido_id):
    """Assume um pedido existente, preservando a primeira transferência.

    Campo atendimento_transferido ausente equivale a False, sem migração.
    Retorna None; erros de validação, existência e infraestrutura propagam.
    """
    if not isinstance(pedido_id, str):
        raise TypeError("pedido_id deve ser string.")
    if not pedido_id.strip():
        raise ValueError("pedido_id não pode ser vazio.")
    if "/" in pedido_id:
        raise ValueError("pedido_id deve identificar um único documento.")

    referencia = db.collection("pedidos").document(pedido_id)

    @firestore.transactional
    def assumir(transaction):
        snapshot = referencia.get(transaction=transaction)
        if not snapshot.exists:
            raise LookupError("Pedido não encontrado.")
        if snapshot.to_dict().get("atendimento_transferido", False) is True:
            return

        transaction.update(referencia, {
            "atendimento_transferido": True,
            "atendimento_transferido_em": firestore.SERVER_TIMESTAMP,
        })

    assumir(db.transaction())


def buscar_servicos_funerarios():

    docs = db.collection("servicos").stream()

    lista = []

    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        lista.append(item)

    lista.sort(key=lambda x: x.get("nome", ""))

    return lista
