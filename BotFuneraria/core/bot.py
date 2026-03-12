from core.session import get_session

from fluxos.floricultura import fluxo_floricultura
from fluxos.funeraria import fluxo_funeraria
from fluxos.atendente import fluxo_atendente


def responder(numero, mensagem):

    session = get_session(numero)

    # MENU PRINCIPAL
    if session["fluxo"] is None:

        if mensagem == "1":

            session["fluxo"] = "floricultura"
            return fluxo_floricultura(session, mensagem)

        elif mensagem == "2":

            session["fluxo"] = "funeraria"
            return fluxo_funeraria(session, mensagem)

        elif mensagem == "3":

            session["fluxo"] = "atendente"
            return fluxo_atendente(session, mensagem)

        else:

            return """
Bem vindo ao atendimento

1 - Floricultura
2 - Funerária
3 - Falar com atendente
"""

    # REDIRECIONA PARA O FLUXO ATUAL

    if session["fluxo"] == "floricultura":
        return fluxo_floricultura(session, mensagem)

    if session["fluxo"] == "funeraria":
        return fluxo_funeraria(session, mensagem)

    if session["fluxo"] == "atendente":
        return fluxo_atendente(session, mensagem)