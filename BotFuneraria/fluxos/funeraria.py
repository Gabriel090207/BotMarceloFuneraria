from datetime import datetime
from core.firebase import salvar_pedido
from core.urnas import listar_urnas
from core.pagamentos import formatar_reais


def fluxo_funeraria(session, mensagem):
    # =========================================================
    # ESTADO INICIAL
    # =========================================================
    session.setdefault("etapa", "inicio")
    session.setdefault("historico", [])
    session.setdefault("dados", {})
    session.setdefault("subfluxo", None)
    session.setdefault("nome", "Cliente")

    # =========================================================
    # FUNÇÕES AUXILIARES
    # =========================================================
    def resetar_fluxo():
        session["etapa"] = "inicio"
        session["historico"] = []
        session["dados"] = {}
        session["subfluxo"] = None
        session.pop("urnas", None)
        session.pop("urna", None)
        session.pop("urnas_cinzas", None)
        session.pop("urna_cinzas", None)
        session.pop("pagamento", None)

    def ir_para(nova_etapa):
        etapa_atual = session.get("etapa")
        if etapa_atual:
            session["historico"].append(etapa_atual)
        session["etapa"] = nova_etapa

    def voltar():
        historico = session.get("historico", [])

        if not historico:
            session["etapa"] = "menu_principal"
            return renderizar_etapa()

        session["etapa"] = historico.pop()
        return renderizar_etapa()

    def ir_menu_principal():
        session["historico"] = []
        session["etapa"] = "menu_principal"
        return renderizar_etapa()

    def botao_voltar_menu(lista_botoes):
        return lista_botoes + [
            {"id": "0", "label": "Voltar"},
            {"id": "00", "label": "Menu principal"},
        ]

    def label_local_corpo(valor):
        mapa = {
            "1": "Hospital",
            "2": "Residência",
            "3": "IML",
            "4": "Outro",
        }
        return mapa.get(valor, valor)

    def label_porte(valor):
        mapa = {
            "1": "Até 70kg",
            "2": "Entre 70kg e 100kg",
            "3": "Acima de 100kg",
        }
        return mapa.get(valor, valor)

    def label_velorio(valor):
        mapa = {
            "1": "Sim",
            "2": "Não",
            "sim": "Sim",
            "nao": "Não",
        }
        return mapa.get(valor, valor)

    def label_local_velorio(valor):
        mapa = {
            "1": "Na Funerária Canaã",
            "2": "Em igreja ou residência",
            "funeraria": "Na Funerária Canaã",
            "externo": "Em igreja ou residência",
        }
        return mapa.get(valor, valor)

    def label_tipo_servico(valor):
        mapa = {
            "1": "Sepultamento",
            "2": "Cremação",
            "sepultamento": "Sepultamento",
            "cremacao": "Cremação",
        }
        return mapa.get(valor, valor)

    def label_cerimonia(valor):
        mapa = {
            "1": "Sim",
            "2": "Não",
            "sim": "Sim",
            "nao": "Não",
        }
        return mapa.get(valor, valor)

    def label_crematorio(valor):
        mapa = {
            "1": "Sim, seguir com crematório parceiro",
            "2": "Prefere outro local",
            "sim": "Sim, seguir com crematório parceiro",
            "outro": "Prefere outro local",
        }
        return mapa.get(valor, valor)

    def obter_resumo():
        dados = session.get("dados", {})
        urna = session.get("urna")
        urna_cinzas = session.get("urna_cinzas")

        linhas = []
        linhas.append("📋 *Resumo do atendimento*")
        linhas.append("")
        linhas.append(f"🕯️ Velório: {label_velorio(dados.get('velorio', '-'))}")

        if dados.get("velorio") == "sim":
            linhas.append(f"🏛️ Local do velório: {label_local_velorio(dados.get('local_velorio', '-'))}")
            if dados.get("local_velorio") == "externo":
                linhas.append(f"📍 Endereço do velório: {dados.get('endereco_velorio', '-')}")
            linhas.append(f"📅 Data do velório: {dados.get('data_velorio', '-')}")
            linhas.append(f"⏰ Horário do velório: {dados.get('horario_velorio', '-')}")

        linhas.append(f"📍 Local do ente querido: {label_local_corpo(dados.get('local_corpo', '-'))}")
        linhas.append(f"📌 Endereço do local atual: {dados.get('endereco_local_corpo', '-')}")
        linhas.append(f"⚖️ Porte aproximado: {label_porte(dados.get('porte', '-'))}")
        linhas.append(f"⚰️ Tipo de serviço: {label_tipo_servico(session.get('subfluxo', '-'))}")

        if session.get("subfluxo") == "sepultamento":
            linhas.append(f"🪦 Cemitério: {dados.get('cemiterio', '-')}")
            if urna:
                linhas.append(f"⚰️ Urna escolhida: {urna.get('nome', '-')}")
                linhas.append(f"💰 Valor da urna: {formatar_reais(float(urna.get('preco', 0)))}")

        elif session.get("subfluxo") == "cremacao":
            linhas.append(f"🙏 Cerimônia na cremação: {label_cerimonia(dados.get('cerimonia_cremacao', '-'))}")
            linhas.append(f"🏢 Crematório: {label_crematorio(dados.get('crematorio', '-'))}")
            if dados.get("crematorio") == "outro":
                linhas.append(f"📍 Local informado: {dados.get('crematorio_outro_nome', '-')}")
            if urna:
                linhas.append(f"⚰️ Urna do velório: {urna.get('nome', '-')}")
                linhas.append(f"💰 Valor da urna do velório: {formatar_reais(float(urna.get('preco', 0)))}")
            if urna_cinzas:
                linhas.append(f"🕊️ Urna de cinzas: {urna_cinzas.get('nome', '-')}")
                linhas.append(f"💰 Valor da urna de cinzas: {formatar_reais(float(urna_cinzas.get('preco', 0)))}")

        return "\n".join(linhas)

    def calcular_pagamento():
        total = 0.0

        if session.get("urna"):
            total += float(session["urna"].get("preco", 0))

        if session.get("urna_cinzas"):
            total += float(session["urna_cinzas"].get("preco", 0))

        sinal = round(total * 0.1, 2)

        session["pagamento"] = {
            "total": total,
            "sinal": sinal
        }

        return total, sinal

    def montar_botoes_urnas(lista):
        botoes = []
        for i, urna in enumerate(lista):
            botoes.append({
                "id": str(i + 1),
                "label": f"{urna['nome']} - {formatar_reais(float(urna['preco']))}"
            })
        return botao_voltar_menu(botoes)

    def renderizar_confirmacao_urna(urna, titulo_botao="Confirmar"):
        respostas = []

        for img in urna.get("imagens", []):
            respostas.append({
                "tipo": "imagem",
                "url": img
            })

        respostas.append({
            "tipo": "botoes",
            "mensagem": f"""🪦 {urna['nome']}
💰 {formatar_reais(float(urna['preco']))}""",
            "botoes": [
                {"id": "1", "label": titulo_botao},
                {"id": "0", "label": "Voltar"},
                {"id": "00", "label": "Menu principal"},
            ]
        })

        return respostas

    # =========================================================
    # RENDERIZAÇÃO DAS ETAPAS
    # =========================================================
    def renderizar_etapa():
        etapa = session.get("etapa")
        nome = session.get("nome", "Cliente")

        if etapa == "menu_principal":
            return {
                "tipo": "botoes",
                "mensagem": f"""⚰️ *Serviços Funerários*

{nome}, o que você procura no momento?""",
                "botoes": [
                    {"id": "1", "label": "Serviços imediatos"},
                    {"id": "2", "label": "Orçamento"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if etapa == "velorio":
            return {
                "tipo": "botoes",
                "mensagem": """Para começarmos com cuidado e organização, você pode me informar:

🕯️ *Haverá velório?*""",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Sim"},
                    {"id": "2", "label": "Não"},
                ])
            }

        if etapa == "local_velorio":
            return {
                "tipo": "botoes",
                "mensagem": """Onde você gostaria de realizar o velório?""",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Na Funerária Canaã"},
                    {"id": "2", "label": "Em igreja ou residência"},
                ])
            }

        if etapa == "endereco_velorio":
            return {
                "tipo": "texto",
                "mensagem": "Pode me informar o endereço completo do local do velório, por favor?"
            }

        if etapa == "data_velorio":
            return {
                "tipo": "texto",
                "mensagem": "📅 Qual a data desejada para o velório?"
            }

        if etapa == "horario_velorio":
            return {
                "tipo": "texto",
                "mensagem": "⏰ E o horário previsto para início?"
            }

        if etapa == "local_corpo":
            return {
                "tipo": "botoes",
                "mensagem": """Para organizarmos o atendimento, onde o ente querido se encontra no momento?""",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Hospital"},
                    {"id": "2", "label": "Residência"},
                    {"id": "3", "label": "IML"},
                    {"id": "4", "label": "Outro"},
                ])
            }

        if etapa == "endereco_local_corpo":
            return {
                "tipo": "texto",
                "mensagem": "📍 Pode me informar o endereço completo desse local, por favor?"
            }

        if etapa == "porte":
            return {
                "tipo": "botoes",
                "mensagem": """Para prepararmos tudo da melhor forma, você pode nos informar o porte aproximado do seu ente querido?""",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Até 70kg"},
                    {"id": "2", "label": "Entre 70kg e 100kg"},
                    {"id": "3", "label": "Acima de 100kg"},
                ])
            }

        if etapa == "tipo_servico":
            return {
                "tipo": "botoes",
                "mensagem": """Como deseja realizar a despedida?""",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Sepultamento"},
                    {"id": "2", "label": "Cremação"},
                ])
            }

        if etapa == "cemiterio":
            return {
                "tipo": "texto",
                "mensagem": "🪦 Em qual cemitério será o sepultamento?"
            }

        if etapa == "cerimonia_cremacao":
            return {
                "tipo": "botoes",
                "mensagem": """Deseja realizar uma cerimônia de despedida no momento da cremação?""",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Sim"},
                    {"id": "2", "label": "Não"},
                ])
            }

        if etapa == "crematorio":
            return {
                "tipo": "botoes",
                "mensagem": """Trabalhamos com crematório parceiro e cuidamos de toda a organização.

Podemos seguir dessa forma?""",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Sim"},
                    {"id": "2", "label": "Prefiro outro local"},
                ])
            }

        if etapa == "crematorio_outro_nome":
            return {
                "tipo": "texto",
                "mensagem": "Pode me informar o nome ou local do crematório desejado?"
            }

        if etapa == "tipo_urna":
            texto = "Vamos escolher a urna.\nVou te apresentar algumas opções disponíveis:"
            if session.get("subfluxo") == "cremacao":
                texto = "Vamos escolher a urna para o velório:\nVou te apresentar algumas opções disponíveis:"
            return {
                "tipo": "botoes",
                "mensagem": texto,
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Simples"},
                    {"id": "2", "label": "Intermediária"},
                    {"id": "3", "label": "Premium"},
                ])
            }

        if etapa == "lista_urnas":
            urnas = session.get("urnas", [])
            return {
                "tipo": "botoes",
                "mensagem": "Escolha a urna:",
                "botoes": montar_botoes_urnas(urnas)
            }

        if etapa == "confirmar_urna":
            urna = session.get("urna")
            if not urna:
                return {"tipo": "texto", "mensagem": "Não encontramos a urna selecionada."}
            return renderizar_confirmacao_urna(urna, "Confirmar urna")

        if etapa == "tipo_urna_cinzas":
            return {
                "tipo": "botoes",
                "mensagem": """E depois, você poderá escolher a urna para guardar as cinzas com carinho:

Qual estilo deseja ver?""",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Simples"},
                    {"id": "2", "label": "Intermediária"},
                    {"id": "3", "label": "Premium"},
                ])
            }

        if etapa == "lista_urnas_cinzas":
            urnas = session.get("urnas_cinzas", [])
            return {
                "tipo": "botoes",
                "mensagem": "Escolha a urna de cinzas:",
                "botoes": montar_botoes_urnas(urnas)
            }

        if etapa == "confirmar_urna_cinzas":
            urna_cinzas = session.get("urna_cinzas")
            if not urna_cinzas:
                return {"tipo": "texto", "mensagem": "Não encontramos a urna de cinzas selecionada."}
            return renderizar_confirmacao_urna(urna_cinzas, "Confirmar urna de cinzas")

        if etapa == "resumo":
            return {
                "tipo": "botoes",
                "mensagem": obter_resumo(),
                "botoes": [
                    {"id": "1", "label": "Confirmar pedido"},
                    {"id": "2", "label": "Editar pedido"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if etapa == "editar_pedido":
            return {
                "tipo": "botoes",
                "mensagem": """O que você deseja editar?""",
                "botoes": [
                    {"id": "1", "label": "Velório"},
                    {"id": "2", "label": "Local do ente querido"},
                    {"id": "3", "label": "Porte"},
                    {"id": "4", "label": "Tipo de serviço"},
                    {"id": "5", "label": "Urna"},
                    {"id": "6", "label": "Urna de cinzas"},
                    {"id": "7", "label": "Cemitério / Crematório"},
                    {"id": "8", "label": "Voltar ao resumo"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        if etapa == "pagamento":
            total, sinal = calcular_pagamento()

            return {
                "tipo": "botoes",
                "mensagem": f"""💳 *Pagamento da entrada (sinal)*

Para concluirmos o atendimento, solicitamos o pagamento de *10% do valor total*.

💰 Valor total: {formatar_reais(total)}
💵 Entrada (10%): {formatar_reais(sinal)}

🔑 *Chave PIX:*
07559544000137

Assim que realizar o pagamento, é só clicar em *Já paguei* aqui embaixo 👇""",
                "botoes": [
                    {"id": "1", "label": "Já paguei"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }

        return {
            "tipo": "texto",
            "mensagem": "Etapa não encontrada."
        }

    # =========================================================
    # NORMALIZAÇÃO DE BOTÕES
    # =========================================================
    if mensagem == "Voltar":
        mensagem = "0"
    elif mensagem == "Menu principal":
        mensagem = "00"

    # =========================================================
    # AÇÕES GLOBAIS
    # =========================================================
    if mensagem == "0":
        return voltar()

    if mensagem == "00":
        return ir_menu_principal()

    # =========================================================
    # INÍCIO
    # =========================================================
    if session["etapa"] == "inicio":
        ir_para("menu_principal")
        return renderizar_etapa()

    # =========================================================
    # MENU PRINCIPAL
    # =========================================================
    if session["etapa"] == "menu_principal":
        if mensagem == "1":
            ir_para("velorio")
            return renderizar_etapa()

        if mensagem == "2":
            return {
                "tipo": "texto",
                "mensagem": """Claro 🙏

Para montar um orçamento com mais precisão, escolha *Serviços imediatos* e eu vou te conduzir passo a passo com cuidado."""
            }

        return {
            "tipo": "texto",
            "mensagem": "Por favor, escolha uma opção válida."
        }

    # =========================================================
    # ETAPA 1 — VELÓRIO
    # =========================================================
    if session["etapa"] == "velorio":
        if mensagem == "1":
            session["dados"]["velorio"] = "sim"
            ir_para("local_velorio")
            return renderizar_etapa()

        if mensagem == "2":
            session["dados"]["velorio"] = "nao"
            ir_para("local_corpo")
            return renderizar_etapa()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    # =========================================================
    # COM VELÓRIO
    # =========================================================
    if session["etapa"] == "local_velorio":
        if mensagem == "1":
            session["dados"]["local_velorio"] = "funeraria"
            ir_para("data_velorio")
            return {
                "tipo": "texto",
                "mensagem": """Perfeito, iremos organizar tudo com cuidado em nossa unidade 🙏

📅 Qual a data desejada para o velório?"""
            }

        if mensagem == "2":
            session["dados"]["local_velorio"] = "externo"
            ir_para("endereco_velorio")
            return renderizar_etapa()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    if session["etapa"] == "endereco_velorio":
        session["dados"]["endereco_velorio"] = mensagem
        ir_para("data_velorio")
        return renderizar_etapa()

    if session["etapa"] == "data_velorio":
        session["dados"]["data_velorio"] = mensagem
        ir_para("horario_velorio")
        return renderizar_etapa()

    if session["etapa"] == "horario_velorio":
        session["dados"]["horario_velorio"] = mensagem
        ir_para("local_corpo")
        return renderizar_etapa()

    # =========================================================
    # SEM VELÓRIO / CONTINUAÇÃO GERAL
    # =========================================================
    if session["etapa"] == "local_corpo":
        if mensagem not in ["1", "2", "3", "4"]:
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        session["dados"]["local_corpo"] = mensagem
        ir_para("endereco_local_corpo")
        return renderizar_etapa()

    if session["etapa"] == "endereco_local_corpo":
        session["dados"]["endereco_local_corpo"] = mensagem
        ir_para("porte")
        return renderizar_etapa()

    if session["etapa"] == "porte":
        if mensagem not in ["1", "2", "3"]:
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        session["dados"]["porte"] = mensagem
        ir_para("tipo_servico")
        return renderizar_etapa()

    if session["etapa"] == "tipo_servico":
        if mensagem == "1":
            session["subfluxo"] = "sepultamento"
            ir_para("cemiterio")
            return renderizar_etapa()

        if mensagem == "2":
            session["subfluxo"] = "cremacao"
            ir_para("cerimonia_cremacao")
            return renderizar_etapa()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    # =========================================================
    # SEPULTAMENTO
    # =========================================================
    if session["etapa"] == "cemiterio":
        session["dados"]["cemiterio"] = mensagem
        ir_para("tipo_urna")
        return renderizar_etapa()

    # =========================================================
    # CREMAÇÃO
    # =========================================================
    if session["etapa"] == "cerimonia_cremacao":
        if mensagem == "1":
            session["dados"]["cerimonia_cremacao"] = "sim"
            ir_para("crematorio")
            return renderizar_etapa()

        if mensagem == "2":
            session["dados"]["cerimonia_cremacao"] = "nao"
            ir_para("crematorio")
            return renderizar_etapa()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    if session["etapa"] == "crematorio":
        if mensagem == "1":
            session["dados"]["crematorio"] = "sim"
            ir_para("tipo_urna")
            return renderizar_etapa()

        if mensagem == "2":
            session["dados"]["crematorio"] = "outro"
            ir_para("crematorio_outro_nome")
            return renderizar_etapa()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    if session["etapa"] == "crematorio_outro_nome":
        session["dados"]["crematorio_outro_nome"] = mensagem
        ir_para("tipo_urna")
        return renderizar_etapa()

    # =========================================================
    # URNA PRINCIPAL
    # =========================================================
    if session["etapa"] == "tipo_urna":
        tipos = {
            "1": "simples",
            "2": "intermediaria",
            "3": "premium"
        }

        if mensagem not in tipos:
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        session["dados"]["tipo_urna"] = tipos[mensagem]

        urnas = listar_urnas(tipos[mensagem], session["subfluxo"])

        if not urnas:
            return {"tipo": "texto", "mensagem": "No momento não encontramos urnas disponíveis nessa categoria."}

        session["urnas"] = urnas
        ir_para("lista_urnas")
        return renderizar_etapa()

    if session["etapa"] == "lista_urnas":
        try:
            urna = session["urnas"][int(mensagem) - 1]
        except Exception:
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        session["urna"] = urna
        ir_para("confirmar_urna")
        return renderizar_etapa()

    if session["etapa"] == "confirmar_urna":
        if mensagem != "1":
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        if session.get("subfluxo") == "cremacao":
            ir_para("tipo_urna_cinzas")
        else:
            ir_para("resumo")

        return renderizar_etapa()

    # =========================================================
    # URNA DE CINZAS
    # =========================================================
    if session["etapa"] == "tipo_urna_cinzas":
        tipos = {
            "1": "simples",
            "2": "intermediaria",
            "3": "premium"
        }

        if mensagem not in tipos:
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        session["dados"]["tipo_urna_cinzas"] = tipos[mensagem]

        # Aqui estou usando o mesmo listar_urnas.
        # Se no seu sistema as urnas de cinzas estiverem cadastradas em outra categoria,
        # basta ajustar o segundo parâmetro abaixo.
        urnas_cinzas = listar_urnas(tipos[mensagem], "cinzas")

        if not urnas_cinzas:
            return {"tipo": "texto", "mensagem": "No momento não encontramos urnas de cinzas disponíveis nessa categoria."}

        session["urnas_cinzas"] = urnas_cinzas
        ir_para("lista_urnas_cinzas")
        return renderizar_etapa()

    if session["etapa"] == "lista_urnas_cinzas":
        try:
            urna_cinzas = session["urnas_cinzas"][int(mensagem) - 1]
        except Exception:
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        session["urna_cinzas"] = urna_cinzas
        ir_para("confirmar_urna_cinzas")
        return renderizar_etapa()

    if session["etapa"] == "confirmar_urna_cinzas":
        if mensagem != "1":
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        ir_para("resumo")
        return renderizar_etapa()

    # =========================================================
    # RESUMO
    # =========================================================
    if session["etapa"] == "resumo":
        if mensagem == "1":
            ir_para("pagamento")
            return renderizar_etapa()

        if mensagem == "2":
            ir_para("editar_pedido")
            return renderizar_etapa()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    # =========================================================
    # EDITAR PEDIDO
    # =========================================================
    if session["etapa"] == "editar_pedido":
        if mensagem == "1":
            ir_para("velorio")
            return renderizar_etapa()

        if mensagem == "2":
            ir_para("local_corpo")
            return renderizar_etapa()

        if mensagem == "3":
            ir_para("porte")
            return renderizar_etapa()

        if mensagem == "4":
            ir_para("tipo_servico")
            return renderizar_etapa()

        if mensagem == "5":
            ir_para("tipo_urna")
            return renderizar_etapa()

        if mensagem == "6":
            if session.get("subfluxo") != "cremacao":
                return {"tipo": "texto", "mensagem": "Urna de cinzas só está disponível para cremação."}
            ir_para("tipo_urna_cinzas")
            return renderizar_etapa()

        if mensagem == "7":
            if session.get("subfluxo") == "sepultamento":
                ir_para("cemiterio")
                return renderizar_etapa()

            if session.get("subfluxo") == "cremacao":
                ir_para("crematorio")
                return renderizar_etapa()

        if mensagem == "8":
            session["etapa"] = "resumo"
            return renderizar_etapa()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    # =========================================================
    # PAGAMENTO
    # =========================================================
    if session["etapa"] == "pagamento":
        if mensagem != "1":
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        total = session.get("pagamento", {}).get("total", 0)
        sinal = session.get("pagamento", {}).get("sinal", 0)

        salvar_pedido({
            "tipo": session.get("subfluxo"),
            "dados": session.get("dados", {}),
            "urna": session.get("urna"),
            "urna_cinzas": session.get("urna_cinzas"),
            "pagamento": {
                "total": total,
                "sinal": sinal
            },
            "telefone": session.get("numero"),
            "nome": session.get("nome"),
            "status": "aguardando_comprovante",
            "criado_em": datetime.now().isoformat()
        })

        session["encerrar_bot"] = True

        return {
            "tipo": "texto",
            "mensagem": """🙏 Obrigado.

Agora, por favor, *envie o comprovante de pagamento* aqui no WhatsApp para que nossa atendente possa finalizar o processo com todo cuidado.

Pode ficar tranquilo(a), nossa equipe vai cuidar de tudo com muito respeito, atenção e responsabilidade.
Desde o translado até a organização completa."""
        }

    # =========================================================
    # FALLBACK
    # =========================================================
    return {
        "tipo": "texto",
        "mensagem": "Não entendi sua resposta. Por favor, escolha uma opção válida."
    }