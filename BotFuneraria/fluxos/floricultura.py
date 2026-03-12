from core.produtos import menu_produtos, produto_por_indice, mensagem_produto
from core.calculos import adicionar_item_carrinho, resumo_carrinho
from core.menus import criar_menu


def fluxo_floricultura(session, mensagem):

    if "etapa" not in session:
        session["etapa"] = "inicio"

    if "dados" not in session:
        session["dados"] = {}

    # -------------------------
    # INICIO
    # -------------------------

    if session["etapa"] == "inicio":

        session["etapa"] = "menu"

        return criar_menu(
            "🌸 Floricultura Marcelo\nEscolha uma opção:",
            [
                ("1", "Ver produtos"),
                ("2", "Ir para o site"),
                ("3", "Pedido personalizado"),
                ("4", "Falar com atendente"),
            ],
        )

    # -------------------------
    # MENU
    # -------------------------

    if session["etapa"] == "menu":

        if mensagem == "1":

            session["etapa"] = "categoria"

            return criar_menu(
                "🌹 Escolha uma categoria",
                [
                    ("1", "Buquês"),
                    ("2", "Arranjos"),
                    ("3", "Coroas de Rosas"),
                    ("4", "Coroas de Flores do Campo"),
                    ("5", "Combos"),
                ],
            )

        elif mensagem == "2":

            return "🌐 Acesse nosso site: https://floriculturavalledasflores.com.br"

        elif mensagem == "3":

            session["etapa"] = "personalizado"

            return """
✏️ Descreva como você deseja o arranjo personalizado.

Nosso atendente irá analisar e responder você.
"""

        elif mensagem == "4":

            session["fluxo"] = "atendente"
            session["etapa"] = "inicio"

            from fluxos.atendente import fluxo_atendente

            return fluxo_atendente(session, mensagem)

        else:

            return "Escolha uma opção válida."

    # -------------------------
    # CATEGORIA
    # -------------------------

    if session["etapa"] == "categoria":

        categorias = {
            "1": "buques",
            "2": "arranjos",
            "3": "coroa_rosas",
            "4": "coroa_campo",
            "5": "combos",
        }

        if mensagem not in categorias:
            return "Escolha uma categoria válida."

        categoria = categorias[mensagem]

        session["dados"]["categoria"] = categoria
        session["etapa"] = "produto"

        return menu_produtos(categoria)

    # -------------------------
    # PRODUTO
    # -------------------------

    if session["etapa"] == "produto":

        categoria = session["dados"]["categoria"]

        produto = produto_por_indice(categoria, mensagem)

        if not produto:
            return "Produto inválido."

        msg = mensagem_produto(produto)

        adicionar_item_carrinho(session, produto)

        session["etapa"] = "carrinho"

        return f"""
✅ Produto adicionado ao carrinho

{msg["texto"]}

{resumo_carrinho(session)}

1 - Finalizar pedido
2 - Escolher outro produto
3 - Menu principal
"""

    # -------------------------
    # CARRINHO
    # -------------------------

    if session["etapa"] == "carrinho":

        if mensagem == "1":

            session["etapa"] = "nome"

            return "👤 Qual é o seu nome?"

        elif mensagem == "2":

            session["etapa"] = "categoria"

            return criar_menu(
                "🌹 Escolha uma categoria",
                [
                    ("1", "Buquês"),
                    ("2", "Arranjos"),
                    ("3", "Coroas de Rosas"),
                    ("4", "Coroas de Flores do Campo"),
                    ("5", "Combos"),
                ],
            )

        elif mensagem == "3":

            session["etapa"] = "menu"

            return criar_menu(
                "🌸 Floricultura Marcelo\nEscolha uma opção:",
                [
                    ("1", "Ver produtos"),
                    ("2", "Ir para o site"),
                    ("3", "Pedido personalizado"),
                    ("4", "Falar com atendente"),
                ],
            )

        else:

            return "Escolha uma opção válida."

    # -------------------------
    # NOME
    # -------------------------

    if session["etapa"] == "nome":

        session["dados"]["nome"] = mensagem

        session["etapa"] = "endereco"

        return "📍 Informe o endereço de entrega."

    # -------------------------
    # ENDEREÇO
    # -------------------------

    if session["etapa"] == "endereco":

        session["dados"]["endereco"] = mensagem

        session["etapa"] = "confirmar"

        return f"""
📦 Pedido

Cliente: {session["dados"]["nome"]}

{resumo_carrinho(session)}

📍 Entrega em:
{mensagem}

1 - Confirmar pedido
2 - Cancelar
"""

    # -------------------------
    # CONFIRMAR
    # -------------------------

    if session["etapa"] == "confirmar":

        if mensagem == "1":


            from core.firebase import salvar_pedido

            salvar_pedido({
                "tipo": "floricultura",
                "nome": session["dados"]["nome"],
                "endereco": session["dados"]["endereco"],
                "carrinho": session.get("carrinho", []),
            })

            session["etapa"] = "finalizado"

            return f"""
✅ Pedido confirmado!

Cliente: {session["dados"]["nome"]}

{resumo_carrinho(session)}

Em breve enviaremos as informações de pagamento.
"""

        elif mensagem == "2":

            session["etapa"] = "menu"

            return "Pedido cancelado."

        else:

            return "Escolha 1 ou 2."

    # -------------------------
    # PERSONALIZADO
    # -------------------------

    if session["etapa"] == "personalizado":

        session["dados"]["pedido_personalizado"] = mensagem

        session["etapa"] = "finalizado"

        return """
✅ Pedido personalizado registrado.

Um atendente irá entrar em contato para combinar os detalhes.
"""