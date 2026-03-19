from core.menus import criar_menu


def fluxo_planos_empresariais(session, mensagem):

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
            f"🏢 Planos Empresariais\n\n{nome}, escolha uma opção:",
            [
                ("1", "Plano Empresarial Básico"),
                ("2", "Plano Empresarial Completo"),
                ("9", "Falar com atendente"),
                ("00", "Voltar ao menu principal"),
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
            return "Escolha uma opção válida."

        plano = planos[mensagem]

        session["dados"]["plano"] = plano["nome"]
        session["etapa"] = "confirmar"

        return f"""
📋 {plano["nome"]}

{plano["desc"]}

Deseja falar com um consultor?

1 - Sim
2 - Voltar
9 - Falar com atendente
00 - Voltar ao menu principal
"""

    # -------------------------
    # CONFIRMAR
    # -------------------------

    if session["etapa"] == "confirmar":

        if mensagem == "1":

            session["fluxo"] = "atendente"

            from fluxos.atendente import fluxo_atendente
            return f"""
✅ Interesse registrado: {session["dados"]["plano"]}

Um consultor empresarial irá entrar em contato.
"""

        elif mensagem == "2":

            session["etapa"] = "menu"
            return fluxo_planos_empresariais(session, mensagem)

        else:
            return "Escolha 1 ou 2."