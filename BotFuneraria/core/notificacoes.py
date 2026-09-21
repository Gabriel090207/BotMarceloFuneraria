from copy import deepcopy


def criar_notificacao(
    tipo,
    titulo,
    *,
    telefone_cliente=None,
    nome_cliente=None,
    fluxo=None,
    etapa=None,
    origem=None,
    dados=None,
    evento_id=None,
    pedido_id=None,
):
    """Cria uma ocorrência em notificacoes com ID automático e retorna o ID.

    Persiste somente os argumentos recebidos, sem consultar sessões.
    Opcionais textuais ausentes são null; dados ausentes resultam em {}.
    evento_id é omitido quando None e não efetua deduplicação.
    pedido_id é omitido quando None; quando informado, deve ser string não vazia.
    Erros de validação e de infraestrutura são propagados ao chamador.
    """
    for campo, valor in (("tipo", tipo), ("titulo", titulo)):
        if not isinstance(valor, str):
            raise TypeError(f"{campo} deve ser string.")
        if not valor.strip():
            raise ValueError(f"{campo} não pode ser vazio.")

    opcionais = {
        "telefone_cliente": telefone_cliente,
        "nome_cliente": nome_cliente,
        "fluxo": fluxo,
        "etapa": etapa,
        "origem": origem,
    }
    for campo, valor in (*opcionais.items(), ("evento_id", evento_id)):
        if valor is not None and not isinstance(valor, str):
            raise TypeError(f"{campo} deve ser string ou None.")

    if dados is not None and not isinstance(dados, dict):
        raise TypeError("dados deve ser dicionário ou None.")

    if pedido_id is not None:
        if not isinstance(pedido_id, str):
            raise TypeError("pedido_id deve ser string ou None.")
        if not pedido_id.strip():
            raise ValueError("pedido_id não pode ser vazio.")

    documento = {
        "tipo": tipo,
        "titulo": titulo,
        **opcionais,
        "dados": deepcopy(dados) if dados is not None else {},
        "lida": False,
        "lida_em": None,
    }
    if evento_id is not None:
        documento["evento_id"] = evento_id
    if pedido_id is not None:
        documento["pedido_id"] = pedido_id

    from core.firebase import db, firestore

    documento["criado_em"] = firestore.SERVER_TIMESTAMP
    _, referencia = db.collection("notificacoes").add(documento)
    return referencia.id
