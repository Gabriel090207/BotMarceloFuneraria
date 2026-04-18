def _menu(titulo, opcoes):
    return {
        "tipo": "botoes",
        "mensagem": titulo,
        "botoes": [{"id": op[0], "label": op[1]} for op in opcoes]
    }


def fluxo_planos_familiares(session, mensagem):

    session.setdefault("etapa", "inicio")
    session.setdefault("historico", [])
    session.setdefault("dados", {})

    nome = session.get("nome", "")

    # =================================================
    # TEXTO FIXO
    # =================================================

    info_importante = """

💡 *Informações importantes:*

✔️ Contrato vitalício com renovação anual
✔️ Carência de 180 dias (antes disso, 30% de desconto no serviço funerário, aprox. R$ 1.000)
✔️ Comece a pagar em até 30 dias e já conta a carência
✔️ Sem idade mínima ou máxima, qualquer pessoa pode aderir
✔️ Valores individuais ou para adições ao pacote variam por faixa etária:
0-45 anos: R$ 27 | 46-69 anos: R$ 40 | 70+: R$ 70
✔️ Empresa local, 30 anos de experiência, estrutura completa com estacionamento, restaurante, floricultura, gráfica e acessibilidade total no térreo.
"""

    cobertura_valioso = """
✅ Salão completo 24h na Funerária Canaã
✅ Caixão padrão até 1.90 comportando até 85kg com segurança
✅ Transporte completo
✅ Preparação completa + Tanatopraxia (24h)
✅ Ornamentação com flores do campo naturais
✅ Cerimonial ecumênico para homenagem com capelão e músico
✅ Kit café + Copa 24h
✅ Carteirinha digital com acesso à nossa rede de parceiros em todos os setores da vida, garantindo descontos em diversos serviços
"""

    # =================================================
    # AUXILIARES
    # =================================================

    def salvar_historico():
        etapa = session.get("etapa")
        if etapa:
            session["historico"].append(etapa)

    def voltar():
        if session["historico"]:
            session["etapa"] = session["historico"].pop()
        else:
            session["etapa"] = "menu"
        return renderizar()

    def menu_principal():
        session["fluxo"] = None
        session["etapa"] = "inicio"
        session["historico"] = []
        session["etapa_global"] = "menu"

        return {
            "tipo": "botoes",
            "mensagem": "🔙 Voltamos ao menu principal.\n\nEscolha uma opção:",
            "botoes": [
                {"id": "1", "label": "Serviços funerários"},
                {"id": "2", "label": "Planos"},
                {"id": "3", "label": "Financeiro / Administrativo"},
                {"id": "4", "label": "Floricultura"},
                {"id": "5", "label": "Falar com atendente"},
            ]
        }

    def renderizar():

        etapa = session["etapa"]

        # -------------------------------------------------
        # MENU INICIAL
        # -------------------------------------------------

        if etapa == "inicio" or etapa == "menu":
            session["etapa"] = "menu"

            return _menu(
                f"""🛡️ Planos

{nome}, escolha uma opção:""",
                [
                    ("1", "Ver planos disponíveis"),
                    ("2", "Contrato Futuro"),
                    ("3", "Abertura de Sinistro"),
                    ("9", "Falar com atendente"),
                    ("00", "Voltar ao menu"),
                ]
            )

        # -------------------------------------------------
        # LISTA PLANOS
        # -------------------------------------------------

        if etapa == "lista_planos":
            return _menu(
                "📋 Escolha um plano:",
                [
                    ("1", "Plano Essencial"),
                    ("2", "Plano Valioso"),
                    ("3", "Plano Supremo Luxo"),
                    ("4", "Individual / Personalizado"),
                    ("0", "Voltar"),
                    ("00", "Menu principal"),
                ]
            )

        # -------------------------------------------------
        # DETALHES PLANOS
        # -------------------------------------------------

        if etapa == "plano_essencial":
            return _menu(
                f"""🛡️ *Plano Essencial – 3 pessoas*

💰 *R$ 97/mês*

✅ Salão para velório 24h
✅ Caixão padrão até 1.90 e comportando até 85kg com segurança
✅ Transporte e preparação básica do corpo
✅ Flores artificiais
✅ Copa 24h
✅ Carteirinha digital com acesso à rede de parceiros

*Indicado para quem busca proteção básica com menor investimento.*{info_importante}""",
                [
                    ("1", "Tenho interesse"),
                    ("2", "Ver outros planos"),
                    ("0", "Voltar"),
                    ("00", "Menu principal"),
                ]
            )

        if etapa == "plano_valioso":
            return _menu(
                f"""⭐ *Plano Valioso (Intermediário) – até 5 pessoas*

💰 *R$ 137/mês*

{cobertura_valioso}

*Oferece uma despedida completa, além de benefícios que ajudam a quem se cuida no dia a dia.*{info_importante}""",
                [
                    ("1", "Tenho interesse"),
                    ("2", "Ver outros planos"),
                    ("0", "Voltar"),
                    ("00", "Menu principal"),
                ]
            )

        if etapa == "plano_supremo":
            return _menu(
                f"""🌹 *Plano Supremo Luxo – até 5 pessoas*

💰 *R$ 157/mês*

{cobertura_valioso}
✅ Coroa de flores para uma homenagem ainda mais especial{info_importante}""",
                [
                    ("1", "Tenho interesse"),
                    ("2", "Ver outros planos"),
                    ("0", "Voltar"),
                    ("00", "Menu principal"),
                ]
            )

        if etapa == "plano_individual":
            return _menu(
                f"""🕊️ *Individual / Personalizado*

💰 R$ 27,00 (0–45 anos)
💰 R$ 40,00 (46–69 anos)
💰 R$ 70,00 (70+)

{cobertura_valioso}{info_importante}""",
                [
                    ("1", "Tenho interesse"),
                    ("2", "Ver outros planos"),
                    ("0", "Voltar"),
                    ("00", "Menu principal"),
                ]
            )

        # -------------------------------------------------
        # CONTRATO FUTURO
        # -------------------------------------------------

        if etapa == "contrato_futuro":
            return _menu(
                """📄 *Contrato Futuro*

💰 *A partir de R$ 3.000*

✅ Personalizado com os itens escolhidos
✅ Até 1 ano para fazer a quitação
✅ Após a quitação, pode utilizar para qualquer pessoa com a cobertura escolhida
✅ Sem reajuste
✅ Sem carência
✅ Caso utilize antes da quitação, paga apenas o saldo restante

Deseja seguir?""",
                [
                    ("1", "Tenho interesse"),
                    ("0", "Voltar"),
                    ("00", "Menu principal"),
                ]
            )

        # -------------------------------------------------
        # COLETAS
        # -------------------------------------------------

        if etapa == "coletar_nome":
            return {
                "tipo": "texto",
                "mensagem": "Perfeito 🙏\n\nInforme seu nome completo."
            }

        if etapa == "coletar_qtd":
            return {
                "tipo": "texto",
                "mensagem": "Quantas pessoas deseja incluir?"
            }

        if etapa == "coletar_idades":
            return {
                "tipo": "texto",
                "mensagem": "Informe as idades separadas por vírgula.\nEx: 35, 32, 8"
            }

        if etapa == "coletar_cidade":
            return {
                "tipo": "texto",
                "mensagem": "Informe sua cidade."
            }

        # -------------------------------------------------
        # SINISTRO
        # -------------------------------------------------

        if etapa == "sinistro_nome":
            return {
                "tipo": "texto",
                "mensagem": "🙏 Sentimos muito por este momento.\n\nInforme o nome completo do responsável."
            }

        if etapa == "sinistro_cpf":
            return {
                "tipo": "texto",
                "mensagem": "Informe o CPF do responsável."
            }

        if etapa == "sinistro_falecido":
            return {
                "tipo": "texto",
                "mensagem": "Informe o nome da pessoa falecida."
            }

        if etapa == "sinistro_cidade":
            return {
                "tipo": "texto",
                "mensagem": "Informe a cidade ou local do ocorrido."
            }

    # =================================================
    # NORMALIZAÇÃO
    # =================================================

    if mensagem == "Voltar":
        mensagem = "0"

    if mensagem == "Menu principal":
        mensagem = "00"

    if mensagem == "0":
        return voltar()

    if mensagem == "00":
        return menu_principal()

    # =================================================
    # INÍCIO
    # =================================================

    if session["etapa"] == "inicio":
        return renderizar()

    # =================================================
    # MENU
    # =================================================

    if session["etapa"] == "menu":

        if mensagem == "1":
            salvar_historico()
            session["etapa"] = "lista_planos"
            return renderizar()

        if mensagem == "2":
            salvar_historico()
            session["dados"]["tipo_interesse"] = "Contrato Futuro"
            session["etapa"] = "contrato_futuro"
            return renderizar()

        if mensagem == "3":
            salvar_historico()
            session["etapa"] = "sinistro_nome"
            return renderizar()

        if mensagem == "9":
            session["fluxo"] = "atendente"
            session["encerrar_bot"] = True
            return {
                "tipo": "texto",
                "mensagem": "👨‍💼 Você será encaminhado para nosso atendimento."
            }

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    # =================================================
    # LISTA PLANOS
    # =================================================

    if session["etapa"] == "lista_planos":

        mapa = {
            "1": ("plano_essencial", "Plano Essencial"),
            "2": ("plano_valioso", "Plano Valioso"),
            "3": ("plano_supremo", "Plano Supremo Luxo"),
            "4": ("plano_individual", "Individual / Personalizado"),
        }

        if mensagem in mapa:
            salvar_historico()
            session["etapa"] = mapa[mensagem][0]
            session["dados"]["tipo_interesse"] = mapa[mensagem][1]
            return renderizar()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    # =================================================
    # DETALHES PLANOS / CONTRATO
    # =================================================

    if session["etapa"] in [
        "plano_essencial",
        "plano_valioso",
        "plano_supremo",
        "plano_individual",
        "contrato_futuro"
    ]:

        if mensagem == "1":
            salvar_historico()
            session["etapa"] = "coletar_nome"
            return renderizar()

        if mensagem == "2" and session["etapa"] != "contrato_futuro":
            session["etapa"] = "lista_planos"
            return renderizar()

        return {"tipo": "texto", "mensagem": "Escolha uma opção válida."}

    # =================================================
    # COLETA INTERESSE
    # =================================================

    if session["etapa"] == "coletar_nome":
        session["dados"]["nome_completo"] = mensagem
        salvar_historico()
        session["etapa"] = "coletar_qtd"
        return renderizar()

    if session["etapa"] == "coletar_qtd":
        session["dados"]["quantidade"] = mensagem

        if session["dados"]["tipo_interesse"] == "Contrato Futuro":
            salvar_historico()
            session["etapa"] = "coletar_cidade"
            return renderizar()

        salvar_historico()
        session["etapa"] = "coletar_idades"
        return renderizar()

    if session["etapa"] == "coletar_idades":
        session["dados"]["idades"] = mensagem
        session["fluxo"] = "atendente"
        session["encerrar_bot"] = True

        return {
            "tipo": "texto",
            "mensagem": f"""📋 Interesse registrado com sucesso.

Interesse: {session["dados"]["tipo_interesse"]}
Nome: {session["dados"]["nome_completo"]}
Pessoas: {session["dados"]["quantidade"]}
Idades: {session["dados"]["idades"]}

👨‍💼 Você será encaminhado para finalizar o atendimento."""
        }

    if session["etapa"] == "coletar_cidade":
        session["dados"]["cidade"] = mensagem
        session["fluxo"] = "atendente"
        session["encerrar_bot"] = True

        return {
            "tipo": "texto",
            "mensagem": f"""📋 Interesse registrado com sucesso.

Interesse: {session["dados"]["tipo_interesse"]}
Nome: {session["dados"]["nome_completo"]}
Pessoas: {session["dados"]["quantidade"]}
Cidade: {session["dados"]["cidade"]}

👨‍💼 Você será encaminhado para finalizar o atendimento."""
        }

    # =================================================
    # SINISTRO
    # =================================================

    if session["etapa"] == "sinistro_nome":
        session["dados"]["responsavel"] = mensagem
        salvar_historico()
        session["etapa"] = "sinistro_cpf"
        return renderizar()

    if session["etapa"] == "sinistro_cpf":
        session["dados"]["cpf"] = mensagem
        salvar_historico()
        session["etapa"] = "sinistro_falecido"
        return renderizar()

    if session["etapa"] == "sinistro_falecido":
        session["dados"]["falecido"] = mensagem
        salvar_historico()
        session["etapa"] = "sinistro_cidade"
        return renderizar()

    if session["etapa"] == "sinistro_cidade":
        session["dados"]["cidade_sinistro"] = mensagem
        session["fluxo"] = "atendente"
        session["encerrar_bot"] = True

        return {
            "tipo": "texto",
            "mensagem": f"""📋 Solicitação de sinistro registrada.

Responsável: {session["dados"]["responsavel"]}
CPF: {session["dados"]["cpf"]}
Falecido(a): {session["dados"]["falecido"]}
Cidade: {session["dados"]["cidade_sinistro"]}

👨‍💼 Você será encaminhado para nosso atendimento."""
        }

    return renderizar()