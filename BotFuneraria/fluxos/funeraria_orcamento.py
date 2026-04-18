from core.firebase import buscar_servicos_funerarios


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


def fluxo_funeraria_orcamento(session, mensagem):

    session.setdefault("etapa", "inicio")
    session.setdefault("dados", {})
    session.setdefault("servicos_cache", [])

    nome = session.get("nome", "")

    # ==================================================
    # MENU PRINCIPAL DO ORÇAMENTO
    # ==================================================

    if session["etapa"] == "inicio":

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

        session["etapa"] = "menu"

        return {
            "tipo": "botoes",
            "mensagem": f"""🏢 *Orçamento Funerário*

{nome}, escolha uma opção:""",
            "botoes": botoes
        }

    # ==================================================
    # MENU LISTA SERVIÇOS
    # ==================================================

    if session["etapa"] == "menu":

        if mensagem == "0":
            session["etapa"] = "inicio"
            session["fluxo"] = "funeraria"
            return {
                "tipo": "texto",
                "mensagem": "🔙 Voltando ao menu funerária."
            }

        if mensagem == "00":
            session["fluxo"] = None
            session["etapa"] = "inicio"
            session["etapa_global"] = "menu"
            return {
                "tipo": "botoes",
                "mensagem": "🏠 Menu principal:",
                "botoes": [
                    {"id": "1", "label": "Serviços funerários"},
                    {"id": "2", "label": "Planos"},
                    {"id": "3", "label": "Financeiro / Administrativo"},
                    {"id": "4", "label": "Floricultura"},
                    {"id": "5", "label": "Falar com atendente"},
                ]
            }

        if mensagem.isdigit():

            indice = int(mensagem) - 1
            servicos = session["servicos_cache"]

            if 0 <= indice < len(servicos):

                servico = servicos[indice]
                session["dados"]["servico"] = servico

                session["etapa"] = "detalhes"

                resposta = []

                if servico.get("imagens"):
                    resposta.append({
                        "tipo": "imagem",
                        "url": servico["imagens"][0]
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

                if servico.get("cobertura") == "externo":
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
            return {
                "tipo": "botoes",
                "mensagem": "Informe seu nome completo.",
                "botoes": [
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if mensagem == "2":
            session["etapa"] = "inicio"
            return fluxo_funeraria_orcamento(session, mensagem)

        if mensagem == "0":
            session["etapa"] = "inicio"
            return fluxo_funeraria_orcamento(session, mensagem)

        if mensagem == "00":
            session["fluxo"] = None
            session["etapa"] = "inicio"
            session["etapa_global"] = "menu"
            return {
                "tipo": "botoes",
                "mensagem": "🏠 Menu principal:",
                "botoes": [
                    {"id": "1", "label": "Serviços funerários"},
                    {"id": "2", "label": "Planos"},
                    {"id": "3", "label": "Financeiro / Administrativo"},
                    {"id": "4", "label": "Floricultura"},
                    {"id": "5", "label": "Falar com atendente"},
                ]
            }

    # ==================================================
    # COLETAS
    # ==================================================

    if session["etapa"] == "coletar_nome":

        if mensagem == "0":
            session["etapa"] = "detalhes"
            return fluxo_funeraria_orcamento(session, "x")

        if mensagem == "00":
            session["fluxo"] = None
            session["etapa"] = "inicio"
            session["etapa_global"] = "menu"

        session["dados"]["nome"] = mensagem
        session["etapa"] = "cidade"

        return {
            "tipo": "botoes",
            "mensagem": "Informe sua cidade.",
            "botoes": [
                {"id": "0", "label": "Voltar"},
                {"id": "00", "label": "Menu principal"},
            ]
        }

    if session["etapa"] == "cidade":

        if mensagem == "0":
            session["etapa"] = "coletar_nome"
            return fluxo_funeraria_orcamento(session, "x")

        session["dados"]["cidade"] = mensagem
        session["etapa"] = "data"

        return {
            "tipo": "botoes",
            "mensagem": "Para quando precisa? (opcional)",
            "botoes": [
                {"id": "0", "label": "Voltar"},
                {"id": "00", "label": "Menu principal"},
            ]
        }

    if session["etapa"] == "data":

        if mensagem == "0":
            session["etapa"] = "cidade"
            return fluxo_funeraria_orcamento(session, "x")

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