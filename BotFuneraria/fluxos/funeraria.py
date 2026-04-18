from datetime import datetime
from core.firebase import salvar_pedido
from core.pagamentos import formatar_reais
from core.firebase import buscar_servicos_funerarios

from fluxos.funeraria_orcamento import fluxo_funeraria_orcamento

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
            "1": "Até 85kg",
            "2": "Entre 85kg e 130kg",
            "3": "Acima de 130kg",
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

    
    def obter_resumo():
        dados = session.get("dados", {})
        

        linhas = []
        linhas.append("📋 *Resumo do atendimento*")
        linhas.append("")
        linhas.append(f"🕯️ Velório: {label_velorio(dados.get('velorio', '-'))}")

        if dados.get("velorio") == "sim":
            linhas.append(f"🏛️ Local do velório: {label_local_velorio(dados.get('local_velorio', '-'))}")
            if dados.get("local_velorio") == "externo":
                linhas.append(f"📍 Endereço do velório: {dados.get('endereco_velorio', '-')}")
            linhas.append(f"📅 Data do velório: {dados.get('data_velorio', '-')}")
            
        linhas.append(f"📍 Local do ente querido: {label_local_corpo(dados.get('local_corpo', '-'))}")
        linhas.append(f"📌 Endereço do local atual: {dados.get('endereco_local_corpo', '-')}")
        linhas.append(f"⚖️ Porte aproximado: {label_porte(dados.get('porte', '-'))}")
        servico = session.get("servico")

        if servico:
            linhas.append(f"⚰️ Serviço: {servico.get('nome', '-')}")
            linhas.append(f"💰 Valor: R$ {servico.get('preco', '-')}")
        

        
        return "\n".join(linhas)

    def calcular_pagamento():

        servico = session.get("servico")
        total = float(servico.get("preco", 0)) if servico else 0
        sinal = round(total * 0.1, 2)

        session["pagamento"] = {
            "total": total,
            "sinal": sinal
        }

        return total, sinal

    

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
                "tipo": "botoes",
                "mensagem": "📅 Qual a data desejada do serviço?",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Hoje"},
                    {"id": "2", "label": "Amanhã"},
                    {"id": "3", "label": "Outro"},
                ])
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
                    {"id": "1", "label": "Até 85kg"},
                    {"id": "2", "label": "Entre 85kg e 130kg"},
                    {"id": "3", "label": "Acima de 130kg"},
                ])
            }

        if etapa == "servicos":

            servicos = buscar_servicos_funerarios()
            session["servicos"] = servicos

            botoes = []

            for i, p in enumerate(servicos):
                botoes.append({
                    "id": str(i + 1),
                    "label": f"{p.get('nome')} - R$ {p.get('preco')}"
                })

            return {
                "tipo": "botoes",
                "mensagem": "⚰️ Escolha o serviço desejado:",
                "botoes": botao_voltar_menu(botoes)
            }

        
        if etapa == "editar_pedido":
            return {
                "tipo": "botoes",
                "mensagem": """O que você deseja editar?""",
                "botoes": [
                    {"id": "1", "label": "Velório"},
                    {"id": "2", "label": "Local do ente querido"},
                    {"id": "3", "label": "Porte"},
                    {"id": "4", "label": "Serviço"},  # 🔥 NOVO
                    {"id": "5", "label": "Voltar ao resumo"},
                    {"id": "0", "label": "Voltar"},
                    {"id": "00", "label": "Menu principal"},
                ]
            }


        if etapa == "resumo":
            return {
                "tipo": "botoes",
                "mensagem": obter_resumo(),
                "botoes": [
                    {"id": "1", "label": "Confirmar e continuar"},
                    {"id": "2", "label": "Editar informações"},
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


    
    

    # 🔥 TRATAR VOLTAR SOMENTE NO CONFIRMAR PACOTE

    if mensagem == "0" and session.get("etapa") == "confirmar_servico":
        session["etapa"] = "servicos"
        return renderizar_etapa()

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
            session["historico"] = []
            session["dados"] = {}
            session["subfluxo"] = None
            session["fluxo"] = "funeraria_orcamento"
            session["etapa"] = "inicio"
            return fluxo_funeraria_orcamento(session, mensagem)
        
        
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
            ir_para("data_velorio")
            return renderizar_etapa()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    # =========================================================
    # COM VELÓRIO
    # =========================================================
    if session["etapa"] == "local_velorio":
        if mensagem == "1":
            session["dados"]["local_velorio"] = "funeraria"
            ir_para("data_velorio")
            return renderizar_etapa()

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

        if mensagem == "1":
            session["dados"]["data_velorio"] = datetime.now().strftime("%d/%m/%Y")
            ir_para("local_corpo")
            return renderizar_etapa()

        if mensagem == "2":
            from datetime import timedelta
            amanha = datetime.now() + timedelta(days=1)
            session["dados"]["data_velorio"] = amanha.strftime("%d/%m/%Y")
            ir_para("local_corpo")
            return renderizar_etapa()

        if mensagem == "3":
            ir_para("data_velorio_digitada")
            return {
                "tipo": "texto",
                "mensagem": "📅 Digite a data desejada (ex: 25/03/2026):"
            }

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    

    # =========================================================
    # SEM VELÓRIO / CONTINUAÇÃO GERAL
    # =========================================================

    if session["etapa"] == "data_velorio_digitada":
        session["dados"]["data_velorio"] = mensagem
        ir_para("local_corpo")
        return renderizar_etapa()

    if session["etapa"] == "local_corpo":
        if mensagem not in ["1", "2", "3", "4"]:
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        session["dados"]["local_corpo"] = mensagem
        ir_para("endereco_local_corpo")
        return renderizar_etapa()

    if session["etapa"] == "endereco_local_corpo":
        session["dados"]["endereco_local_corpo"] = mensagem

        # 🔥 SE ESTIVER EDITANDO
        if session.get("editando") == "local_corpo":
            session.pop("editando", None)
            session["etapa"] = "resumo"
            return renderizar_etapa()

        # fluxo normal
        ir_para("porte")
        return renderizar_etapa()

    if session["etapa"] == "porte":
        if mensagem not in ["1", "2", "3"]:
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        session["dados"]["porte"] = mensagem

        # 🔥 EDITANDO
        if session.get("editando") == "porte":
            session.pop("editando", None)
            session["etapa"] = "resumo"
            return renderizar_etapa()

        ir_para("servicos")
        return renderizar_etapa()

    if session["etapa"] == "servicos":

        if mensagem == "0":
            return renderizar_etapa()

        try:
            servico = session["servicos"][int(mensagem) - 1]
        except:
            return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

        session["servico"] = servico

        respostas = []

        # envia imagens
        for img in servico.get("imagens", []):
            respostas.append({
                "tipo": "imagem",
                "url": img
            })

        # mensagem final
        respostas.append({
            "tipo": "botoes",
            "mensagem": f"""📦 *{servico.get('nome')}*

💰 R$ {servico.get('preco')}

{servico.get('descricao', '')}

Deseja confirmar ou alterar alguma coisa?""",
            "botoes": [
                {"id": "1", "label": "Confirmar"},
                {"id": "2", "label": "Alterar"},
                {"id": "0", "label": "Voltar"},
                {"id": "00", "label": "Menu principal"},
            ]
        })

        session["etapa"] = "confirmar_servico"

        return respostas

    
    # =========================================================
    # RESUMO
    # =========================================================

    if session["etapa"] == "confirmar_servico":

        if mensagem == "0":
            # 🔥 VOLTAR PARA LISTA DE PACOTES
            session["etapa"] = "servicos"
            return renderizar_etapa()

        if mensagem == "1":
            ir_para("resumo")
            return renderizar_etapa()

        if mensagem == "2":
            session["encerrar_bot"] = True
            return {
                "tipo": "texto",
                "mensagem": "Perfeito 🙏\n\nVou te encaminhar agora para um atendente que irá te ajudar nisso."
            }

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}



    # =========================================================
    # RESUMO - AÇÕES
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
            session["editando"] = "velorio"
            session["etapa"] = "velorio"
            return renderizar_etapa()

        if mensagem == "2":
            session["editando"] = "local_corpo"
            session["etapa"] = "local_corpo"
            return renderizar_etapa()

        if mensagem == "3":
            session["editando"] = "porte"
            session["etapa"] = "porte"
            return renderizar_etapa()

        if mensagem == "4":
            # 🔥 IR PARA PACOTES
            session.pop("servico", None)
            session["etapa"] = "servicos"
            return renderizar_etapa()

        if mensagem == "5":
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
            "servico": session.get("servico"),
            "dados": session.get("dados", {}),
            "pagamento": {
                "total": total,
                "sinal": sinal
            },
            "telefone": session.get("numero"),
            "nome": session.get("nome"),
            "status": "aberto",
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