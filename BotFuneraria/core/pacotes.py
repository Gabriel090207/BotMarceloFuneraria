from core.firebase import db

def listar_pacotes():

    docs = db.collection("pacotes").where("ativo", "==", True).stream()

    lista = []

    for d in docs:
        data = d.to_dict() or {}
        data["id"] = d.id
        lista.append(data)

    return lista