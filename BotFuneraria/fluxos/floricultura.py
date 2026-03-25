def fluxo_floricultura(session, mensagem):

    if "etapa" not in session:
        session["etapa"] = "inicio"

    nome = session.get("nome", "")

    # -------------------------
    # NORMALIZA BOTÕES
    # -------------------------

    if mensagem == "Voltar":
        mensagem = "0"
    elif mensagem == "Menu principal":
        mensagem = "00"

    # -------------------------
    # MENU PRINCIPAL
    # -------------------------

    def menu_principal():
        session["fluxo"] = None
        session["etapa"] = "inicio"
        session["etapa_global"] = "menu"

        return {
            "tipo": "botoes",
            "mensagem": """🔙 Voltamos ao menu principal

Escolha uma opção para continuar:""",
            "botoes": [
                {"id": "1", "label": "Serviços funerários"},
                {"id": "2", "label": "Planos familiares"},
                {"id": "3", "label": "Planos empresariais"},
                {"id": "4", "label": "Floricultura"},
                {"id": "5", "label": "Falar com atendente"},
            ]
        }

    # -------------------------
    # VOLTAR DO SITE / CONTATO
    # -------------------------

    if session["etapa"] in ["site", "contato"]:

        if mensagem == "0":
            session["etapa"] = "menu"

            return {
                "tipo": "botoes",
                "mensagem": """🔙 Voltamos para Floricultura

Escolha uma opção:""",
                "botoes": [
                    {"id": "1", "label": "Acessar site"},
                    {"id": "2", "label": "Falar com floricultura"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        elif mensagem == "00":
            return menu_principal()

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
                {"id": "00", "label": "Voltar ao menu"},
            ]
        }

    # -------------------------
    # MENU
    # -------------------------

    if session["etapa"] == "menu":

        if mensagem == "00":
            return menu_principal()

        elif mensagem == "1":

            session["etapa"] = "site"

            return {
                "tipo": "botoes",
                "mensagem": """🌐 Acesse nosso site:

https://floriculturavalledasflores.com.br""",
                "botoes": [
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        elif mensagem == "2":

            session["etapa"] = "contato"

            return {
                "tipo": "botoes",
                "mensagem": """📱 Fale diretamente com a floricultura:

https://wa.me/559281230907""",
                "botoes": [
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        else:
            return {
                "tipo": "texto",
                "mensagem": "Escolha uma opção válida."
            }