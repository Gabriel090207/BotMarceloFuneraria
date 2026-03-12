import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred)

db = firestore.client()


def salvar_pedido(dados):

    pedido_ref = db.collection("pedidos").document()

    pedido_ref.set(dados)