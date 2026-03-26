from core.firebase import iniciar_firebase
import core.firebase as fb


def listar_urnas(tipo=None, categoria=None):

    iniciar_firebase()  # 🔥 garante conexão

    db = fb.db  # 🔥 pega o db atualizado

    urnas_ref = db.collection("urnas").where("ativo", "==", True).stream()

    urnas = []

    for urna in urnas_ref:
        dados = urna.to_dict()

        # 🔹 filtro por tipo (simples, premium...)
        if tipo and dados.get("tipo") != tipo:
            continue

        # 🔹 filtro por categoria (sepultamento ou cremacao)
        if categoria and dados.get("categoria") != categoria:
            continue

        urnas.append({
            "id": urna.id,
            "nome": dados.get("nome"),
            "preco": float(dados.get("preco", 0)),
            "tipo": dados.get("tipo"),
            "categoria": dados.get("categoria"),  # 🔥 novo
            "imagens": dados.get("imagens", [])
        })

    return urnas