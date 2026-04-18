from core.session import get_session
from datetime import datetime
import pytz

from fluxos.floricultura import fluxo_floricultura
from fluxos.funeraria import fluxo_funeraria
from fluxos.atendente import fluxo_atendente
from fluxos.planos_familiares import fluxo_planos_familiares
from fluxos.financeiro import fluxo_financeiro
from fluxos.funeraria_orcamento import fluxo_funeraria_orcamento

def responder(numero, mensagem):

    session = get_session(numero)
    session["numero"] = numero

    if session.get("encerrar_bot") is True:
        return None

    if "etapa_global" not in session:
        session["etapa_global"] = "inicio"

    if "nome" not in session:
        session["nome"] = None

    if "fluxo" not in session:
        session["fluxo"] = None

    # -------------------------------------------------
    # INÍCIO
    # -------------------------------------------------

    if session["etapa_global"] == "inicio":

        fuso = pytz.timezone("America/Sao_Paulo")
        hora = datetime.now(fuso).hour

        if hora < 12:
            saudacao = "Bom dia"
        elif hora < 18:
            saudacao = "Boa tarde"
        else:
            saudacao = "Boa noite"

        session["etapa_global"] = "nome"

        return {
            "tipo": "texto",
            "mensagem": f"""
{saudacao}, seja bem-vindo à nossa funerária 🙏

Antes de iniciar o atendimento, poderia me informar seu nome?
"""
        }

    # -------------------------------------------------
    # NOME
    # -------------------------------------------------

    if session["etapa_global"] == "nome":

        session["nome"] = mensagem.strip().title()
        session["etapa_global"] = "menu"

        nome = session["nome"]

        return {
            "tipo": "botoes",
            "mensagem": f"""
Prazer, {nome} 🙏

Como podemos te ajudar hoje?
""",
            "botoes": [
                {"id": "1", "label": "Serviços funerários"},
                {"id": "2", "label": "Planos"},
                {"id": "3", "label": "Financeiro / Administrativo"},
                {"id": "4", "label": "Floricultura"},
                {"id": "5", "label": "Falar com atendente"},
            ]
        }

    # -------------------------------------------------
    # MENU PRINCIPAL
    # -------------------------------------------------

    if session["etapa_global"] == "menu" and session["fluxo"] is None:

        if mensagem == "1":
            session["fluxo"] = "funeraria"
            session["etapa"] = "inicio"
            return fluxo_funeraria(session, mensagem)

        elif mensagem == "2":
            session["fluxo"] = "planos"
            session["etapa"] = "inicio"
            return fluxo_planos_familiares(session, mensagem)

        elif mensagem == "3":
            session["fluxo"] = "financeiro"
            session["etapa"] = "inicio"
            return fluxo_financeiro(session, mensagem)

        elif mensagem == "4":
            session["fluxo"] = "floricultura"
            session["etapa"] = "inicio"
            return fluxo_floricultura(session, mensagem)

        elif mensagem == "5":
            session["fluxo"] = "atendente"
            session["etapa"] = "inicio"
            return fluxo_atendente(session, mensagem)

        else:
            return {
                "tipo": "texto",
                "mensagem": "Escolha uma opção válida."
            }

    # -------------------------------------------------
    # REDIRECIONAMENTOS
    # -------------------------------------------------

    if session["fluxo"] == "funeraria":
        return fluxo_funeraria(session, mensagem)

    if session["fluxo"] == "funeraria_orcamento":
        return fluxo_funeraria_orcamento(session, mensagem)

    if session["fluxo"] == "planos":
        return fluxo_planos_familiares(session, mensagem)

    if session["fluxo"] == "floricultura":
        return fluxo_floricultura(session, mensagem)

    if session["fluxo"] == "atendente":
        return fluxo_atendente(session, mensagem)

    if session["fluxo"] == "financeiro":
        return fluxo_financeiro(session, mensagem)

    return {
        "tipo": "texto",
        "mensagem": "Escolha uma opção válida."
    }