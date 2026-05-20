from core.avisos import aviso_atendente


def fluxo_convenios(session, mensagem):

    session.setdefault("etapa", "inicio")
    session.setdefault("historico", [])
    session.setdefault("dados", {})

    # ==================================================
    # AUXILIARES
    # ==================================================

    def salvar():
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
        session["etapa_global"] = "menu"
        session["historico"] = []
        session["etapa"] = "inicio"

        return {
            "tipo": "botoes",
            "mensagem": "🕊️ Voltamos ao menu principal.\n\nEscolha uma opção:",
            "botoes": [
                {"id": "1", "label": "⚰️ Serviços funerários"},
                {"id": "2", "label": "🛡️ Planos"},
                {"id": "3", "label": "🗃️ Convênios"},
                {"id": "4", "label": "💼 Financeiro / Administrativo"},
                {"id": "5", "label": "🌷 Floricultura"},
                {"id": "6", "label": "🏢 Conhecer estrutura"},
                {"id": "7", "label": "📍 Localização"},
                {"id": "8", "label": "👤 Falar com atendente"},
                {"id": "99", "label": "🔄 Reiniciar atendimento"},
                
            ]
        }

    def menu(msg, botoes):
        return {
            "tipo": "botoes",
            "mensagem": msg,
            "botoes": botoes
        }

    def botoes_padrao(lista):
        return lista + [
            {"id": "0", "label": "Voltar"},
            {"id": "00", "label": "Menu principal"},
            {"id": "99", "label": "🔄 Reiniciar atendimento"},
        ]

    def encaminhar(origem, texto):
        aviso_atendente(
            session.get("nome"),
            session.get("numero"),
            origem
        )

        return {
            "tipo": "botoes",
            "mensagem": f"""{texto}

📲 Fale agora com nosso plantonista:
https://wa.me/5592995131313

ℹ️ As informações já foram enviadas para nossa equipe.""",
            "botoes": [
                {"id": "00", "label": "Menu principal"},
            ]
        }

    # ==================================================
    # RENDER
    # ==================================================

    def renderizar():

        etapa = session["etapa"]

        # MENU INICIAL (sem voltar)
        if etapa == "inicio" or etapa == "menu":
            session["etapa"] = "menu"

            return menu(
                "🗃️ *Convênios*\n\nComo podemos ajudar?",
                [
                    {"id": "1", "label": "Abertura de Sinistro"},
                    {"id": "2", "label": "Migração empresarial"},
                    {"id": "3", "label": "Orçamento para convênio"},
                    {"id": "00", "label": "Menu principal"},
                ]
            )

        if etapa == "sinistro_tipo":
            return menu(
                "📋 O atendimento é para:",
                botoes_padrao([
                    {"id": "1", "label": "Titular"},
                    {"id": "2", "label": "Dependente cadastrado"},
                    {"id": "3", "label": "Associado do titular"},
                ])
            )

        if etapa == "nome_titular":
            return {
                "tipo": "texto",
                "mensagem": "👤 Informe o nome completo do(a) titular."
            }

        if etapa == "nome_dependente":
            return {
                "tipo": "texto",
                "mensagem": "👤 Informe o nome completo do dependente ou associado."
            }

        if etapa == "migracao_nome":
            return {
                "tipo": "texto",
                "mensagem": "👤 Informe o nome completo do(a) titular."
            }

        if etapa == "orcamento":
            return {
                "tipo": "texto",
                "mensagem": "📎 Envie a proposta aqui para análise."
            }

        return {
            "tipo": "texto",
            "mensagem": "Etapa não encontrada."
        }

    # ==================================================
    # GLOBAL
    # ==================================================

    if mensagem == "Voltar":
        mensagem = "0"

    if mensagem == "Menu principal":
        mensagem = "00"

    if mensagem == "0":
        return voltar()

    if mensagem == "00":
        return menu_principal()

    if session["etapa"] == "inicio":
        return renderizar()

    # ==================================================
    # MENU
    # ==================================================

    if session["etapa"] == "menu":

        if mensagem == "1":
            salvar()
            session["etapa"] = "sinistro_tipo"
            return renderizar()

        if mensagem == "2":
            salvar()
            session["etapa"] = "migracao_nome"
            return renderizar()

        if mensagem == "3":
            salvar()
            session["etapa"] = "orcamento"
            return renderizar()

        return {
            "tipo": "texto",
            "mensagem": "Escolha uma opção válida."
        }

    # ==================================================
    # SINISTRO
    # ==================================================

    if session["etapa"] == "sinistro_tipo":

        if mensagem == "1":
            session["dados"]["tipo"] = "Titular"
            salvar()
            session["etapa"] = "nome_titular"
            return renderizar()

        if mensagem in ["2", "3"]:
            session["dados"]["tipo"] = (
                "Dependente" if mensagem == "2" else "Associado"
            )
            salvar()
            session["etapa"] = "nome_titular"
            return renderizar()

    if session["etapa"] == "nome_titular":
        session["dados"]["titular"] = mensagem

        if session["dados"]["tipo"] == "Titular":
            return encaminhar(
                "Convênio - Abertura de Sinistro",
                "👤 Recebemos as informações. Você será encaminhado para nosso atendimento."
            )

        salvar()
        session["etapa"] = "nome_dependente"
        return renderizar()

    if session["etapa"] == "nome_dependente":
        session["dados"]["dependente"] = mensagem

        return encaminhar(
            "Convênio - Abertura de Sinistro",
            "👤 Recebemos as informações. Você será encaminhado para nosso atendimento.\n\n📄 Tenha em mãos o documento de filiação. A elegibilidade será verificada pela equipe."
        )

    # ==================================================
    # MIGRAÇÃO
    # ==================================================

    if session["etapa"] == "migracao_nome":
        session["dados"]["titular"] = mensagem

        return encaminhar(
            "Convênio - Migração empresarial",
            "👤 Solicitação recebida. Você será encaminhado para nosso atendimento."
        )

    # ==================================================
    # ORÇAMENTO
    # ==================================================

    if session["etapa"] == "orcamento":
        return encaminhar(
            "Convênio - Orçamento",
            "👤 Proposta recebida. Você será encaminhado para nosso atendimento."
        )

    return renderizar()