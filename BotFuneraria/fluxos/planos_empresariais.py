def _menu(titulo, opcoes):
    return {
        "tipo": "botoes",
        "mensagem": titulo,
        "botoes": [{"id": op[0], "label": op[1]} for op in opcoes]
    }


def fluxo_planos_empresariais(session, mensagem):

    if "etapa" not in session:
        session["etapa"] = "inicio"

    if "dados" not in session:
        session["dados"] = {}

    nome = session.get("nome", "")

    # -------------------------
    # ATALHOS GLOBAIS
    # -------------------------

    if mensagem == "9":
        session["fluxo"] = "atendente"
        from fluxos.atendente import fluxo_atendente
        return fluxo_atendente(session, mensagem)

    if mensagem == "00":
        session["fluxo"] = None
        session["etapa"] = "inicio"
        return {
            "tipo": "texto",
            "mensagem": "Voltando ao menu principal..."
        }

    # -------------------------
    # INICIO
    # -------------------------

    if session["etapa"] == "inicio":

        session["etapa"] = "menu"

        return _menu(
            f"""🏢 Planos Empresariais

{nome}, escolha uma opção:""",
            [
                ("1", "Plano Empresarial Básico"),
                ("2", "Plano Empresarial Completo"),
                ("9", "Falar com atendente"),
                ("00", "Voltar ao menu"),
            ]
        )

    # -------------------------
    # ESCOLHA
    # -------------------------

    if session["etapa"] == "menu":

        planos = {
            "1": {
                "nome": "Empresarial Básico",
                "desc": "✔ Cobertura para colaboradores\n✔ Atendimento básico\n✔ Documentação"
            },
            "2": {
                "nome": "Empresarial Completo",
                "desc": "✔ Cobertura completa\n✔ Atendimento prioritário\n✔ Gestão documental\n✔ Suporte 24h"
            }
        }

        if mensagem not in planos:
            return {
                "tipo": "texto",
                "mensagem": "Escolha uma opção válida."
            }

        plano = planos[mensagem]

        session["dados"]["plano"] = plano["nome"]
        session["etapa"] = "confirmar"

        return _menu(
            f"""📋 {plano["nome"]}

{plano["desc"]}

Deseja falar com um consultor?""",
            [
                ("1", "Sim"),
                ("2", "Voltar"),
                ("9", "Falar com atendente"),
                ("00", "Menu principal"),
            ]
        )

    # -------------------------
    # CONFIRMAR
    # -------------------------

    if session["etapa"] == "confirmar":

        if mensagem == "1":

            session["fluxo"] = "atendente"

            from fluxos.atendente import fluxo_atendente

            return {
                "tipo": "texto",
                "mensagem": f"""✅ Interesse registrado: {session["dados"]["plano"]}

Um consultor empresarial irá entrar em contato."""
            }

        elif mensagem == "2":

            session["etapa"] = "menu"
            return fluxo_planos_empresariais(session, "menu")

        else:
            return {
                "tipo": "texto",
                "mensagem": "Escolha 1 ou 2."
            }