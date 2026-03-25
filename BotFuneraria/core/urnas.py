from core.firebase import iniciar_firebase
import core.firebase as fb


def listar_urnas(tipo=None):

    iniciar_firebase()  # 🔥 garante conexão

    db = fb.db  # 🔥 pega o db atualizado

    urnas_ref = db.collection("urnas").where("ativo", "==", True).stream()

    urnas = []

    for urna in urnas_ref:
        dados = urna.to_dict()

        if tipo and dados.get("tipo") != tipo:
            continue

        urnas.append({
            "id": urna.id,
            "nome": dados.get("nome"),
            "preco": float(dados.get("preco", 0)),
            "tipo": dados.get("tipo"),
            "imagens": dados.get("imagens", [])
        })

    return urnas