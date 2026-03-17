from core.menus import criar_menu
from core.firebase import salvar_pedido
from core.urnas import listar_urnas
from datetime import datetime


def fluxo_funeraria(session, mensagem):

    if "etapa" not in session:
        session["etapa"] = "inicio"

    if "dados" not in session:
        session["dados"] = {}

    # ---------------------------
    # INICIO
    # ---------------------------

    if session["etapa"] == "inicio":

        session["etapa"] = "nome"

        return """
⚰️ Atendimento Funerário

Qual é o nome da pessoa responsável?
"""

    # ---------------------------
    # NOME
    # ---------------------------

    if session["etapa"] == "nome":

        session["dados"]["nome"] = mensagem
        session["etapa"] = "endereco"

        return "📍 Informe o endereço do local."

    # ---------------------------
    # ENDEREÇO
    # ---------------------------

    if session["etapa"] == "endereco":

        session["dados"]["endereco"] = mensagem
        session["etapa"] = "tipo_servico"

        return criar_menu(
            "⚰️ Qual o tipo de serviço?",
            [
                ("1", "Sepultamento"),
                ("2", "Cremação")
            ]
        )

    # ---------------------------
    # TIPO DE SERVIÇO
    # ---------------------------

    if session["etapa"] == "tipo_servico":

        if mensagem == "1":
            session["dados"]["tipo_servico"] = "Sepultamento"

        elif mensagem == "2":
            session["dados"]["tipo_servico"] = "Cremação"

        else:
            return "Escolha 1 ou 2."

        session["etapa"] = "porte_corpo"

        return criar_menu(
            "Qual o porte do corpo?",
            [
                ("1", "Até 80kg"),
                ("2", "80kg até 120kg"),
                ("3", "Acima de 120kg")
            ]
        )

    # ---------------------------
    # PORTE DO CORPO
    # ---------------------------

    if session["etapa"] == "porte_corpo":

        opcoes = {
            "1": "Até 80kg",
            "2": "80kg até 120kg",
            "3": "Acima de 120kg"
        }

        if mensagem not in opcoes:
            return "Escolha 1, 2 ou 3."

        session["dados"]["porte_corpo"] = opcoes[mensagem]
        session["etapa"] = "tipo_urna"

        return criar_menu(
            "Escolha o tipo de urna:",
            [
                ("1", "Simples"),
                ("2", "Intermediária"),
                ("3", "Premium")
            ]
        )

    # ---------------------------
    # TIPO DE URNA
    # ---------------------------

    if session["etapa"] == "tipo_urna":

        opcoes = {
            "1": "Simples",
            "2": "Intermediária",
            "3": "Premium"
        }

        if mensagem not in opcoes:
            return "Escolha 1, 2 ou 3."

        session["dados"]["tipo_urna"] = opcoes[mensagem]
        session["etapa"] = "urna_modelo"

        urnas = listar_urnas()

        opcoes = []

        for i, urna in enumerate(urnas):
            opcoes.append((str(i+1), urna["nome"]))

        session["urnas"] = urnas

        return criar_menu(
            "Escolha o modelo da urna:",
            opcoes
        )


    

    # ---------------------------
    # MODELO URNA
    # ---------------------------

    if session["etapa"] == "urna_modelo":

        urnas = session.get("urnas", [])

        try:
            urna = urnas[int(mensagem) - 1]
        except:
            return "Escolha uma opção válida."

        session["dados"]["modelo_urna"] = urna["nome"]
        session["dados"]["urna_id"] = urna["id"]
        session["dados"]["urna_imagem"] = urna["imagem"]

        session["etapa"] = "velorio"

        return criar_menu(
            "Haverá velório?",
            [
                ("1", "Sim"),
                ("2", "Não")
            ]
        )

    # ---------------------------
    # VELÓRIO
    # ---------------------------

    if session["etapa"] == "velorio":

        opcoes = {
            "1": "Sim",
            "2": "Não"
        }

        if mensagem not in opcoes:
            return "Escolha 1 ou 2."

        session["dados"]["velorio"] = opcoes[mensagem]
        session["etapa"] = "translado"

        return criar_menu(
            "Haverá translado?",
            [
                ("1", "Sim"),
                ("2", "Não")
            ]
        )

    # ---------------------------
    # TRANSLADO
    # ---------------------------

    if session["etapa"] == "translado":

        opcoes = {
            "1": "Sim",
            "2": "Não"
        }

        if mensagem not in opcoes:
            return "Escolha 1 ou 2."

        session["dados"]["translado"] = opcoes[mensagem]
        session["etapa"] = "local_entrega"

        return "📍 Informe o local de entrega."

    # ---------------------------
    # LOCAL ENTREGA
    # ---------------------------

    if session["etapa"] == "local_entrega":

        session["dados"]["local_entrega"] = mensagem
        session["etapa"] = "observacao"

        return criar_menu(
            "Deseja adicionar alguma observação?",
            [
                ("1", "Sim"),
                ("2", "Não")
            ]
        )

    # ---------------------------
    # OBSERVAÇÃO
    # ---------------------------

    if session["etapa"] == "observacao":

        if mensagem == "1":

            session["etapa"] = "digitar_observacao"

            return "Digite a observação."

        elif mensagem == "2":

            session["dados"]["observacao"] = "Nenhuma"
            session["etapa"] = "resumo"

        else:
            return "Escolha 1 ou 2."

    # ---------------------------
    # DIGITAR OBSERVAÇÃO
    # ---------------------------

    if session["etapa"] == "digitar_observacao":

        session["dados"]["observacao"] = mensagem
        session["etapa"] = "resumo"

    # ---------------------------
    # RESUMO FINAL
    # ---------------------------

    if session["etapa"] == "resumo":

        dados = session["dados"]

        session["etapa"] = "confirmacao"

        return f"""
📋 RESUMO DO ATENDIMENTO

Nome: {dados["nome"]}
Endereço: {dados["endereco"]}
Serviço: {dados["tipo_servico"]}
Porte do corpo: {dados["porte_corpo"]}
Tipo de urna: {dados["tipo_urna"]}
Modelo da urna: {dados["modelo_urna"]}
Velório: {dados["velorio"]}
Translado: {dados["translado"]}
Local de entrega: {dados["local_entrega"]}
Observação: {dados["observacao"]}

1 - Confirmar
2 - Corrigir
"""

    # ---------------------------
    # CONFIRMAÇÃO
    # ---------------------------

    if session["etapa"] == "confirmacao":

        if mensagem == "1":

            salvar_pedido({
                "tipo": "funeraria",
                "telefone": session.get("numero"),
                "nome": session["dados"]["nome"],
                "endereco": session["dados"]["endereco"],
                "tipo_servico": session["dados"]["tipo_servico"],
                "porte_corpo": session["dados"]["porte_corpo"],
                "tipo_urna": session["dados"]["tipo_urna"],
                "modelo_urna": session["dados"]["modelo_urna"],
                "velorio": session["dados"]["velorio"],
                "translado": session["dados"]["translado"],
                "local_entrega": session["dados"]["local_entrega"],
                "observacao": session["dados"]["observacao"],
                "status": "novo",
                "criado_em": datetime.now().isoformat()
            })

            session["etapa"] = "finalizado"

            return """
✅ Pedido confirmado

Em breve um atendente entrará em contato para acompanhar o atendimento.
"""

        if mensagem == "2":

            session["etapa"] = "inicio"

            return "Vamos reiniciar o atendimento."

        return "Escolha 1 ou 2."