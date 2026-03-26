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
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        etapa_anterior = session["historico"].pop()
        session["etapa"] = etapa_anterior

        if etapa_anterior == "pagamento":
            dados = session.get("dados", {})
            urna = session.get("urna", {})

            resumo = f"""📋 *Resumo do pedido*

📍 Endereço: {dados.get("endereco", "-")}
⚖️ Porte: {dados.get("porte_corpo", "-")}
🕯️ Velório: {dados.get("velorio", "-")}
📅 Data: {dados.get("data", "-")}
⏰ Horário: {dados.get("horario", "-")}
🚐 Translado: {dados.get("tera_translado", "-")}
"""

            if dados.get("tera_translado") == "sim":
                resumo += f"""📍 Origem: {dados.get("origem_translado", "-")}
📍 Destino: {dados.get("destino_translado", "-")}
⏰ Horário translado: {dados.get("horario_translado", "-")}"""

            resumo += f"""

🪦 Urna: {urna.get("nome", "-")}
💰 Valor: {formatar_reais(urna.get("preco", 0))}
"""

            return {
                "tipo": "botoes",
                "mensagem": resumo,
                "botoes": [
                    {"id": "1", "label": "Confirmar pedido"},
                    {"id": "2", "label": "Editar"},
                    {"id": "0", "label": "Voltar"},
                ]
            }

        if not session.get("historico"):
            session["etapa"] = "menu"
            session["subfluxo"] = None

            return {
                "tipo": "botoes",
                "mensagem": "Voltando ao menu...",
                "botoes": [
                    {"id": "1", "label": "Sepultamento"},
                    {"id": "2", "label": "Cremação"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        etapa_anterior = session["historico"].pop()
        session["etapa"] = etapa_anterior

        if etapa_anterior == "endereco":
            return {"tipo": "texto", "mensagem": "📍 Onde será o velório?"}

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

            if not urna:
                return {"tipo": "texto", "mensagem": "Erro ao voltar."}

            return {
                "tipo": "botoes",
                "mensagem": f"""🪦 {urna['nome']}
💰 {formatar_reais(urna['preco'])}""",
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

    # -------------------------
    # VOLTAR GLOBAL
    # -------------------------

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
            "mensagem": f"""⚰️ Serviços Funerários

{nome}, como podemos ajudar?""",
            "botoes": [
                {"id": "1", "label": "Sepultamento"},
                {"id": "2", "label": "Cremação"},
                {"id": "3", "label": "Translado"},
                {"id": "4", "label": "Salas de Homenagens"},
                {"id": "5", "label": "Atendente"},
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
            return {"tipo": "texto", "mensagem": "📍 Onde será o velório?"}

        if mensagem == "2":
            session["subfluxo"] = "cremacao"
            mudar_etapa(session, "endereco")
            return {"tipo": "texto", "mensagem": "📍 Onde será o velório?"}


        if mensagem == "3":
            session["subfluxo"] = "translado"
            mudar_etapa(session, "translado_origem")
            return {"tipo": "texto", "mensagem": "📍 Informe o endereço de origem:"}

            
    # -------------------------
    # SUBFLUXO
    # -------------------------

    if session["subfluxo"] in ["sepultamento", "cremacao"]:

        if session["etapa"] == "endereco":
            session["dados"]["local_velorio"] = mensagem
            mudar_etapa(session, "porte_corpo")

            return {
                "tipo": "botoes",
                "mensagem": "⚖️ Qual o porte do corpo?",
                "botoes": [
                    {"id": "1", "label": "Pequeno (até 60kg)"},
                    {"id": "2", "label": "Médio (60kg a 90kg)"},
                    {"id": "3", "label": "Grande (acima de 90kg)"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if session["etapa"] == "porte_corpo":

            portes = {
                "1": "pequeno",
                "2": "medio",
                "3": "grande"
            }

            if mensagem not in portes:
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            session["dados"]["porte_corpo"] = portes[mensagem]
            mudar_etapa(session, "data")

            return {
                "tipo": "botoes",
                "mensagem": "🕯️ Haverá velório?",
                "botoes": [
                    {"id": "1", "label": "Sim"},
                    {"id": "2", "label": "Não"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        

        if session["etapa"] == "data":
            session["dados"]["data"] = mensagem
            mudar_etapa(session, "horario")

            return {
                "tipo": "texto",
                "mensagem": "⏰ Informe o horário (ex: 11:00, 16:30, 20:45):"
            }

        if session["etapa"] == "horario":
            session["dados"]["horario"] = mensagem

            if session["subfluxo"] == "cremacao":
                mudar_etapa(session, "tipo_urna")
            else:
                mudar_etapa(session, "pergunta_translado")

        if session["etapa"] == "pergunta_translado":

            if mensagem == "1":
                session["dados"]["tera_translado"] = "sim"
                mudar_etapa(session, "destino_translado")

                return {
                    "tipo": "texto",
                    "mensagem": "📍 Informe a origem do translado:"
                }

            elif mensagem == "2":
                session["dados"]["tera_translado"] = "nao"
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

            return {"tipo": "texto", "mensagem": "Escolha válida"}

      

        if session["etapa"] == "destino_translado":
            session["dados"]["destino_translado"] = mensagem
            mudar_etapa(session, "horario_translado")

            return {
                "tipo": "texto",
                "mensagem": "⏰ Informe o horário do translado:"
            }

        if session["etapa"] == "horario_translado":
            session["dados"]["horario_translado"] = mensagem
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

            tipos = {
                "1": "simples",
                "2": "intermediaria",
                "3": "premium"
            }

            if mensagem not in tipos:
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            session["tipo_urna"] = tipos[mensagem]
            mudar_etapa(session, "lista_urnas")

            urnas = listar_urnas(
                tipos[mensagem],
                session["subfluxo"]
            )

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

        if session["etapa"] == "lista_urnas":

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

        if session["etapa"] == "confirmar":

            if mensagem != "1":
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            dados = session.get("dados", {})
            urna = session.get("urna", {})

            resumo = f"""📋 *Resumo do pedido*

📍 Local do velório: {dados.get("local_velorio", "-")}
⚖️ Porte: {dados.get("porte_corpo", "-")}
🕯️ Velório: {dados.get("velorio", "-")}
📅 Data: {dados.get("data", "-")}
⏰ Horário: {dados.get("horario", "-")}
\n🚐 Translado: {dados.get("tera_translado", "-")}
"""

            if dados.get("tera_translado") == "sim":
                resumo += f"""📍 Origem: {dados.get("origem_translado", "-")}
📍 Destino: {dados.get("destino_translado", "-")}
⏰ Horário translado: {dados.get("horario_translado", "-")}"""

            resumo += f"""

🪦 Urna: {urna.get("nome", "-")}
💰 Valor: {formatar_reais(urna.get("preco", 0))}
"""

            mudar_etapa(session, "resumo")

            return {
                "tipo": "botoes",
                "mensagem": resumo,
                "botoes": [
                    {"id": "1", "label": "Confirmar pedido"},
                    {"id": "2", "label": "Editar"},
                    {"id": "0", "label": "Voltar"},
                ]
            }

        if session["etapa"] == "resumo":

            if mensagem == "2":
                mudar_etapa(session, "endereco")
                return {"tipo": "texto", "mensagem": "📍 Informe o endereço novamente:"}

            if mensagem != "1":
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            total = float(session["urna"]["preco"])
            sinal = round(total * 0.1, 2)

            session["pagamento"] = {
                "total": total,
                "sinal": sinal
            }

            mudar_etapa(session, "pagamento")

            return {
                "tipo": "botoes",
                "mensagem": f"""💳 *Pagamento da entrada (sinal)*

Para concluir o pedido, solicitamos o pagamento de 10% do valor.

💰 Valor total: {formatar_reais(total)}
💵 Entrada (10%): {formatar_reais(sinal)}

🔑 Chave PIX:
07559544000137

Após pagar, clique em *Já paguei* 👇""",
            "botoes": [
                {"id": "1", "label": "Já paguei"},
                {"id": "0", "label": "Voltar"},
                ]
            }

        if session["etapa"] == "final":

            if mensagem == "2":
                session["etapa"] = "inicio"
                session["historico"] = []
                return {"tipo": "texto", "mensagem": "Reiniciando atendimento..."}

            if mensagem == "1":

                salvar_pedido({
                    "tipo": session["subfluxo"],
                    "telefone": session.get("numero"),
                    "nome": session.get("nome"),
                    "urna": session["urna"],
                    "status": "aberto",
                    "criado_em": datetime.now().isoformat()
                })

                session["encerrar_bot"] = True

                return {
                    "tipo": "texto",
                    "mensagem": "✅ Pedido registrado! Em breve entraremos em contato."
                }

    
    # -------------------------
    # TRANSLADO
    # -------------------------

    if session["subfluxo"] == "translado":

        if session["etapa"] == "translado_origem":
            session["dados"]["origem"] = mensagem
            mudar_etapa(session, "translado_destino")

            return {
                "tipo": "texto",
                "mensagem": "📍 Informe o destino do translado:"
            }

        if session["etapa"] == "translado_destino":
            session["dados"]["destino"] = mensagem
            mudar_etapa(session, "translado_data")

            return {
                "tipo": "texto",
                "mensagem": "📅 Informe a data do translado (ex: 10/02/2026):"
            }

        if session["etapa"] == "translado_data":
            session["dados"]["data"] = mensagem
            mudar_etapa(session, "translado_horario")

            return {
                "tipo": "texto",
                "mensagem": "⏰ Informe o horário do translado (ex: 11:00):"
            }

        if session["etapa"] == "translado_horario":
            session["dados"]["horario"] = mensagem
            mudar_etapa(session, "confirmar_translado")

            return {
                "tipo": "botoes",
                "mensagem": f"""🚐 *Confirmação do translado*

📍 Origem: {session['dados']['origem']}
📍 Destino: {session['dados']['destino']}
📅 Data: {session['dados'].get('data', '-')}
⏰ Horário: {session['dados']['horario']}""",
            "botoes": [
                {"id": "1", "label": "Confirmar"},
                {"id": "0", "label": "Voltar"},
                {"id": "00", "label": "Menu principal"},
            ]
        }

        if session["etapa"] == "confirmar_translado":

            if mensagem != "1":
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            salvar_pedido({
                "tipo": "translado",
                "dados": session.get("dados"),
                "telefone": session.get("numero"),
                "nome": session.get("nome"),
                "status": "aberto",
                "criado_em": datetime.now().isoformat()
            })

            session["encerrar_bot"] = True

            return {
                "tipo": "texto",
                "mensagem": """✅ Pedido de translado registrado!

Nossa equipe continuará o atendimento diretamente com você pelo WhatsApp."""
            }

    # -------------------------
    # PAGAMENTO
    # -------------------------

    if session["etapa"] == "pagamento":

        if mensagem == "1":

            salvar_pedido({
                "tipo": session["subfluxo"],
                "dados": session.get("dados"),
                "urna": session.get("urna"),
                "pagamento": session.get("pagamento"),
                "telefone": session.get("numero"),
                "nome": session.get("nome"),
                "status": "aberto",
                "criado_em": datetime.now().isoformat()
            })

            session["encerrar_bot"] = True

            return {
                "tipo": "texto",
                "mensagem": """📎 *Envio do comprovante*

Recebemos sua confirmação de pagamento.

Agora, por favor, envie o comprovante aqui no WhatsApp para a equipe da funerária.

A partir deste momento, o atendimento seguirá diretamente com nossa equipe."""
            }



    
    return {"tipo": "texto", "mensagem": "Escolha válida."}