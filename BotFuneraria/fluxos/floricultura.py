from core.avisos import aviso_floricultura, aviso_atendente

def fluxo_floricultura(session, mensagem):

    session.setdefault("etapa", "inicio")
    session.setdefault("historico", [])
    session.setdefault("carrinho", [])

    nome = session.get("nome", "")

    produtos = {
        "2": {
            "nome": "🌸 Coroa de flores naturais do campo",
            "preco": "R$ 350,00",
            "descricao": "Modelo padrão.",
            "imagem": "https://firebasestorage.googleapis.com/v0/b/bot-marcelofloricultura.firebasestorage.app/o/floricultura%2Fcoroa_padrao.png?alt=media&token=f14263ac-c37b-46d3-8e28-fc8e5233dbb3"
        },
        "3": {
            "nome": "🌸 Coroa de flores naturais com 6 rosas",
            "preco": "R$ 400,00",
            "descricao": "Modelo especial.",
            "imagem": "https://firebasestorage.googleapis.com/v0/b/bot-marcelofloricultura.firebasestorage.app/o/floricultura%2Fcoroa_rosas.png?alt=media&token=8801a471-b2a7-4a94-ad22-ab5c4183c35c"
        },
        "4": {
            "nome": "🌼 Buquê com flores do campo naturais",
            "preco": "A partir de R$ 150,00",
            "descricao": "Modelo padrão.",
            "imagem": "https://firebasestorage.googleapis.com/v0/b/bot-marcelofloricultura.firebasestorage.app/o/floricultura%2Fbuque_padrao.png?alt=media&token=d7657ef6-afac-46d7-b032-858d17aae189"
        },
        "5": {
            "nome": "💐 Buquê de flores naturais do campo e 6 rosas",
            "preco": "A partir de R$ 200,00",
            "descricao": "Modelo padrão.",
            "imagem": "https://firebasestorage.googleapis.com/v0/b/bot-marcelofloricultura.firebasestorage.app/o/floricultura%2Fbuque_rosas.png?alt=media&token=c26c0a8f-7c6f-4805-9620-81f672c80cae"
        }
    }

    # -------------------------------------------------
    # AUXILIARES
    # -------------------------------------------------

    def salvar_historico():
        etapa = session.get("etapa")
        if etapa:
            session["historico"].append(etapa)

    def voltar():
        if session["historico"]:
            session["etapa"] = session["historico"].pop()
        else:
            session["etapa"] = "menu"
        return renderizar()

    def menu_principal():
        session["fluxo"] = None
        session["etapa"] = "inicio"
        session["historico"] = []

        return {
            "tipo": "botoes",
            "mensagem": "🕊️ Voltamos ao menu principal.\n\nEscolha uma opção:",
            "botoes": [
                {"id": "1", "label": "Serviços funerários"},
                {"id": "2", "label": "Planos"},
                {"id": "3", "label": "🗃️ Convênios"},
                {"id": "4", "label": "Financeiro / Administrativo"},
                {"id": "5", "label": "Floricultura"},
                {"id": "6", "label": "📍 Localização"},
                {"id": "7", "label": "Falar com atendente"},
            ]
        }

    def resumo_pedido():
        linhas = ["🌸 *Pedido Floricultura*", ""]
        for item in session["carrinho"]:
            linhas.append(f"• {item}")
        return "\n".join(linhas)

    def renderizar():

        etapa = session["etapa"]

        # ---------------- MENU ----------------

        if etapa == "inicio" or etapa == "menu":

            session["etapa"] = "menu"

            msg = f"{nome}, escolha uma opção:"
            if session["carrinho"]:
                msg = f"{nome}, o que mais você deseja?"

            botoes = [
                {"id": "1", "label": "Arranjos e Presentes"},
                {"id": "2", "label": "Coroa padrão"},
                {"id": "3", "label": "Coroa com rosas"},
                {"id": "4", "label": "Buquê padrão"},
                {"id": "5", "label": "Buquê com rosas"},
            ]

            if session["carrinho"]:
                botoes.append(
                    {"id": "8", "label": "Finalizar pedido agora"}
                )

            botoes += [
                {"id": "7", "label": "💡 Gráfica"},
                {"id": "9", "label": "Falar com atendente"},
                {"id": "00", "label": "Menu principal"},
            ]

            return {
                "tipo": "botoes",
                "mensagem": f"""🌸 Floricultura

{msg}""",
                "botoes": botoes
            }

        # ---------------- SITE ----------------

        if etapa == "site":
            return {
                "tipo": "botoes",
                "mensagem": """🎁 Arranjos e Presentes:

https://floriculturavalledasflores.com.br""",
                "botoes": [
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        # ---------------- PRODUTO ----------------

        if etapa == "produto":

            produto = produtos[session["produto"]]

            return [
                {
                    "tipo": "imagem",
                    "url": produto["imagem"]
                },
                {
                    "tipo": "botoes",
                    "mensagem": f"""*{produto["nome"]}*

💰 {produto["preco"]}

{produto["descricao"]}

Deseja adicionar ao pedido?""",
                    "botoes": [
                        {"id": "1", "label": "Confirmar"},
                        {"id": "0", "label": "Voltar"},
                        {"id": "00", "label": "Menu principal"},
                    ]
                }
            ]

        # ---------------- GRÁFICA ----------------

        if etapa == "grafica":
            return {
                "tipo": "botoes",
                "mensagem": """💡 *Gráfica*


📎 Catálogo de materiais:
https://botmarcelofuneraria.onrender.com/static/grafica.pdf


👤 Deseja falar com nosso atendimento?""",
                "botoes": [
                    {"id": "1", "label": "Solicitar atendimento"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        # ---------------- PÓS ITEM ----------------

        if etapa == "pos_interesse":
            return {
                "tipo": "botoes",
                "mensagem": "🌹 Deseja mais alguma coisa?",
                "botoes": [
                    {"id": "1", "label": "Não, confirmar pedido"},
                    {"id": "2", "label": "Sim"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

    # -------------------------------------------------
    # NORMALIZAÇÃO
    # -------------------------------------------------

    if mensagem == "Voltar":
        mensagem = "0"

    if mensagem == "Menu principal":
        mensagem = "00"

    if mensagem == "0":
        return voltar()

    if mensagem == "00":
        return menu_principal()

    # -------------------------------------------------
    # INÍCIO
    # -------------------------------------------------

    if session["etapa"] == "inicio":
        return renderizar()

    # -------------------------------------------------
    # MENU
    # -------------------------------------------------

    if session["etapa"] == "menu":

        if mensagem == "1":
            salvar_historico()
            session["etapa"] = "site"
            return renderizar()

        if mensagem in produtos:
            salvar_historico()
            session["produto"] = mensagem
            session["etapa"] = "produto"
            return renderizar()

        if mensagem == "8":

            if not session["carrinho"]:
                return {
                    "tipo": "texto",
                    "mensagem": "Seu pedido está vazio."
                }


            aviso_floricultura(
                session.get("nome"),
                session.get("numero"),
                session.get("carrinho", [])
            )

            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True

            return {
                "tipo": "texto",
                "mensagem": resumo_pedido() + "\n\n👤 Você será encaminhado para finalizar seu pedido."
            }

        if mensagem == "7":
            salvar_historico()
            session["etapa"] = "grafica"
            return renderizar()

        if mensagem == "9":

            aviso_atendente(
                session.get("nome"),
                session.get("numero"),
                "Floricultura"
            )

            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True

            return {
                "tipo": "texto",
                "mensagem": resumo_pedido() + "\n\n👤 Você será encaminhado para nosso atendimento."
            }

        return {
            "tipo": "texto",
            "mensagem": "Escolha uma opção válida."
        }

    # -------------------------------------------------
    # PRODUTO
    # -------------------------------------------------

    if session["etapa"] == "produto":

        if mensagem == "1":

            produto = produtos[session["produto"]]
            session["carrinho"].append(produto["nome"])

            salvar_historico()
            session["etapa"] = "pos_interesse"
            return renderizar()

        return {
            "tipo": "texto",
            "mensagem": "Escolha uma opção válida."
        }

    # -------------------------------------------------
    # PÓS ITEM
    # -------------------------------------------------

    if session["etapa"] == "pos_interesse":

        if mensagem == "1":


            aviso_floricultura(
                session.get("nome"),
                session.get("numero"),
                session.get("carrinho", [])
            )

            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True

            return {
                "tipo": "texto",
                "mensagem": resumo_pedido() + "\n\n👤 Você será encaminhado para finalizar seu pedido."
            }

        if mensagem == "2":
            session["historico"] = []
            session["etapa"] = "menu"
            return renderizar()

        return {
            "tipo": "texto",
            "mensagem": "Escolha uma opção válida."
        }

    if session["etapa"] == "grafica":

        if mensagem == "1":
            aviso_atendente(
                session.get("nome"),
                session.get("numero"),
                "Gráfica"
            )

            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True

            return {
                "tipo": "texto",
                "mensagem": "💡 Você será encaminhado para nosso atendimento da gráfica."
            }

        return {
            "tipo": "texto",
            "mensagem": "Escolha uma opção válida."
        }

    return renderizar()