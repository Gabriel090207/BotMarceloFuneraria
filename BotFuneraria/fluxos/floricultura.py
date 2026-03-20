def fluxo_floricultura(session, mensagem):

    if "etapa" not in session:
        session["etapa"] = "inicio"

    nome = session.get("nome", "")

    # -------------------------
    # INICIO
    # -------------------------

    if session["etapa"] == "inicio":

        session["etapa"] = "menu"

        return {
            "tipo": "botoes",
            "mensagem": f"""🌸 Floricultura

{nome}, nosso atendimento de flores é realizado separadamente.""",
            "botoes": [
                {"id": "1", "label": "Acessar site"},
                {"id": "2", "label": "Falar com floricultura"},
                {"id": "3", "label": "Falar com atendente"},
                {"id": "0", "label": "Voltar ao menu"},
            ]
        }

    # -------------------------
    # MENU
    # -------------------------

    if session["etapa"] == "menu":

        if mensagem == "1":

            return {
                "tipo": "texto",
                "mensagem": """🌐 Acesse nosso site:

https://floriculturavalledasflores.com.br"""
            }

        elif mensagem == "2":

            return {
                "tipo": "texto",
                "mensagem": """📱 Fale diretamente com a floricultura:

(INSIRA AQUI O NÚMERO)

Ex: https://wa.me/5511999999999"""
            }

        elif mensagem == "3":

            session["fluxo"] = "atendente"

            from fluxos.atendente import fluxo_atendente
            return fluxo_atendente(session, mensagem)

        elif mensagem == "0":

            session["fluxo"] = None
            session["etapa"] = "inicio"

            return {
                "tipo": "texto",
                "mensagem": "Voltando ao menu principal..."
            }

        else:

            return {
                "tipo": "texto",
                "mensagem": "Escolha uma opção válida."
            }