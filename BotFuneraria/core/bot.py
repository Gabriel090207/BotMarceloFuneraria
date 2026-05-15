from core.session import get_session
from datetime import datetime
import pytz

from fluxos.floricultura import fluxo_floricultura
from fluxos.funeraria import fluxo_funeraria
from fluxos.atendente import fluxo_atendente
from fluxos.planos_familiares import fluxo_planos_familiares
from fluxos.financeiro import fluxo_financeiro
from fluxos.funeraria_orcamento import fluxo_funeraria_orcamento
from fluxos.convenios import fluxo_convenios
from fluxos.planos_sinistro import fluxo_planos_sinistro

SAUDACOES = [
    "oi", "ola", "olá", "bom dia", "boa tarde",
    "boa noite", "hey", "eai", "opa", "menu"
]


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
{saudacao}, bem-vindo(a) à Funerária Canaã 🕊️

🤖 Este é nosso atendimento automático 24h exclusivo via WhatsApp.

📞 Caso prefira ligação ou atendimento humano imediato, fale com nosso plantonista:

➡️ Falar com plantonista:
https://wa.me/5592995131313

ℹ️ Ao final do atendimento, você também poderá ser direcionado para nossa equipe humana para continuidade, envio de comprovantes e finalização do serviço.

Antes de iniciar, poderia me informar seu nome? 🙏
        """
        }

    # -------------------------------------------------
    # NOME
    # -------------------------------------------------

    if session["etapa_global"] == "nome":

        texto = mensagem.strip().lower()

        if texto in SAUDACOES:
            return {
                "tipo": "texto",
                "mensagem": "Para continuar o atendimento, poderia me informar seu nome, por favor? 🙏"
            }

        if len(texto) <= 1:
            return {
                "tipo": "texto",
                "mensagem": "Não consegui identificar. Pode me informar seu nome, por favor? 🙏"
            }

        session["nome"] = mensagem.strip().title()
        session["etapa_global"] = "menu"

        nome = session["nome"]

        return {
            "tipo": "botoes",
            "mensagem": f"""Prazer, {nome} 🙏

Como podemos te ajudar hoje?""",
            "botoes": [
                {"id": "1", "label": "⚰️ Serviços funerários"},
                {"id": "2", "label": "🛡️ Planos"},
                {"id": "3", "label": "🗃️ Convênios"},
                {"id": "4", "label": "💼 Financeiro / Administrativo"},
                {"id": "5", "label": "🌷 Floricultura"},
                {"id": "6", "label": "📍 Localização"},
                {"id": "7", "label": "👤 Falar com atendente"},
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
            session["fluxo"] = "convenios"
            session["etapa"] = "inicio"
            return fluxo_convenios(session, mensagem)

        elif mensagem == "4":
            session["fluxo"] = "financeiro"
            session["etapa"] = "inicio"
            return fluxo_financeiro(session, mensagem)

        elif mensagem == "5":
            session["fluxo"] = "floricultura"
            session["etapa"] = "inicio"
            return fluxo_floricultura(session, mensagem)

        elif mensagem == "6":
            session["fluxo"] = "localizacao"
            session["etapa"] = "mostrar"

            return {
                "tipo": "botoes",
                "mensagem": """📍 *Nossa localização*

Rua Major Gabriel, 1833
Centro - Manaus/AM
CEP 69.020-060

🗺️ Abra no mapa:
https://www.google.com/maps/search/?api=1&query=Rua+Major+Gabriel,+1833+Manaus+AM""",
                "botoes": [
                    {"id": "0", "label": "Menu Principal"},
                ]
            }

        elif mensagem == "7":

            return {
                "tipo": "botoes",
                "mensagem": """👤 *Atendimento Humano*

Você pode falar diretamente com nosso plantonista pelo WhatsApp:

📲 https://wa.me/5592995131313

ℹ️ Nosso atendimento automático continua disponível 24h.

Solicitações administrativas, financeiras e demais setores serão respondidas em horário comercial.""",
                "botoes": [
                    {"id": "00", "label": "Menu principal"},
                ]
            }

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

    if session["fluxo"] == "planos_sinistro":
        return fluxo_planos_sinistro(session, mensagem)

    if session["fluxo"] == "convenios":
        return fluxo_convenios(session, mensagem)

    if session["fluxo"] == "floricultura":
        return fluxo_floricultura(session, mensagem)

    if session["fluxo"] == "atendente":
        return fluxo_atendente(session, mensagem)

    if session["fluxo"] == "financeiro":
        return fluxo_financeiro(session, mensagem)

    if session["fluxo"] == "localizacao":

        if mensagem == "0" or mensagem == "Voltar":
            session["fluxo"] = None
            session["etapa_global"] = "menu"
            session["etapa"] = "inicio"

            return {
                "tipo": "botoes",
                "mensagem": "🕊️ Voltamos ao menu principal.\n\nEscolha uma opção:",
                "botoes": [
                    {"id": "1", "label": "⚰️ Serviços funerários"},
                    {"id": "2", "label": "🛡️ Planos"},
                    {"id": "3", "label": "🗃️ Convênios"},
                    {"id": "4", "label": "💼 Financeiro / Administrativo"},
                    {"id": "5", "label": "🌷 Floricultura"},
                    {"id": "6", "label": "📍 Localização"},
                    {"id": "7", "label": "👤 Falar com atendente"},
                ]
            }

    return {
        "tipo": "texto",
        "mensagem": "Escolha uma opção válida."
    }