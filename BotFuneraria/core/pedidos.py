import json
import os

ARQUIVO_PEDIDOS = "pedidos.json"


def carregar_pedidos():

    if not os.path.exists(ARQUIVO_PEDIDOS):
        return []

    with open(ARQUIVO_PEDIDOS, "r") as f:
        return json.load(f)


def salvar_pedidos(lista):

    with open(ARQUIVO_PEDIDOS, "w") as f:
        json.dump(lista, f, indent=4)


def registrar_pedido(session, numero):

    pedidos = carregar_pedidos()

    carrinho = session.get("carrinho", {})
    dados = session.get("dados", {})

    pedido = {
        "cliente": dados.get("nome", "Cliente"),
        "telefone": numero,
        "itens": carrinho.get("itens", []),
        "total": carrinho.get("total", 0),
        "endereco": dados.get("endereco", ""),
    }

    pedidos.append(pedido)

    salvar_pedidos(pedidos)

    return pedido