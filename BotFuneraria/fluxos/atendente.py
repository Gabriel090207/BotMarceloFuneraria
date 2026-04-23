from core.avisos import aviso_atendente


def fluxo_atendente(session, mensagem):

    session["fluxo"] = "atendente"
    session["etapa"] = "finalizado"
    session["encerrar_bot"] = True

    origem = session.get("origem_atendimento", "Menu principal")

    aviso_atendente(
        session.get("nome"),
        session.get("numero"),
        origem
    )

    nome = session.get("nome", "")

    aviso_horario = ""

    if origem not in [
        "Abertura de Sinistro",
        "Convênio - Abertura de Sinistro",
        "Comprovante / Finalização funerária",
        "Funerária"
    ]:
        aviso_horario = """

⏰ Atendimento para planos, convênios e assuntos administrativos ocorre em horário comercial.

Mensagens enviadas fora desse período serão respondidas no próximo horário útil."""

    if nome:
        return {
            "tipo": "texto",
            "mensagem": f"""👤 Atendimento humano

{nome}, sua solicitação foi enviada com sucesso.

Em breve um atendente entrará em contato para continuar o atendimento.{aviso_horario}"""
        }

    return {
        "tipo": "texto",
        "mensagem": f"""👤 Atendimento humano

Sua solicitação foi enviada com sucesso.

Em breve um atendente entrará em contato para continuar o atendimento.{aviso_horario}"""
    }