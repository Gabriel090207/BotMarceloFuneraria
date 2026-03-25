from core.firebase import iniciar_firebase, db


def listar_urnas(tipo=None):

    iniciar_firebase()  # 🔥 garante conexão

    urnas_ref = db.collection("urnas").where("ativo", "==", True).stream()

    urnas = []

    for urna in urnas_ref:
        dados = urna.to_dict()

        # 🔥 filtro por tipo (Simples, Intermediária, Premium)
        if tipo and dados.get("tipo") != tipo.lower():
            continue

        urnas.append({
            "id": urna.id,
            "nome": dados.get("nome"),
            "preco": float(dados.get("preco", 0)),
            "tipo": dados.get("tipo"),
            "imagens": dados.get("imagens", [])
        })

    return urnas