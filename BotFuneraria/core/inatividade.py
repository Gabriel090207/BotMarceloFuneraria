import time
from threading import Thread

from core.sessoes import sessoes
from core.avisos import enviar_aviso_interno
from integracoes.zapi import enviar_texto

TEMPO_LIMITE = 180  # 3 minutos


def gerar_resumo(session):

    dados = session.get("dados", {})

    linhas = [
        f"👤 Nome: {session.get('nome', '-')}",
        f"📞 Telefone: {session.get('numero', '-')}",
        f"📍 Fluxo: {session.get('fluxo', '-')}",
    ]

    for chave, valor in dados.items():
        if valor:
            linhas.append(f"• {chave}: {valor}")

    return linhas


def verificar_inatividade():

    while True:

        agora = time.time()

        for numero, session in list(sessoes.items()):

            ultima = session.get("ultima_interacao")

            if not ultima:
                continue

            # evita duplicidade
            if session.get("inatividade_notificada"):
                continue

            tempo_parado = agora - ultima

            if tempo_parado >= TEMPO_LIMITE:

                # evita aviso vazio
                if not session.get("dados"):
                    continue

                linhas = gerar_resumo(session)

                enviar_aviso_interno(
                    "Cliente parou no meio do atendimento",
                    linhas
                )

                enviar_texto(
                    numero,
                    """👤 Percebemos que o atendimento foi interrompido.

📲 Nosso plantonista pode continuar seu atendimento diretamente pelo WhatsApp:
https://wa.me/5592995131313

ℹ️ As informações já foram encaminhadas para nossa equipe."""
                )

                # marca como notificado
                session["inatividade_notificada"] = True

                # limpa sessão
                session["historico"] = []
                session["dados"] = {}
                session["fluxo"] = None
                session["etapa"] = "inicio"

        time.sleep(15)


def iniciar_monitor():

    thread = Thread(
        target=verificar_inatividade,
        daemon=True
    )

    thread.start()

