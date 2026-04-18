from core.firebase import buscar_servicos_funerarios

VIDEO_ESTRUTURA = "https://firebasestorage.googleapis.com/v0/b/bot-marcelofloricultura.firebasestorage.app/o/midias%2FWhatsApp%20Video%202026-04-15%20at%2017.16.41.mp4?alt=media&token=a3297384-1607-45a2-a3a9-3772caf942e0"

COBERTURA_COMPLETA = """
💡 *COBERTURA:*

✅ Salão completo 24h na Funerária Canaã
✅ Caixão padrão até 1.90 comportando até 85kg com segurança
✅ Remoção e Cortejo
✅ Preparação completa + Tanatopraxia (24h)
✅ Ornamentação com flores artificiais
✅ Kit café da manhã para até 05 pessoas que pernoitarem + Copa 24h
✅ Pagamento de taxa municipal, livro de presença, véu e velas
✅ Paramentação completa para velório (exclusivo velório externo)
✅ Contratação de demais serviços como flores naturais, cerimonial ecumênico, translado, entre outros é feito direto com o(a) atendente.
"""

COBERTURA_EXTERNO = """
💡 *COBERTURA:*

✅ Caixão padrão até 1.90 comportando até 85kg com segurança
✅ Remoção e Cortejo
✅ Preparação completa + Tanatopraxia (24h)
✅ Ornamentação com flores artificiais
✅ Pagamento de taxa municipal, livro de presença, véu e velas
✅ Paramentação completa para velório (exclusivo velório externo)
✅ Contratação de demais serviços como flores naturais, cerimonial ecumênico, translado, entre outros é feito direto com o(a) atendente.
"""


def menu_principal():
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


