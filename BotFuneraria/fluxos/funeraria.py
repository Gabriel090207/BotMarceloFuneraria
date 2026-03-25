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
    # NORMALIZA BOTÕES
    # -------------------------

    if mensagem == "Voltar":
        mensagem = "0"
    elif mensagem == "Menu principal":
        mensagem = "00"

    # -------------------------
    # FUNÇÃO MUDAR ETAPA
    # -------------------------

    def mudar_etapa(session, nova_etapa):
        etapa_atual = session.get("etapa")

        if etapa_atual:
            session["historico"].append(etapa_atual)

        session["etapa"] = nova_etapa

    # -------------------------
    # VOLTAR INTELIGENTE
    # -------------------------

    def voltar(session):
        if session.get("historico"):
            etapa_anterior = session["historico"].pop()
        else:
            etapa_anterior = "menu"

        # regra especial
        if etapa_anterior == "endereco":
            session["subfluxo"] = None
            session["etapa"] = "menu"
            return fluxo_funeraria(session, "")

        session["etapa"] = etapa_anterior
        return fluxo_funeraria(session, "")

    # -------------------------
    # MENU PRINCIPAL
    # -------------------------

    def menu_principal():
        session["fluxo"] = None
        session["etapa"] = "inicio"
        session["subfluxo"] = None
        session["historico"] = []

        return {
            "tipo": "botoes",
            "mensagem": """🔙 Voltamos ao menu principal

Escolha uma opção:""",
            "botoes": [
                {"id": "1", "label": "Serviços funerários"},
                {"id": "2", "label": "Planos familiares"},
                {"id": "3", "label": "Planos empresariais"},
                {"id": "4", "label": "Floricultura"},
                {"id": "5", "label": "Falar com atendente"},
            ]
        }

    # -------------------------
    # INICIO
    # -------------------------

    if session["etapa"] == "inicio":

        mudar_etapa(session, "menu")

        return {
            "tipo": "botoes",
            "mensagem": f"""⚰️ Serviços Funerários

{nome}, como podemos ajudar?""",
            "botoes": [
                {"id": "1", "label": "Sepultamento"},
                {"id": "2", "label": "Cremação"},
                {"id": "3", "label": "Translado"},
                {"id": "4", "label": "Salas de velório"},
                {"id": "5", "label": "Atendente"},
                {"id": "00", "label": "Menu principal"},
            ]
        }

    # -------------------------
    # MENU
    # -------------------------

    if session["etapa"] == "menu":

        if mensagem == "00":
            return menu_principal()

        if mensagem == "1":
            session["subfluxo"] = "sepultamento"
            mudar_etapa(session, "endereco")
            return {"tipo": "texto", "mensagem": "📍 Endereço do local:"}

        if mensagem == "2":
            session["subfluxo"] = "cremacao"
            mudar_etapa(session, "endereco")
            return {"tipo": "texto", "mensagem": "📍 Endereço do local:"}

    # -------------------------
    # SUBFLUXO
    # -------------------------

    if session["subfluxo"] in ["sepultamento", "cremacao"]:

        if mensagem == "00":
            return menu_principal()

        if mensagem == "0":
            return voltar(session)

        # ENDEREÇO
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

        # TIPO URNA
        if session["etapa"] == "tipo_urna":

            if mensagem == "0":
                return voltar(session)

            tipos = {
                "1": "simples",
                "2": "intermediaria",
                "3": "premium"
            }

            if mensagem not in tipos:
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            session["tipo_urna"] = tipos[mensagem]
            mudar_etapa(session, "lista_urnas")

            urnas = listar_urnas(tipos[mensagem])

            if not urnas:
                return {"tipo": "texto", "mensagem": "Nenhuma urna disponível"}

            session["urnas"] = urnas

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

        # LISTA URNAS
        if session["etapa"] == "lista_urnas":

            if mensagem == "0":
                return voltar(session)

            try:
                urna = session["urnas"][int(mensagem)-1]
            except:
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            session["urna"] = urna
            mudar_etapa(session, "confirmar")

            respostas = []

            for img in urna.get("imagens", []):
                respostas.append({
                    "tipo": "imagem",
                    "url": img
                })

            respostas.append({
                "tipo": "botoes",
                "mensagem": f"""🪦 {urna['nome']}
💰 {formatar_reais(urna['preco'])}""",
                "botoes": [
                    {"id": "1", "label": "Confirmar"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            })

            return respostas

        # CONFIRMAR
        if session["etapa"] == "confirmar":

            if mensagem == "0":
                return voltar(session)

            if mensagem != "1":
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            total = float(session["urna"]["preco"])
            mudar_etapa(session, "final")

            return {
                "tipo": "botoes",
                "mensagem": f"""Resumo

Urna: {session['urna']['nome']}
Valor: {formatar_reais(total)}""",
                "botoes": [
                    {"id": "1", "label": "Confirmar pedido"},
                    {"id": "2", "label": "Refazer"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        # FINAL
        if session["etapa"] == "final":

            if mensagem == "2":
                session["etapa"] = "inicio"
                session["historico"] = []
                return {"tipo": "texto", "mensagem": "Reiniciando atendimento..."}

            if mensagem == "00":
                return menu_principal()

            if mensagem == "1":

                salvar_pedido({
                    "tipo": session["subfluxo"],
                    "telefone": session.get("numero"),
                    "nome": session.get("nome"),
                    "urna": session["urna"],
                    "status": "novo",
                    "criado_em": datetime.now().isoformat()
                })

                session["encerrar_bot"] = True

                return {
                    "tipo": "texto",
                    "mensagem": "✅ Pedido registrado! Em breve entraremos em contato."
                }

    return {"tipo": "texto", "mensagem": "Escolha válida."}

