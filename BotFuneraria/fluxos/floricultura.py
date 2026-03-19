from core.menus import criar_menu


def fluxo_floricultura(session, mensagem):

    if "etapa" not in session:
        session["etapa"] = "inicio"

    nome = session.get("nome", "")

    # -------------------------
    # INICIO
    # -------------------------

    if session["etapa"] == "inicio":

        session["etapa"] = "menu"

        return criar_menu(
            f"🌸 Floricultura\n\n{nome}, nosso atendimento de flores é realizado separadamente.",
            [
                ("1", "Acessar site da floricultura"),
                ("2", "Falar com a floricultura"),
                ("3", "Falar com atendente"),
                ("0", "Voltar ao menu principal"),
            ],
        )

    # -------------------------
    # MENU
    # -------------------------

    if session["etapa"] == "menu":

        if mensagem == "1":

            return """
🌐 Acesse nosso site:

https://floriculturavalledasflores.com.br
"""

        elif mensagem == "2":

            return """
📱 Fale diretamente com a floricultura:

(INSIRA AQUI O NÚMERO)

Ex: https://wa.me/5511999999999
"""

        elif mensagem == "3":

            session["fluxo"] = "atendente"

            from fluxos.atendente import fluxo_atendente
            return fluxo_atendente(session, mensagem)

        elif mensagem == "0":

            session["fluxo"] = None
            session["etapa"] = "inicio"

            return "Voltando ao menu principal..."

        else:

            return "Escolha uma opção válida."