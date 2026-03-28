from core.firebase import db, iniciar_firebase


def listar_pacotes():

    iniciar_firebase()  # 🔥 ESSA LINHA FALTAVA

    docs = db.collection("pacotes").where("ativo", "==", True).stream()

    lista = []

    for d in docs:
        data = d.to_dict() or {}
        data["id"] = d.id
        lista.append(data)

    return lista