def _menu(titulo, opcoes):
    return {
        "tipo": "botoes",
        "mensagem": titulo,
        "botoes": [{"id": op[0], "label": op[1]} for op in opcoes]
    }


def fluxo_financeiro(session, mensagem):

    session.setdefault("etapa", "inicio")
    session.setdefault("historico", [])
    session.setdefault("dados", {})

    nome = session.get("nome", "")

    # ==================================================
    # AUXILIARES
    # ==================================================

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

    def finalizar():
        session["fluxo"] = "atendente"
        session["encerrar_bot"] = True

        return {
            "tipo": "texto",
            "mensagem": f"""📋 Solicitação registrada.

Assunto: {session["dados"].get("assunto")}
Nome: {session["dados"].get("nome")}
CPF: {session["dados"].get("cpf")}
Descrição: {session["dados"].get("descricao", "Não informada")}

👨‍💼 Você será encaminhado para nosso atendimento."""
        }

    def renderizar():

        etapa = session["etapa"]

        # --------------------------------------------------
        # MENU INICIAL
        # --------------------------------------------------

        if etapa == "inicio" or etapa == "menu":
            session["etapa"] = "menu"

            return _menu(
                f"""💰 Financeiro / Administrativo

{nome}, seu assunto é sobre:""",
                [
                    ("1", "Planos"),
                    ("2", "Funerária"),
                    ("3", "Outro assunto"),
                    ("0", "Voltar"),
                    ("00", "Menu principal"),
                ]
            )

        # --------------------------------------------------
        # PLANOS
        # --------------------------------------------------

        if etapa == "planos":
            return _menu(
                "📄 Assunto sobre Planos:",
                [
                    ("1", "Segunda via mensalidade"),
                    ("2", "Declaração anual de quitação"),
                    ("3", "Solicitar boleto / link"),
                    ("4", "Verificar situação do plano"),
                    ("5", "Outras solicitações"),
                    ("9", "Falar com atendente"),
                    ("0", "Voltar"),
                    ("00", "Menu principal"),
                ]
            )

        # --------------------------------------------------
        # FUNERÁRIA
        # --------------------------------------------------

        if etapa == "funeraria":
            return _menu(
                "🏢 Assunto sobre Funerária:",
                [
                    ("1", "Nota fiscal"),
                    ("2", "Segunda via recibo"),
                    ("3", "Dúvidas sobre pagamento"),
                    ("4", "Outras solicitações"),
                    ("9", "Falar com atendente"),
                    ("0", "Voltar"),
                    ("00", "Menu principal"),
                ]
            )

        # --------------------------------------------------
        # COLETAS COM BOTÕES
        # --------------------------------------------------

        if etapa == "coletar_nome":
            return {
                "tipo": "botoes",
                "mensagem": "Informe seu nome completo.",
                "botoes": [
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if etapa == "coletar_cpf":
            return {
                "tipo": "botoes",
                "mensagem": "Agora informe seu CPF.",
                "botoes": [
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if etapa == "descricao":
            return {
                "tipo": "botoes",
                "mensagem": "Descreva sua solicitação.",
                "botoes": [
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

    # ==================================================
    # NORMALIZAÇÃO
    # ==================================================

    if mensagem == "Voltar":
        mensagem = "0"

    if mensagem == "Menu principal":
        mensagem = "00"

    if mensagem == "0":
        return voltar()

    if mensagem == "00":
        return menu_principal()

    # ==================================================
    # INÍCIO
    # ==================================================

    if session["etapa"] == "inicio":
        return renderizar()

    # ==================================================
    # MENU INICIAL
    # ==================================================

    if session["etapa"] == "menu":

        if mensagem == "1":
            salvar_historico()
            session["etapa"] = "planos"
            return renderizar()

        if mensagem == "2":
            salvar_historico()
            session["etapa"] = "funeraria"
            return renderizar()

        if mensagem == "3":
            session["dados"]["assunto"] = "Outro assunto"
            salvar_historico()
            session["etapa"] = "coletar_nome"
            return renderizar()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    # ==================================================
    # MENU PLANOS
    # ==================================================

    if session["etapa"] == "planos":

        mapa = {
            "1": "Segunda via mensalidade",
            "2": "Declaração anual de quitação",
            "3": "Solicitar boleto / link",
            "4": "Verificar situação do plano",
            "5": "Outras solicitações"
        }

        if mensagem == "9":
            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True
            return {
                "tipo": "texto",
                "mensagem": "👨‍💼 Você será encaminhado para nosso atendimento."
            }

        if mensagem in mapa:
            session["dados"]["assunto"] = mapa[mensagem]
            salvar_historico()
            session["etapa"] = "coletar_nome"
            return renderizar()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    # ==================================================
    # MENU FUNERÁRIA
    # ==================================================

    if session["etapa"] == "funeraria":

        mapa = {
            "1": "Nota fiscal",
            "2": "Segunda via recibo",
            "3": "Dúvidas sobre pagamento",
            "4": "Outras solicitações"
        }

        if mensagem == "9":
            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True
            return {
                "tipo": "texto",
                "mensagem": "👨‍💼 Você será encaminhado para nosso atendimento."
            }

        if mensagem in mapa:
            session["dados"]["assunto"] = mapa[mensagem]
            salvar_historico()
            session["etapa"] = "coletar_nome"
            return renderizar()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    # ==================================================
    # COLETAS
    # ==================================================

    if session["etapa"] == "coletar_nome":
        session["dados"]["nome"] = mensagem
        salvar_historico()
        session["etapa"] = "coletar_cpf"
        return renderizar()

    if session["etapa"] == "coletar_cpf":
        session["dados"]["cpf"] = mensagem

        if session["dados"]["assunto"] in [
            "Outras solicitações",
            "Outro assunto"
        ]:
            salvar_historico()
            session["etapa"] = "descricao"
            return renderizar()

        return finalizar()

    if session["etapa"] == "descricao":
        session["dados"]["descricao"] = mensagem
        return finalizar()

    return renderizar()