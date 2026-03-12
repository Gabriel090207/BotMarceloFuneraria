# Tabelas de preço (depois podemos mover para banco ou json)

PRECO_SERVICO = {
    "Sepultamento": 2500,
    "Cremação": 3500
}

PRECO_PESO = {
    "Até 80kg": 0,
    "80kg até 120kg": 300,
    "Acima de 120kg": 700
}

PRECO_URNA = {
    "Simples": 500,
    "Intermediária": 900,
    "Premium": 1500
}

PRECO_VELORIO = {
    "Sim": 800,
    "Não": 0
}

PRECO_TRANSLADO = {
    "Sim": 600,
    "Não": 0
}


def calcular_funeraria(dados):

    total = 0

    total += PRECO_SERVICO.get(dados["tipo_servico"], 0)
    total += PRECO_PESO.get(dados["porte_corpo"], 0)
    total += PRECO_URNA.get(dados["tipo_urna"], 0)
    total += PRECO_VELORIO.get(dados["velorio"], 0)
    total += PRECO_TRANSLADO.get(dados["translado"], 0)

    sinal = total * 0.10

    return {
        "total": total,
        "sinal": sinal
    }

def criar_carrinho(session):

    if "carrinho" not in session:

        session["carrinho"] = {
            "itens": [],
            "total": 0
        }

    return session["carrinho"]

def adicionar_item_carrinho(session, produto):

    carrinho = criar_carrinho(session)

    carrinho["itens"].append(produto)

    carrinho["total"] += produto["preco"]

def resumo_carrinho(session):

    carrinho = criar_carrinho(session)

    if not carrinho["itens"]:
        return "Carrinho vazio."

    texto = "🛒 Seu pedido:\n\n"

    for item in carrinho["itens"]:

        texto += f"{item['nome']} - R$ {item['preco']}\n"

    texto += f"\nTotal: R$ {carrinho['total']:.2f}"

    return texto