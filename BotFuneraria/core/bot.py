from core.session import get_session
from datetime import datetime

from fluxos.floricultura import fluxo_floricultura
from fluxos.funeraria import fluxo_funeraria
from fluxos.atendente import fluxo_atendente
from fluxos.planos_familiares import fluxo_planos_familiares
from fluxos.planos_empresariais import fluxo_planos_empresariais


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

    # ---------------------------
    # INICIO
    # ---------------------------

    if session["etapa_global"] == "inicio":

        hora = datetime.now().hour

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

    # ---------------------------
    # NOME
    # ---------------------------

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
                {"id": "2", "label": "Planos familiares"},
                {"id": "3", "label": "Planos empresariais"},
                {"id": "4", "label": "Floricultura"},
                {"id": "5", "label": "Falar com atendente"},
            ]
        }

    # ---------------------------
    # MENU PRINCIPAL
    # ---------------------------

    if session["etapa_global"] == "menu" and session["fluxo"] is None:

        if mensagem == "1":
            session["fluxo"] = "funeraria"
            session["etapa"] = "inicio"  # 🔥 ESSENCIAL
            return fluxo_funeraria(session, mensagem)

        elif mensagem == "2":
            session["fluxo"] = "planos_familiares"
            session["etapa"] = "inicio"
            return fluxo_planos_familiares(session, mensagem)

        elif mensagem == "3":
            session["fluxo"] = "planos_empresariais"
            session["etapa"] = "inicio"
            return fluxo_planos_empresariais(session, mensagem)

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

    # ---------------------------
    # REDIRECIONAMENTO
    # ---------------------------

    if session["fluxo"] == "funeraria":
        return fluxo_funeraria(session, mensagem)

    if session["fluxo"] == "floricultura":
        return fluxo_floricultura(session, mensagem)

    if session["fluxo"] == "atendente":
        return fluxo_atendente(session, mensagem)

    if session["fluxo"] == "planos_familiares":
        return fluxo_planos_familiares(session, mensagem)

    if session["fluxo"] == "planos_empresariais":
        return fluxo_planos_empresariais(session, mensagem)