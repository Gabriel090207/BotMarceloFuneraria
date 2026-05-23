from datetime import datetime
from core.firebase import salvar_pedido
from core.pagamentos import formatar_reais
from core.firebase import buscar_servicos_funerarios

from core.avisos import aviso_funeraria, aviso_atendente

from fluxos.funeraria_orcamento import (
    fluxo_funeraria_orcamento,
    COBERTURA_COMPLETA,
    COBERTURA_EXTERNO
)

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
        session["dados"] = {}
        session["subfluxo"] = None
        session["fluxo"] = None
        session["etapa"] = "inicio"
        session["etapa_global"] = "menu"

        return {
            "tipo": "botoes",
            "mensagem": "🕊️ Voltamos ao menu principal.\n\nEscolha uma opção:",
            "botoes": [
                {"id": "1", "label": "⚰️ Serviços funerários"},
                {"id": "2", "label": "🛡️ Planos"},
                {"id": "3", "label": "🗃️ Convênios"},
                {"id": "4", "label": "💼 Financeiro / Administrativo"},
                {"id": "5", "label": "🌷 Floricultura"},
                {"id": "6", "label": "🏢 Conhecer estrutura"},
                {"id": "7", "label": "📍 Localização"},
                {"id": "8", "label": "👤 Falar com atendente"},
                {"id": "99", "label": "🔄 Reiniciar atendimento"},
            ]
        }

    def botao_voltar_menu(lista_botoes):
        return lista_botoes + [
            {"id": "0", "label": "Voltar"},
            {"id": "00", "label": "Menu principal"},
            {"id": "99", "label": "🔄 Reiniciar atendimento"},
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
        if dados.get("velorio") == "nao":
            linhas.append(f"🙏 Despedida: {dados.get('despedida', '-')}")


        if dados.get("velorio") == "sim":
            linhas.append(f"🏛️ Local do velório: {label_local_velorio(dados.get('local_velorio', '-'))}")
            if dados.get("local_velorio") == "externo":
                linhas.append(f"📍 Endereço do velório: {dados.get('endereco_velorio', '-')}")
            linhas.append(f"📅 Data do velório: {dados.get('data_velorio', '-')}")
            
        if dados.get("local_corpo"):
            linhas.append(f"📍 Local do ente querido: {label_local_corpo(dados.get('local_corpo'))}")

        if dados.get("local_corpo") == "1" and dados.get("hospital_nome"):
            linhas.append(f"📌 Hospital: {dados.get('hospital_nome')}")

        elif (
            dados.get("local_corpo") in ["2", "4"]
            and dados.get("endereco_local_corpo")
        ):
            linhas.append(f"📌 Endereço atual: {dados.get('endereco_local_corpo')}")
        if dados.get("porte"):
            linhas.append(f"⚖️ Porte aproximado: {label_porte(dados.get('porte'))}")
        if dados.get("destino"):
            linhas.append(f"⚱️ Destino: {dados.get('destino')}")

        if dados.get("cemiterio"):
            linhas.append(f"🪦 Cemitério: {dados.get('cemiterio')}")
        servico = session.get("servico")

        if servico:
            if servico.get("nome"):
                linhas.append(f"⚰️ Serviço: {servico.get('nome')}")

            if servico.get("preco"):
                linhas.append(f"💰 Valor: R$ {servico.get('preco')}")
        

        
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
                    {"id": "99", "label": "🔄 Reiniciar atendimento"},
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

        if etapa == "despedida_sem_velorio":
            return {
                "tipo": "botoes",
                "mensagem": "Os familiares desejam realizar uma despedida?",
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

        if etapa == "hospital_liberacao":
            return {
                "tipo": "botoes",
                "mensagem": "O ente querido já foi liberado no necrotério?",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Sim"},
                    {"id": "2", "label": "Não"},
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


        if etapa == "destino_final":
            return {
                "tipo": "botoes",
                "mensagem": "🪦 Qual o destino final do seu ente querido?",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Jazigo particular"},
                    {"id": "2", "label": "Sem jazigo particular"},
                    {"id": "3", "label": "Cremação"},
                    {"id": "4", "label": "Translado"},
                ])
            }

        if etapa == "cemiterio_nome":
            return {
                "tipo": "texto",
                "mensagem": "Qual o nome do cemitério?"
            }

        if etapa == "cidade_destino":
            return {
                "tipo": "texto",
                "mensagem": "📍 Informe a cidade e estado de destino para cotação."
            }


        if etapa == "conhece_funeraria":
            return {
                "tipo": "botoes",
                "mensagem": "🏢 Você já conhece nossa estrutura? 🕊️",
                "botoes": botao_voltar_menu([
                    {"id": "1", "label": "Sim, já conheço"},
                    {"id": "2", "label": "Não, quero conhecer"},
                ])
            }

        if etapa == "servicos":

            if session["dados"].get("velorio") == "nao":
                session["servicos"] = [{
                    "nome": "Sem velório",
                    "preco": 2000
                }]

                return {
                    "tipo": "botoes",
                    "mensagem": "⚰️ Escolha o serviço desejado, Parcelamos em até 10x sem juros:",
                    "botoes": botao_voltar_menu([
                        {"id": "1", "label": "Sem velório - R$ 2.000,00"}
                    ])
                }

            servicos = buscar_servicos_funerarios()

            local = session["dados"].get("local_velorio")

            if local == "funeraria":
                servicos = [
                    s for s in servicos
                    if str(s.get("categoria", "")).lower() != "externo"
                ]

            elif local == "externo":
                servicos = [
                    s for s in servicos
                    if str(s.get("categoria", "")).lower() == "externo"
                ]

            session["servicos"] = servicos

            botoes = []

            for i, p in enumerate(servicos):
                preco = formatar_reais(float(p.get("preco", 0)))

                botoes.append({
                    "id": str(i + 1),
                    "label": f"{preco} • {p.get('nome')[:18]}"
  
                })

            return {
                "tipo": "botoes",
                "mensagem": "⚰️ Escolha o serviço desejado, Parcelamos em até 10x sem juros:",
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
                    {"id": "99", "label": "🔄 Reiniciar atendimento"},
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
                    {"id": "99", "label": "🔄 Reiniciar atendimento"},
                ]
            }

        if etapa == "pagamento":
            total, sinal = calcular_pagamento()

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

           

            return [
            {
                "tipo": "texto",
                "mensagem": f"""👤 *Pagamento da entrada (sinal)*

Para concluirmos o atendimento, solicitamos o pagamento de *10% do valor total*.

💰 Valor total: {formatar_reais(total)}
💵 Entrada (10%): {formatar_reais(sinal)}"""
            },
            {
                "tipo": "pix",
                "chave": "07559544000137",
                "tipo_chave": "CNPJ"
            },
            {
                "tipo": "botoes",
                "mensagem": """👤 Após realizar o pagamento, envie o comprovante diretamente para nosso plantonista.

📲 WhatsApp do plantonista:
https://wa.me/5592995131313

ℹ️ Nossa equipe continuará seu atendimento humano por lá.""",
                "botoes": [
                    {"id": "00", "label": "Menu principal"},
                    {"id": "99", "label": "🔄 Reiniciar atendimento"},
                ]
            }
            ]

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

        if session["dados"].get("velorio") == "nao":
            session["etapa"] = "despedida_sem_velorio"
        else:
            session["etapa"] = "servicos"

        return renderizar_etapa()

    # =========================================================
    # AÇÕES GLOBAIS
    # =========================================================
    if mensagem == "0":
        return voltar()

    if mensagem == "00":
        return ir_menu_principal()


    if mensagem == "99":
        session.clear()
        session["etapa_global"] = "inicio"
        return None

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


    if session["etapa"] == "despedida_sem_velorio":

        texto = """⚰️ *SEM VELÓRIO*

💰 Valor: R$ 2.000,00
💳 Em até 10x no cartão de crédito sem juros

✅ Caixão padrão até 1.90 comportando até 85kg com segurança
✅ Remoção e Cortejo
✅ Pagamento de taxa municipal"""

        session["servico"] = {
            "nome": "Sem velório",
            "preco": 2000
        }

        if mensagem == "1":
            session["dados"]["despedida"] = "Sim"
            texto += "\n\n🙏 Permanência por até 1h com a urna fechada."

        elif mensagem == "2":
            session["dados"]["despedida"] = "Não"

        else:
            return {
                "tipo": "texto",
                "mensagem": "Escolha uma opção válida."
            }  

        session["etapa"] = "confirmar_servico"
        session["aguardando_confirmacao"] = False

        

        return {
            "tipo": "botoes",
            "mensagem": texto + "\n\nDeseja confirmar?",
            "botoes": [
                {"id": "1", "label": "Confirmar"},
                {"id": "0", "label": "Voltar"},
                {"id": "00", "label": "Menu principal"},
                {"id": "99", "label": "🔄 Reiniciar atendimento"},
            ]
        }
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
            return {
                "tipo": "texto",
                "mensagem": "Escolha uma opção válida."
            }

        session["dados"]["local_corpo"] = mensagem

        if mensagem == "1":  # Hospital
            ir_para("hospital_nome")
            return {
                "tipo": "texto",
                "mensagem": "🏥 Qual o nome do hospital?"
            }

        if mensagem == "3":
            ir_para("destino_final")
            return renderizar_etapa()

        ir_para("endereco_local_corpo")
        return renderizar_etapa()

    


    if session["etapa"] == "hospital_nome":
        session["dados"]["hospital_nome"] = mensagem

        ir_para("hospital_liberacao")

        return {
            "tipo": "botoes",
            "mensagem": "O ente querido já foi liberado no necrotério?",
            "botoes": botao_voltar_menu([
                {"id": "1", "label": "Sim"},
                {"id": "2", "label": "Não"},
            ])
        }


    if session["etapa"] == "hospital_liberacao":

        if mensagem == "1":
            session["dados"]["liberacao_hospital"] = "Sim"

            ir_para("porte")

            return [
                {
                    "tipo": "texto",
                    "mensagem": "🙏 Pedimos que um familiar aguarde no local para recepcionar nossa equipe."
                },
                renderizar_etapa()
            ]

        elif mensagem == "2":
            session["dados"]["liberacao_hospital"] = "Não"

            ir_para("porte")

            return renderizar_etapa()

        else:
            return {
                "tipo": "texto",
                "mensagem": "Escolha uma opção válida."
            }

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
            return {
                "tipo": "texto",
                "mensagem": "Escolha uma opção válida."
            }

        session["dados"]["porte"] = mensagem

        # Se estiver editando
        if session.get("editando") == "porte":
            session.pop("editando", None)
            session["etapa"] = "resumo"
            return renderizar_etapa()

        # Até 85kg segue normal
        if mensagem == "1":

            # Se for translado, pedir cidade destino
            if session["dados"].get("destino") == "Translado":
                ir_para("cidade_destino")
            else:
                ir_para("conhece_funeraria")

            return renderizar_etapa()

        # Acima de 85kg = atendente
        aviso_atendente(
            session.get("nome"),
            session.get("numero"),
            "Atendimento funerário - peso acima de 85kg"
        )

        return {
            "tipo": "botoes",
            "mensagem": """👤 Nossa equipe humana irá te auxiliar com todo cuidado.

📲 Fale agora com nosso plantonista:
https://wa.me/5592995131313

ℹ️ As informações já foram enviadas para nossa equipe.""",
            "botoes": [
                {"id": "00", "label": "Menu principal"},
                {"id": "99", "label": "🔄 Reiniciar atendimento"},
            ]
        }

    if session["etapa"] == "destino_final":

        if mensagem == "1":
            session["dados"]["destino"] = "Jazigo particular"
            ir_para("cemiterio_nome")
            return renderizar_etapa()

        if mensagem == "2":
            session["dados"]["destino"] = "Sem jazigo particular"
            ir_para("porte")
            return renderizar_etapa()

        if mensagem == "3":
            session["dados"]["destino"] = "Cremação"
            ir_para("porte")
            return renderizar_etapa()

        if mensagem == "4":
            session["dados"]["destino"] = "Translado"
            ir_para("porte")
            return renderizar_etapa()

        return {
            "tipo": "texto",
            "mensagem": "Escolha uma opção válida."
        }

    if session["etapa"] == "cemiterio_nome":
        session["dados"]["cemiterio"] = mensagem
        ir_para("porte")
        return renderizar_etapa()

    if session["etapa"] == "conhece_funeraria":

        if mensagem == "1":
            ir_para("servicos")
            return renderizar_etapa()

        elif mensagem == "2":
            session["etapa"] = "aguardando_ver_servicos"

        

            return [
                {
                    "tipo": "video",
                    "url": "https://firebasestorage.googleapis.com/v0/b/bot-marcelofloricultura.firebasestorage.app/o/midias%2FWhatsApp%20Video%202026-04-15%20at%2017.16.41.mp4?alt=media&token=a3297384-1607-45a2-a3a9-3772caf942e0"
                },
                {
                    "tipo": "botoes",
                    "mensagem": "🏢 Conheça nossa estrutura 🕊️",
                    "botoes": [
                        {"id": "1", "label": "Ver serviços"},
                        {"id": "00", "label": "Menu principal"},
                        {"id": "99", "label": "🔄 Reiniciar atendimento"},
                    ]
                }
            ]

        return {
            "tipo": "texto",
            "mensagem": "Escolha uma opção válida."
        }

    if session["etapa"] == "aguardando_ver_servicos":

        if mensagem == "1":
            session["etapa"] = "servicos"
            return renderizar_etapa()

        elif mensagem == "00":
            session["fluxo"] = None
            session["etapa_global"] = "menu"
            return None

        elif mensagem == "99":
            session.clear()
            session["etapa_global"] = "inicio"
            return None

        return {
            "tipo": "texto",
            "mensagem": "Escolha uma opção válida."
        }

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
        texto = f"""🏢 *{servico.get('nome')}*

💰 A partir de {formatar_reais(float(servico.get('preco', 0)))}
💳 Em até 10x no cartão de crédito sem juros

ℹ️ Valor inicial considerando urna padrão para até 85kg.
Para outras necessidades, consulte nossa equipe."""

        if servico.get("capacidade"):
            texto += f"\n\n✅ Capacidade interna: {servico['capacidade']}"

        if str(servico.get("suite", "")).lower() == "sim":
            texto += f"\n✅ Suíte: {servico['suite']}"

        if servico.get("area_externa"):
            texto += f"\n✅ {servico['area_externa']}"

        if servico.get("descricao"):
            texto += f"\n\n{servico['descricao']}"

        if str(servico.get("categoria", "")).lower() == "externo":
            texto += "\n" + COBERTURA_EXTERNO
        else:
            texto += "\n" + COBERTURA_COMPLETA

        texto += "\n\nDeseja confirmar?"

        respostas.append({
            "tipo": "botoes",
            "mensagem": texto,
            "botoes": [
                {"id": "1", "label": "Confirmar"},
                {"id": "0", "label": "Voltar"},
                {"id": "00", "label": "Menu principal"},
                {"id": "99", "label": "🔄 Reiniciar atendimento"},
            ]
        })

        session["etapa"] = "confirmar_servico"
        session["aguardando_confirmacao"] = False

        return respostas

    
    # =========================================================
    # RESUMO
    # =========================================================

    if session["etapa"] == "confirmar_servico":

        if session.get("aguardando_confirmacao") != True:
            session["aguardando_confirmacao"] = True
            return None

        if mensagem == "0":
            session["etapa"] = "servicos"
            return renderizar_etapa()

        elif mensagem == "1":
            ir_para("resumo")
            return renderizar_etapa()

        elif mensagem == "2":
            ir_para("editar_pedido")
            return renderizar_etapa()

        else:
            return None



    # =========================================================
    # RESUMO - AÇÕES
    # =========================================================
    if session["etapa"] == "resumo":

        if mensagem == "1":

            aviso_funeraria(
                session.get("nome"),
                session.get("numero"),
                session.get("dados", {}),
                session.get("servico")
            )

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
            session.pop("servico", None)
            session.pop("editando", None)
            session["historico"] = []
            session["etapa"] = "servicos"
            return renderizar_etapa()

        if mensagem == "5":
            session["etapa"] = "resumo"
            return renderizar_etapa()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    


    if session["etapa"] == "cidade_destino":

        session["dados"]["cidade_destino"] = mensagem

        aviso_atendente(
            session.get("nome"),
            session.get("numero"),
            f"Translado para {mensagem}"
        )

        return {
            "tipo": "botoes",
            "mensagem": """👤 Recebemos as informações para cotação do translado.

📲 Fale agora com nosso plantonista:
https://wa.me/5592995131313

ℹ️ As informações já foram enviadas para nossa equipe.""",
            "botoes": [
                {"id": "00", "label": "Menu principal"},
                {"id": "99", "label": "🔄 Reiniciar atendimento"},
            ]
        }
    # =========================================================
    # PAGAMENTO
    # =========================================================
    if session["etapa"] == "pagamento":
        return {
            "tipo": "texto",
            "mensagem": """👤 Assim que concluir o pagamento, envie o comprovante para nosso plantonista.

📲 WhatsApp:
https://wa.me/5592995131313"""
        }