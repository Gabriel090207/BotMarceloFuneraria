def fluxo_floricultura(session, mensagem):

    session.setdefault("etapa", "inicio")
    session.setdefault("historico", [])

    nome = session.get("nome", "")

    produtos = {
        "2": {
            "nome": "Coroa de flores naturais do campo",
            "preco": "R$ 350,00",
            "descricao": "Modelo padrão.",
            "imagem": "https://firebasestorage.googleapis.com/v0/b/bot-marcelofloricultura.firebasestorage.app/o/floricultura%2Fcoroa_padrao.png?alt=media&token=f14263ac-c37b-46d3-8e28-fc8e5233dbb3"
        },
        "3": {
            "nome": "Coroa de flores naturais com 6 rosas",
            "preco": "R$ 400,00",
            "descricao": "Modelo especial.",
            "imagem": "https://firebasestorage.googleapis.com/v0/b/bot-marcelofloricultura.firebasestorage.app/o/floricultura%2Fcoroa_rosas.png?alt=media&token=8801a471-b2a7-4a94-ad22-ab5c4183c35c"
        },
        "4": {
            "nome": "Buquê com flores do campo naturais",
            "preco": "A partir de R$ 150,00",
            "descricao": "Modelo padrão.",
            "imagem": "https://firebasestorage.googleapis.com/v0/b/bot-marcelofloricultura.firebasestorage.app/o/floricultura%2Fbuque_padrao.png?alt=media&token=d7657ef6-afac-46d7-b032-858d17aae189"
        },
        "5": {
            "nome": "Buquê de flores naturais do campo e 6 rosas",
            "preco": "A partir de R$ 200,00",
            "descricao": "Modelo padrão.",
            "imagem": "https://firebasestorage.googleapis.com/v0/b/bot-marcelofloricultura.firebasestorage.app/o/floricultura%2Fbuque_rosas.png?alt=media&token=c26c0a8f-7c6f-4805-9620-81f672c80cae"
        }
    }

    # -------------------------------------------------
    # FUNÇÕES
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
        session["etapa_global"] = "menu"

        return {
            "tipo": "botoes",
            "mensagem": "🔙 Voltamos ao menu principal.\n\nEscolha uma opção:",
            "botoes": [
                {"id": "1", "label": "Serviços funerários"},
                {"id": "2", "label": "Planos"},
                {"id": "3", "label": "Financeiro / Administrativo"},
                {"id": "4", "label": "Floricultura"},
                {"id": "5", "label": "Falar com atendente"},
            ]
        }

    def renderizar():

        etapa = session["etapa"]

        if etapa == "inicio" or etapa == "menu":
            session["etapa"] = "menu"

            return {
                "tipo": "botoes",
                "mensagem": f"""🌸 Floricultura

{nome}, escolha uma opção:""",
                "botoes": [
                    {"id": "1", "label": "Arranjos e Presentes"},
                    {"id": "2", "label": "Coroa padrão"},
                    {"id": "3", "label": "Coroa com rosas"},
                    {"id": "4", "label": "Buquê padrão"},
                    {"id": "5", "label": "Buquê com rosas"},
                    {"id": "9", "label": "Falar com atendente"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if etapa == "site":
            return {
                "tipo": "botoes",
                "mensagem": """🌐 Arranjos e Presentes:

https://floriculturavalledasflores.com.br""",
                "botoes": [
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if etapa == "produto":
            produto = produtos[session["produto"]]

            return [
                {
                    "tipo": "imagem",
                    "url": produto["imagem"]
                },
                {
                    "tipo": "botoes",
                    "mensagem": f"""🌸 *{produto["nome"]}*

💰 {produto["preco"]}

{produto["descricao"]}

Deseja confirmar interesse?""",
                    "botoes": [
                        {"id": "1", "label": "Confirmar"},
                        {"id": "0", "label": "Voltar"},
                        {"id": "00", "label": "Menu principal"},
                    ]
                }
            ]

        if etapa == "pos_interesse":
            return {
                "tipo": "botoes",
                "mensagem": "🙏 Deseja mais alguma coisa?",
                "botoes": [
                    {"id": "1", "label": "Sim"},
                    {"id": "2", "label": "Falar com atendente"},
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
    # ENTRADA
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

        if mensagem == "9":
            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True

            return {
                "tipo": "texto",
                "mensagem": "👨‍💼 Você será encaminhado para nosso atendimento."
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
            salvar_historico()
            session["etapa"] = "pos_interesse"
            return renderizar()

        return {
            "tipo": "texto",
            "mensagem": "Escolha uma opção válida."
        }

    # -------------------------------------------------
    # PÓS INTERESSE
    # -------------------------------------------------

    if session["etapa"] == "pos_interesse":

        if mensagem == "1":
            session["historico"] = []
            session["etapa"] = "menu"
            return renderizar()

        if mensagem == "2":
            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True

            return {
                "tipo": "texto",
                "mensagem": "👨‍💼 Você será encaminhado para nosso atendimento."
            }

        return {
            "tipo": "texto",
            "mensagem": "Escolha uma opção válida."
        }

    return renderizar()