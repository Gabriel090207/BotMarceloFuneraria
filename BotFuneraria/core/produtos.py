BASE_IMAGENS = "https://floriculturavalledasflores.com.br"


produtos = [

# -------------------------
# BUQUES
# -------------------------

{
"id":45,
"nome":"Felizes Para Sempre",
"preco":229.99,
"categoria":"buques",
"imagem":"/buqueprincipal4.png"
},

{
"id":46,
"nome":"Quatro Estações",
"preco":99.99,
"categoria":"buques",
"imagem":"/buqueprincipal5.png"
},

{
"id":47,
"nome":"Três Corações",
"preco":89.99,
"categoria":"buques",
"imagem":"/buqueprincipal1.png"
},

{
"id":48,
"nome":"Minha Paixão",
"preco":149.99,
"categoria":"buques",
"imagem":"/buqueprincipal2.png"
},

{
"id":49,
"nome":"Eterno Amor",
"preco":199.99,
"categoria":"buques",
"imagem":"/buqueprincipal3.png"
},

# -------------------------
# ARRANJOS
# -------------------------

{
"id":60,
"nome":"O Transbordar do Amor",
"preco":239.99,
"categoria":"arranjos",
"imagem":"/arranjo3.png"
},

{
"id":50,
"nome":"Coração Apaixonado",
"preco":439.99,
"categoria":"arranjos",
"imagem":"/arranjo4.png"
},

# -------------------------
# COROAS
# -------------------------

{
"id":11,
"nome":"Coroa de Rosas",
"preco":400.00,
"categoria":"coroa_rosas",
"imagem":"/coroa1.png"
},

{
"id":21,
"nome":"Coroa de Flores do Campo",
"preco":370.00,
"categoria":"coroa_campo",
"imagem":"/coroa11.png"
},

# -------------------------
# COMBOS
# -------------------------

{
"id":31,
"nome":"Combo Beijinho de Natal",
"preco":119.00,
"categoria":"combos",
"imagem":"/combo1.png"
},

{
"id":35,
"nome":"Combo Doce Afago",
"preco":169.99,
"categoria":"combos",
"imagem":"/combo5.png"
},

]


# -------------------------
# GERAR URL COMPLETA IMAGEM
# -------------------------

def url_imagem(produto):

    return BASE_IMAGENS + produto["imagem"]


# -------------------------
# PRODUTOS POR CATEGORIA
# -------------------------

def produtos_por_categoria(categoria):

    lista = []

    for p in produtos:

        if p["categoria"] == categoria:
            lista.append(p)

    return lista


# -------------------------
# MENU DE PRODUTOS
# -------------------------

def menu_produtos(categoria):

    lista = produtos_por_categoria(categoria)

    if not lista:
        return "Nenhum produto encontrado."

    texto = "🌸 Escolha um produto:\n\n"

    for i, p in enumerate(lista, start=1):

        texto += f"{i} - {p['nome']}\n"
        texto += f"💰 R$ {p['preco']}\n\n"

    return texto


# -------------------------
# PRODUTO POR INDICE
# -------------------------

def produto_por_indice(categoria, indice):

    lista = produtos_por_categoria(categoria)

    try:
        return lista[int(indice) - 1]

    except:

        return None


def mensagem_produto(produto):

    texto = f"""
🌸 {produto['nome']}

💰 Preço: R$ {produto['preco']}
"""

    imagem = url_imagem(produto)

    return {
        "texto": texto,
        "imagem": imagem
    }