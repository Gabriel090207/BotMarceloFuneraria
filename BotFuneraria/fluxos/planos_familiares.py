from core.menus import criar_menu


def fluxo_planos_familiares(session, mensagem):

    if "etapa" not in session:
        session["etapa"] = "inicio"

    nome = session.get("nome", "")

    # -------------------------
    # ATENDENTE GLOBAL
    # -------------------------

    if mensagem == "9":
        session["fluxo"] = "atendente"
        from fluxos.atendente import fluxo_atendente
        return fluxo_atendente(session, mensagem)

    if mensagem == "00":
        session["fluxo"] = None
        session["etapa"] = "inicio"
        return "Voltando ao menu principal..."

    # -------------------------
    # INICIO
    # -------------------------

    if session["etapa"] == "inicio":

        session["etapa"] = "menu"

        return criar_menu(
            f"🏠 Planos Familiares\n\n{nome}, escolha uma opção:",
            [
                ("1", "Plano Básico"),
                ("2", "Plano Intermediário"),
                ("3", "Plano Premium"),
                ("9", "Falar com atendente"),
                ("00", "Voltar ao menu principal"),
            ]
        )

    # -------------------------
    # ESCOLHA DO PLANO
    # -------------------------

    if session["etapa"] == "menu":

        planos = {
            "1": {
                "nome": "Plano Básico",
                "desc": "✔ Atendimento funerário\n✔ Urna simples\n✔ Transporte local\n✔ Velório simples"
            },
            "2": {
                "nome": "Plano Intermediário",
                "desc": "✔ Atendimento completo\n✔ Urna intermediária\n✔ Velório completo\n✔ Translado incluso"
            },
            "3": {
                "nome": "Plano Premium",
                "desc": "✔ Atendimento completo\n✔ Urna premium\n✔ Sala VIP\n✔ Translado nacional\n✔ Atendimento prioritário"
            }
        }

        if mensagem not in planos:
            return "Escolha uma opção válida."

        plano = planos[mensagem]

        session["dados"]["plano"] = plano["nome"]
        session["etapa"] = "confirmar"

        return f"""
📋 {plano["nome"]}

{plano["desc"]}

Deseja contratar este plano?

1 - Sim
2 - Escolher outro plano
9 - Falar com atendente
00 - Voltar ao menu principal
"""

    # -------------------------
    # CONFIRMAÇÃO
    # -------------------------

    if session["etapa"] == "confirmar":

        if mensagem == "1":

            session["fluxo"] = "atendente"

            from fluxos.atendente import fluxo_atendente
            return f"""
✅ Plano selecionado: {session["dados"]["plano"]}

Um consultor irá entrar em contato para finalizar a contratação.
"""

        elif mensagem == "2":

            session["etapa"] = "menu"

            return fluxo_planos_familiares(session, mensagem)

        else:
            return "Escolha 1 ou 2."