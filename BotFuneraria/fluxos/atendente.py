def fluxo_atendente(session, mensagem):

    session["fluxo"] = "atendente"
    session["etapa"] = "finalizado"
    session["encerrar_bot"] = True

    nome = session.get("nome", "")

    if nome:
        return f"""
👨‍💼 Atendimento humano

{name}, sua solicitação foi enviada com sucesso.

Em breve um atendente entrará em contato para continuar o atendimento.
"""
    else:
        return """
👨‍💼 Atendimento humano

Sua solicitação foi enviada com sucesso.

Em breve um atendente entrará em contato para continuar o atendimento.
"""