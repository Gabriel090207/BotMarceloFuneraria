def fluxo_atendente(session, mensagem):

    session["etapa"] = "finalizado"

    return """
👨‍💼 Atendimento humano

Sua solicitação foi enviada.

Em breve um atendente iniciará o atendimento.
"""