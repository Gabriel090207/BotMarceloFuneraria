from datetime import datetime
from core.firebase import salvar_pedido
from core.urnas import listar_urnas
from core.pagamentos import formatar_reais


def fluxo_funeraria(session, mensagem):

    if "etapa" not in session:
        session["etapa"] = "inicio"

    if "historico" not in session:
        session["historico"] = []

    if "dados" not in session:
        session["dados"] = {}

    if "subfluxo" not in session:
        session["subfluxo"] = None

    nome = session.get("nome", "Cliente")

    # -------------------------
    # FUNÇÕES
    # -------------------------

    def mudar_etapa(session, nova_etapa):
        etapa_atual = session.get("etapa")

        if etapa_atual and (not session["historico"] or session["historico"][-1] != etapa_atual):
            session["historico"].append(etapa_atual)

        session["etapa"] = nova_etapa

    def menu_principal():
        session["fluxo"] = None
        session["etapa"] = "inicio"
        session["subfluxo"] = None
        session["historico"] = []

        return {
            "tipo": "botoes",
            "mensagem": "🔙 Voltamos ao menu principal\n\nEscolha uma opção:",
            "botoes": [
                {"id": "1", "label": "Serviços funerários"},
                {"id": "2", "label": "Planos familiares"},
                {"id": "3", "label": "Planos empresariais"},
                {"id": "4", "label": "Floricultura"},
                {"id": "5", "label": "Falar com atendente"},
            ]
        }

    def voltar(session):

        if not session.get("historico"):
            session["etapa"] = "menu"
            session["subfluxo"] = None

            return {
                "tipo": "botoes",
                "mensagem": "Voltando ao menu...",
                "botoes": [
                    {"id": "1", "label": "Sepultamento"},
                    {"id": "2", "label": "Cremação"},
                    {"id": "3", "label": "Salas de velório"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        etapa_anterior = session["historico"].pop()
        session["etapa"] = etapa_anterior

        if etapa_anterior == "endereco":
            return {"tipo": "texto", "mensagem": "📍 Endereço do local:"}

        if etapa_anterior == "tipo_urna":
            return {
                "tipo": "botoes",
                "mensagem": "Escolha o tipo de urna:",
                "botoes": [
                    {"id": "1", "label": "Simples"},
                    {"id": "2", "label": "Intermediária"},
                    {"id": "3", "label": "Premium"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if etapa_anterior == "lista_urnas":
            urnas = session.get("urnas", [])

            botoes = []
            for i, u in enumerate(urnas):
                botoes.append({
                    "id": str(i+1),
                    "label": f"{u['nome']} - {formatar_reais(u['preco'])}"
                })

            botoes += [
                {"id": "0", "label": "Voltar"},
                {"id": "00", "label": "Menu principal"},
            ]

            return {
                "tipo": "botoes",
                "mensagem": "Escolha a urna:",
                "botoes": botoes
            }

        if etapa_anterior == "confirmar":
            urna = session.get("urna")

            return {
                "tipo": "botoes",
                "mensagem": f"🪦 {urna['nome']}\n💰 {formatar_reais(urna['preco'])}",
                "botoes": [
                    {"id": "1", "label": "Confirmar"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        return {"tipo": "texto", "mensagem": "Voltando..."}

    # -------------------------
    # NORMALIZA BOTÕES
    # -------------------------

    if mensagem == "Voltar":
        mensagem = "0"
    elif mensagem == "Menu principal":
        mensagem = "00"

    if mensagem == "0":
        return voltar(session)

    if mensagem == "00":
        return menu_principal()

    # -------------------------
    # INICIO
    # -------------------------

    if session["etapa"] == "inicio":

        mudar_etapa(session, "menu")

        return {
            "tipo": "botoes",
            "mensagem": f"⚰️ Serviços Funerários\n\n{nome}, como podemos ajudar?",
            "botoes": [
                {"id": "1", "label": "Sepultamento"},
                {"id": "2", "label": "Cremação"},
                {"id": "3", "label": "Salas de velório"},
                {"id": "00", "label": "Menu principal"},
            ]
        }

    # -------------------------
    # MENU
    # -------------------------

    if session["etapa"] == "menu":

        if mensagem == "1":
            session["subfluxo"] = "sepultamento"
            mudar_etapa(session, "endereco")
            return {"tipo": "texto", "mensagem": "📍 Endereço do local:"}

        if mensagem == "2":
            session["subfluxo"] = "cremacao"
            mudar_etapa(session, "endereco")
            return {"tipo": "texto", "mensagem": "📍 Endereço do local:"}

        if mensagem == "3":
            session["subfluxo"] = "sala"
            mudar_etapa(session, "data_velorio")
            return {"tipo": "texto", "mensagem": "📅 Informe a data do velório:"}

    # -------------------------
    # SALAS DE VELÓRIO
    # -------------------------

    if session["subfluxo"] == "sala":

        if session["etapa"] == "data_velorio":
            session["dados"]["data"] = mensagem
            mudar_etapa(session, "hora_velorio")
            return {"tipo": "texto", "mensagem": "⏰ Informe o horário:"}

        if session["etapa"] == "hora_velorio":
            session["dados"]["hora"] = mensagem
            mudar_etapa(session, "confirmar_sala")

            return {
                "tipo": "botoes",
                "mensagem": f"""🏢 Reserva de sala

Data: {session['dados']['data']}
Hora: {session['dados']['hora']}""",
                "botoes": [
                    {"id": "1", "label": "Confirmar"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if session["etapa"] == "confirmar_sala":

            if mensagem != "1":
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            salvar_pedido({
                "tipo": "sala_velorio",
                "dados": session["dados"],
                "telefone": session.get("numero"),
                "nome": session.get("nome"),
                "status": "novo",
                "criado_em": datetime.now().isoformat()
            })

            return {"tipo": "texto", "mensagem": "✅ Sala reservada! Entraremos em contato."}

    # -------------------------
    # URNAS
    # -------------------------

    if session["subfluxo"] in ["sepultamento", "cremacao"]:

        if session["etapa"] == "endereco":
            session["dados"]["endereco"] = mensagem
            mudar_etapa(session, "tipo_urna")

            return {
                "tipo": "botoes",
                "mensagem": "Escolha o tipo de urna:",
                "botoes": [
                    {"id": "1", "label": "Simples"},
                    {"id": "2", "label": "Intermediária"},
                    {"id": "3", "label": "Premium"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if session["etapa"] == "tipo_urna":

            tipos = {"1": "simples", "2": "intermediaria", "3": "premium"}

            if mensagem not in tipos:
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            session["tipo_urna"] = tipos[mensagem]
            mudar_etapa(session, "lista_urnas")

            urnas = listar_urnas(tipos[mensagem])
            session["urnas"] = urnas

            botoes = [
                {"id": str(i+1), "label": f"{u['nome']} - {formatar_reais(u['preco'])}"}
                for i, u in enumerate(urnas)
            ]

            botoes += [{"id": "0", "label": "Voltar"}, {"id": "00", "label": "Menu principal"}]

            return {"tipo": "botoes", "mensagem": "Escolha a urna:", "botoes": botoes}

        if session["etapa"] == "lista_urnas":

            try:
                urna = session["urnas"][int(mensagem)-1]
            except:
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            session["urna"] = urna
            mudar_etapa(session, "confirmar")

            return {
                "tipo": "botoes",
                "mensagem": f"🪦 {urna['nome']}\n💰 {formatar_reais(urna['preco'])}",
                "botoes": [
                    {"id": "1", "label": "Confirmar"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if session["etapa"] == "confirmar":

            if mensagem != "1":
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            total = float(session["urna"]["preco"])
            sinal = round(total * 0.1, 2)

            session["pagamento"] = {"total": total, "sinal": sinal}

            mudar_etapa(session, "pagamento")

            return {
                "tipo": "botoes",
                "mensagem": f"""💳 Pagamento via PIX

Total: {formatar_reais(total)}
Entrada (10%): {formatar_reais(sinal)}

PIX:
chavepix@email.com""",
                "botoes": [
                    {"id": "1", "label": "Já paguei"},
                    {"id": "0", "label": "Voltar"},
                ]
            }

        if session["etapa"] == "pagamento":

            if mensagem == "1":
                mudar_etapa(session, "comprovante")
                return {"tipo": "texto", "mensagem": "📎 Envie o comprovante."}

        if session["etapa"] == "comprovante":

            salvar_pedido({
                "tipo": session["subfluxo"],
                "urna": session["urna"],
                "pagamento": session["pagamento"],
                "telefone": session.get("numero"),
                "nome": session.get("nome"),
                "status": "pago",
                "criado_em": datetime.now().isoformat()
            })

            return {"tipo": "texto", "mensagem": "✅ Pedido confirmado! A funerária entrará em contato."}

    return {"tipo": "texto", "mensagem": "Escolha válida."}