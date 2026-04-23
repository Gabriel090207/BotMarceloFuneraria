from datetime import datetime, timedelta
from core.avisos import aviso_atendente


def fluxo_planos_sinistro(session, mensagem):

    session.setdefault("etapa", "inicio")
    session.setdefault("historico", [])
    session.setdefault("dados", {})

    # =================================================
    # AUXILIARES
    # =================================================

    def ir_para(nova):
        atual = session.get("etapa")
        if atual:
            session["historico"].append(atual)
        session["etapa"] = nova

    def voltar():

        # PRIMEIRA TELA DO SINISTRO -> VOLTA PARA MENU PLANOS
        if session.get("etapa") == "velorio" and not session["historico"]:
            nome = session.get("nome", "")
            session["fluxo"] = "planos"
            session["etapa"] = "menu"

            return {
                "tipo": "botoes",
                "mensagem": f"""🛡️ Planos

{nome}, escolha uma opção:""",
                "botoes": [
                    {"id": "1", "label": "Ver planos disponíveis"},
                    {"id": "2", "label": "Contrato Futuro"},
                    {"id": "3", "label": "Abertura de Sinistro"},
                    {"id": "4", "label": "🕊️ Sou cliente"},
                    {"id": "5", "label": "🤝 Indique e ganhe"},
                    {"id": "6", "label": "🧾 Desconto com parceiros"},
                    {"id": "9", "label": "Falar com atendente"},
                    {"id": "00", "label": "Voltar ao menu"},
                ]
            }

        # ETAPAS INTERNAS
        if session["historico"]:
            session["etapa"] = session["historico"].pop()
        else:
            session["etapa"] = "velorio"

        return renderizar()

    def menu():
        session["fluxo"] = None
        session["etapa_global"] = "menu"
        session["historico"] = []
        session["etapa"] = "inicio"

        return {
            "tipo": "botoes",
            "mensagem": "🕊️ Voltamos ao menu principal.\n\nEscolha uma opção:",
            "botoes": [
                {"id": "1", "label": "Serviços funerários"},
                {"id": "2", "label": "Planos"},
                {"id": "3", "label": "🗃️ Convênios"},
                {"id": "4", "label": "Financeiro / Administrativo"},
                {"id": "5", "label": "Floricultura"},
                {"id": "6", "label": "📍 Localização"},
                {"id": "7", "label": "Falar com atendente"},
            ]
        }

    def botao_voltar_menu(lista):
        return lista + [
            {"id": "0", "label": "Voltar"},
            {"id": "00", "label": "Menu principal"},
        ]

    def finalizar():
        aviso_atendente(
            session.get("nome"),
            session.get("numero"),
            "Abertura de Sinistro"
        )

        session["encerrar_bot"] = True
        session["fluxo"] = "atendente"

        return {
            "tipo": "texto",
            "mensagem": "🙏 Recebemos as informações. Você será encaminhado para nosso atendimento."
        }

    # =================================================
    # RENDER
    # =================================================

    def renderizar():
        etapa = session["etapa"]

        if etapa == "inicio":
            session["etapa"] = "velorio"
            return renderizar()

        if etapa == "velorio":
            return {
                "tipo": "botoes",
                "mensagem": "🕯️ Haverá velório?",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Sim"},
                    {"id": "2", "label": "Não"},
                ])
            }

        if etapa == "local_velorio":
            return {
                "tipo": "botoes",
                "mensagem": "🏛️ Onde será o velório?",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Na funerária"},
                    {"id": "2", "label": "Igreja / Residência"},
                ])
            }

        if etapa == "endereco_velorio":
            return {
                "tipo": "texto",
                "mensagem": "📍 Informe o endereço do velório."
            }

        if etapa == "data_velorio":
            return {
                "tipo": "botoes",
                "mensagem": "📅 Qual a data desejada?",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Hoje"},
                    {"id": "2", "label": "Amanhã"},
                    {"id": "3", "label": "Outro"},
                ])
            }

        if etapa == "data_digitada":
            return {
                "tipo": "texto",
                "mensagem": "📅 Digite a data desejada (ex: 25/04/2026)."
            }

        if etapa == "local_corpo":
            return {
                "tipo": "botoes",
                "mensagem": "📍 Onde o ente querido se encontra?",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Hospital"},
                    {"id": "2", "label": "Residência"},
                    {"id": "3", "label": "IML"},
                    {"id": "4", "label": "Outro"},
                ])
            }

        if etapa == "hospital_nome":
            return {
                "tipo": "texto",
                "mensagem": "🏥 Qual o nome do hospital?"
            }

        if etapa == "hospital_liberacao":
            return {
                "tipo": "botoes",
                "mensagem": "O ente querido já foi liberado no necrotério?",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Sim"},
                    {"id": "2", "label": "Não"},
                ])
            }

        if etapa == "endereco_local":
            return {
                "tipo": "texto",
                "mensagem": "📍 Informe o endereço atual."
            }

        if etapa == "destino":
            return {
                "tipo": "botoes",
                "mensagem": "🪦 Qual o destino final?",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Jazigo particular"},
                    {"id": "2", "label": "Sem jazigo particular"},
                    {"id": "3", "label": "Cremação"},
                    {"id": "4", "label": "Translado"},
                ])
            }

        if etapa == "cemiterio":
            return {
                "tipo": "texto",
                "mensagem": "🪦 Qual o nome do cemitério?"
            }

        if etapa == "porte":
            return {
                "tipo": "botoes",
                "mensagem": "⚖️ Qual o porte aproximado?",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Até 85kg"},
                    {"id": "2", "label": "Entre 85kg e 130kg"},
                    {"id": "3", "label": "Acima de 130kg"},
                ])
            }

        return {"tipo": "texto", "mensagem": "Etapa não encontrada."}

    # =================================================
    # GLOBAL
    # =================================================

    if mensagem == "Voltar":
        mensagem = "0"

    if mensagem == "Menu principal":
        mensagem = "00"

    if mensagem == "0":
        return voltar()

    if mensagem == "00":
        return menu()

    if session["etapa"] == "inicio":
        return renderizar()

    # =================================================
    # FLUXO
    # =================================================

    if session["etapa"] == "velorio":
        if mensagem == "1":
            session["dados"]["velorio"] = "Sim"
            ir_para("local_velorio")
            return renderizar()

        if mensagem == "2":
            session["dados"]["velorio"] = "Não"
            ir_para("data_velorio")
            return renderizar()

        return renderizar()

    if session["etapa"] == "local_velorio":
        if mensagem == "1":
            session["dados"]["local_velorio"] = "Funerária"
            ir_para("data_velorio")
            return renderizar()

        if mensagem == "2":
            session["dados"]["local_velorio"] = "Igreja / Residência"
            ir_para("endereco_velorio")
            return renderizar()

        return renderizar()

    if session["etapa"] == "endereco_velorio":
        session["dados"]["endereco_velorio"] = mensagem
        ir_para("data_velorio")
        return renderizar()

    if session["etapa"] == "data_velorio":
        if mensagem == "1":
            session["dados"]["data_velorio"] = datetime.now().strftime("%d/%m/%Y")
            ir_para("local_corpo")
            return renderizar()

        if mensagem == "2":
            amanha = datetime.now() + timedelta(days=1)
            session["dados"]["data_velorio"] = amanha.strftime("%d/%m/%Y")
            ir_para("local_corpo")
            return renderizar()

        if mensagem == "3":
            ir_para("data_digitada")
            return renderizar()

        return renderizar()

    if session["etapa"] == "data_digitada":
        session["dados"]["data_velorio"] = mensagem
        ir_para("local_corpo")
        return renderizar()

    if session["etapa"] == "local_corpo":

        if mensagem == "1":
            session["dados"]["local_corpo"] = "Hospital"
            ir_para("hospital_nome")
            return renderizar()

        if mensagem == "2":
            session["dados"]["local_corpo"] = "Residência"
            ir_para("endereco_local")
            return renderizar()

        if mensagem == "3":
            session["dados"]["local_corpo"] = "IML"
            ir_para("destino")
            return renderizar()

        if mensagem == "4":
            session["dados"]["local_corpo"] = "Outro"
            ir_para("endereco_local")
            return renderizar()

        return renderizar()

    if session["etapa"] == "hospital_nome":
        session["dados"]["hospital_nome"] = mensagem
        ir_para("hospital_liberacao")
        return renderizar()

    if session["etapa"] == "hospital_liberacao":
        if mensagem in ["1", "2"]:
            session["dados"]["liberacao_hospital"] = "Sim" if mensagem == "1" else "Não"
            ir_para("destino")
            return renderizar()

        return renderizar()

    if session["etapa"] == "endereco_local":
        session["dados"]["endereco_local"] = mensagem
        ir_para("destino")
        return renderizar()

    if session["etapa"] == "destino":

        if mensagem == "1":
            session["dados"]["destino"] = "Jazigo particular"
            ir_para("cemiterio")
            return renderizar()

        if mensagem == "2":
            session["dados"]["destino"] = "Sem jazigo particular"
            ir_para("porte")
            return renderizar()

        if mensagem == "3":
            session["dados"]["destino"] = "Cremação"
            ir_para("porte")
            return renderizar()

        if mensagem == "4":
            session["dados"]["destino"] = "Translado"
            ir_para("porte")
            return renderizar()

        return renderizar()

    if session["etapa"] == "cemiterio":
        session["dados"]["cemiterio"] = mensagem
        ir_para("porte")
        return renderizar()

    if session["etapa"] == "porte":
        if mensagem in ["1", "2", "3"]:
            session["dados"]["porte"] = mensagem
            return finalizar()

        return renderizar()

    return renderizar()