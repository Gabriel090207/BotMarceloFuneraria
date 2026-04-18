def fluxo_floricultura(session, mensagem):

    if "etapa" not in session:
        session["etapa"] = "inicio"

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
    # NORMALIZA BOTÕES
    # -------------------------------------------------

    if mensagem == "Voltar":
        mensagem = "0"

    elif mensagem == "Menu principal":
        mensagem = "00"

    # -------------------------------------------------
    # MENU PRINCIPAL
    # -------------------------------------------------

    def voltar_menu_principal():
        session["fluxo"] = None
        session["etapa"] = "inicio"
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

    # -------------------------------------------------
    # INÍCIO
    # -------------------------------------------------

    if session["etapa"] == "inicio":

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
                {"id": "00", "label": "Voltar ao menu"},
            ]
        }

    # -------------------------------------------------
    # MENU
    # -------------------------------------------------

    if session["etapa"] == "menu":

        if mensagem == "1":
            return {
                "tipo": "texto",
                "mensagem": "🌐 Arranjos e Presentes:\nhttps://floriculturavalledasflores.com.br"
            }

        elif mensagem in produtos:

            produto = produtos[mensagem]
            session["produto_escolhido"] = mensagem
            session["etapa"] = "produto"

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

        elif mensagem == "9":
            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True

            return {
                "tipo": "texto",
                "mensagem": "👨‍💼 Você será encaminhado para nosso atendimento."
            }

        elif mensagem == "00":
            return voltar_menu_principal()

        else:
            return {
                "tipo": "texto",
                "mensagem": "Escolha uma opção válida."
            }

    # -------------------------------------------------
    # PRODUTO
    # -------------------------------------------------

    if session["etapa"] == "produto":

        if mensagem == "1":

            session["etapa"] = "pos_interesse"

            return {
                "tipo": "botoes",
                "mensagem": "Perfeito 🙏\n\nDeseja mais alguma coisa?",
                "botoes": [
                    {"id": "1", "label": "Ver menu novamente"},
                    {"id": "2", "label": "Falar com atendente"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        elif mensagem == "0":
            session["etapa"] = "menu"
            return fluxo_floricultura(session, "menu")

        elif mensagem == "00":
            return voltar_menu_principal()

        else:
            return {
                "tipo": "texto",
                "mensagem": "Escolha uma opção válida."
            }

    # -------------------------------------------------
    # PÓS INTERESSE
    # -------------------------------------------------

    if session["etapa"] == "pos_interesse":

        if mensagem == "1":
            session["etapa"] = "menu"

            return {
                "tipo": "botoes",
                "mensagem": "😊 O que você deseja agora?",
                "botoes": [
                    {"id": "1", "label": "Serviços funerários"},
                    {"id": "2", "label": "Planos"},
                    {"id": "3", "label": "Financeiro / Administrativo"},
                    {"id": "4", "label": "Floricultura"},
                    {"id": "5", "label": "Falar com atendente"},
                ]
            }

        elif mensagem == "2":
            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True

            return {
                "tipo": "texto",
                "mensagem": "👨‍💼 Você será encaminhado para nosso atendimento."
            }

        elif mensagem == "00":
            return voltar_menu_principal()

        else:
            return {
                "tipo": "texto",
                "mensagem": "Escolha uma opção válida."
            }

    return {
        "tipo": "texto",
        "mensagem": "Escolha uma opção válida."
    }