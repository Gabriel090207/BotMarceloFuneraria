def fluxo_atendente(session, mensagem):

    session["fluxo"] = "atendente"
    session["etapa"] = "finalizado"
    session["encerrar_bot"] = True

    nome = session.get("nome", "")

    if nome:
        return {
            "tipo": "texto",
            "mensagem": f"""👨‍💼 Atendimento humano

{nome}, sua solicitação foi enviada com sucesso.

Em breve um atendente entrará em contato para continuar o atendimento."""
        }
    else:
        return {
            "tipo": "texto",
            "mensagem": """👨‍💼 Atendimento humano

Sua solicitação foi enviada com sucesso.

Em breve um atendente entrará em contato para continuar o atendimento."""
        }