def fluxo_funeraria_orcamento(session, mensagem):

    session.setdefault("etapa", "inicio")
    session.setdefault("dados", {})
    session.setdefault("servicos_cache", [])

    nome = session.get("nome", "")

    # ==================================================
    # MENU INICIAL
    # ==================================================

    if session["etapa"] == "inicio":

        session["etapa"] = "submenu"

        return {
            "tipo": "botoes",
            "mensagem": f"""🏢 *Orçamento Funerário*

{nome}, como podemos te ajudar?""",
            "botoes": [
                {"id": "1", "label": "Ver serviços e valores"},
                {"id": "2", "label": "Conhecer estrutura"},
                {"id": "3", "label": "Falar com atendente"},
                {"id": "0", "label": "Voltar"},
                {"id": "00", "label": "Menu principal"},
            ]
        }

    # ==================================================
    # SUBMENU
    # ==================================================

    if session["etapa"] == "submenu":

        if mensagem == "1":
            session["etapa"] = "lista"
            return fluxo_funeraria_orcamento(session, "x")

        if mensagem == "2":
            session["etapa"] = "estrutura"

            return [
                {
                    "tipo": "video",
                    "url": VIDEO_ESTRUTURA
                },
                {
                    "tipo": "botoes",
                    "mensagem": """🏢 *Conheça nossa estrutura*

Ambientes preparados para acolher sua família com conforto, respeito e tranquilidade.""",
                    "botoes": [
                        {"id": "1", "label": "Ver serviços"},
                        {"id": "00", "label": "Menu principal"},
                    ]
                }
            ]

        if mensagem == "3":
            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True
            return {
                "tipo": "texto",
                "mensagem": "👨‍💼 Você será encaminhado para nosso atendimento."
            }

        if mensagem == "0":
            session["fluxo"] = "funeraria"
            session["etapa"] = "inicio"
            return {
                "tipo": "texto",
                "mensagem": "🔙 Voltando ao menu funerária."
            }

        if mensagem == "00":
            session["fluxo"] = None
            session["etapa"] = "inicio"
            session["etapa_global"] = "menu"
            return menu_principal()

    # ==================================================
    # ESTRUTURA
    # ==================================================

    if session["etapa"] == "estrutura":

        if mensagem == "1":
            session["etapa"] = "lista"
            return fluxo_funeraria_orcamento(session, "x")

        if mensagem == "00":
            session["fluxo"] = None
            session["etapa"] = "inicio"
            session["etapa_global"] = "menu"
            return menu_principal()

    # ==================================================
    # LISTA SERVIÇOS
    # ==================================================

    if session["etapa"] == "lista":

        servicos = buscar_servicos_funerarios()
        session["servicos_cache"] = servicos

        botoes = []
        contador = 1

        for s in servicos:
            botoes.append({
                "id": str(contador),
                "label": s["nome"][:24]
            })
            contador += 1

        botoes.append({"id": "0", "label": "Voltar"})
        botoes.append({"id": "00", "label": "Menu principal"})

        session["etapa"] = "menu_lista"

        return {
            "tipo": "botoes",
            "mensagem": "🏢 *Serviços e Valores*\n\nEscolha uma opção:",
            "botoes": botoes
        }

    # ==================================================
    # MENU LISTA
    # ==================================================

    if session["etapa"] == "menu_lista":

        if mensagem == "0":
            session["etapa"] = "inicio"
            return fluxo_funeraria_orcamento(session, "x")

        if mensagem == "00":
            session["fluxo"] = None
            session["etapa"] = "inicio"
            session["etapa_global"] = "menu"
            return menu_principal()

        if mensagem.isdigit():

            indice = int(mensagem) - 1
            servicos = session["servicos_cache"]

            if 0 <= indice < len(servicos):

                servico = servicos[indice]
                session["dados"]["servico"] = servico
                session["etapa"] = "detalhes"

                resposta = []

                if servico.get("imagens"):
                    for img in servico["imagens"]:
                        resposta.append({
                            "tipo": "imagem",
                            "url": img
                        })

                texto = f"""🏢 *{servico["nome"]}*

💰 R$ {float(servico["preco"]):,.2f}
""".replace(",", "X").replace(".", ",").replace("X", ".")

                if servico.get("capacidade"):
                    texto += f'\n✅ Capacidade interna: {servico["capacidade"]}'

                if servico.get("suite"):
                    texto += f'\n✅ Suíte: {servico["suite"]}'

                if servico.get("area_externa"):
                    texto += f'\n✅ {servico["area_externa"]}'

                if servico.get("descricao"):
                    texto += f'\n\n📝 {servico["descricao"]}'

                if str(servico.get("cobertura", "")).lower() == "externo":
                    texto += "\n" + COBERTURA_EXTERNO
                else:
                    texto += "\n" + COBERTURA_COMPLETA

                resposta.append({
                    "tipo": "botoes",
                    "mensagem": texto,
                    "botoes": [
                        {"id": "1", "label": "Tenho interesse"},
                        {"id": "2", "label": "Ver outra opção"},
                        {"id": "0", "label": "Voltar"},
                        {"id": "00", "label": "Menu principal"},
                    ]
                })

                return resposta

        return {
            "tipo": "texto",
            "mensagem": "Escolha uma opção válida."
        }

    # ==================================================
    # DETALHES
    # ==================================================

    if session["etapa"] == "detalhes":

        if mensagem == "1":
            session["etapa"] = "coletar_nome"
            return {"tipo": "texto", "mensagem": "Informe seu nome completo."}

        if mensagem == "2":
            session["etapa"] = "lista"
            return fluxo_funeraria_orcamento(session, "x")

        if mensagem == "0":
            session["etapa"] = "lista"
            return fluxo_funeraria_orcamento(session, "x")

        if mensagem == "00":
            session["fluxo"] = None
            session["etapa"] = "inicio"
            session["etapa_global"] = "menu"
            return menu_principal()

    # ==================================================
    # COLETA
    # ==================================================

    if session["etapa"] == "coletar_nome":

        session["dados"]["nome"] = mensagem
        session["etapa"] = "cidade"
        return {"tipo": "texto", "mensagem": "Informe sua cidade."}

    if session["etapa"] == "cidade":

        session["dados"]["cidade"] = mensagem
        session["etapa"] = "data"
        return {"tipo": "texto", "mensagem": "Para quando precisa? (opcional)"}

    if session["etapa"] == "data":

        session["dados"]["data"] = mensagem
        servico = session["dados"]["servico"]

        session["fluxo"] = "atendente"
        session["encerrar_bot"] = True

        return {
            "tipo": "texto",
            "mensagem": f"""📋 *Solicitação registrada*

Interesse: {servico["nome"]}
Nome: {session["dados"]["nome"]}
Cidade: {session["dados"]["cidade"]}
Data: {session["dados"]["data"]}

👨‍💼 Você será encaminhado para nosso atendimento."""
        }

    return {
        "tipo": "texto",
        "mensagem": "Escolha uma opção válida."
    }