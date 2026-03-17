from core.firebase import db


def listar_urnas():

    urnas_ref = db.collection("urnas").where("ativo", "==", True).stream()

    urnas = []

    for urna in urnas_ref:
        dados = urna.to_dict()
        dados["id"] = urna.id
        urnas.append(dados)

    return urnas