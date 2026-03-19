from datetime import datetime

from core.menus import criar_menu
from core.firebase import salvar_pedido
from core.urnas import listar_urnas
from core.pagamentos import (
    gerar_link_pagamento_sinal,
    gerar_referencia_externa,
    formatar_reais,
)


PRECO_TIPO_SERVICO = {
    "Sepultamento": 3500.00,
    "Cremação": 5200.00,
}

PRECO_PORTE_CORPO = {
    "Até 80kg": 0.00,
    "80kg até 120kg": 450.00,
    "Acima de 120kg": 900.00,
}

PRECO_TIPO_URNA = {
    "Simples": 0.00,
    "Intermediária": 1200.00,
    "Premium": 2800.00,
}

PRECO_VELORIO = {
    "Sim": 850.00,
    "Não": 0.00,
}

PRECO_TRANSLADO = {
    "Sim": 600.00,
    "Não": 0.00,
}


def _ir_para_atendente(session, mensagem):
    session["fluxo"] = "atendente"
    from fluxos.atendente import fluxo_atendente
    return fluxo_atendente(session, mensagem)


def _voltar_menu_principal(session):
    session["fluxo"] = None
    session["etapa"] = "inicio"
    session["dados"] = {}
    session.pop("urnas", None)
    return "Voltando ao menu principal..."


def _calcular_valor_total(dados):
    total = 0.0

    total += PRECO_TIPO_SERVICO.get(dados.get("tipo_servico"), 0.0)
    total += PRECO_PORTE_CORPO.get(dados.get("porte_corpo"), 0.0)
    total += PRECO_TIPO_URNA.get(dados.get("tipo_urna"), 0.0)
    total += PRECO_VELORIO.get(dados.get("velorio"), 0.0)
    total += PRECO_TRANSLADO.get(dados.get("translado"), 0.0)
    total += float(dados.get("valor_urna_modelo", 0.0) or 0.0)

    return round(total, 2)


def fluxo_funeraria(session, mensagem):
    if "etapa" not in session:
        session["etapa"] = "inicio"

    if "dados" not in session:
        session["dados"] = {}

    nome = session.get("nome", "Cliente").strip().title()

    # ---------------------------
    # ATALHOS GLOBAIS
    # ---------------------------

    if mensagem == "9":
        return _ir_para_atendente(session, mensagem)

    if session["etapa"] != "inicio" and mensagem == "00":
        return _voltar_menu_principal(session)

    # ---------------------------
    # INICIO
    # ---------------------------

    if session["etapa"] == "inicio":
        session["dados"] = {}
        session.pop("urnas", None)
        session["etapa"] = "endereco"

        return f"""
⚰️ Atendimento Funerário

{nome}, vamos iniciar seu atendimento.

📍 Informe o endereço do local.

Digite:
9  - Falar com atendente
00 - Voltar ao menu principal
"""

    # ---------------------------
    # ENDEREÇO
    # ---------------------------

    if session["etapa"] == "endereco":
        session["dados"]["nome"] = nome
        session["dados"]["endereco"] = mensagem
        session["etapa"] = "tipo_servico"

        return criar_menu(
            "⚰️ Qual o tipo de serviço?",
            [
                ("1", "Sepultamento"),
                ("2", "Cremação"),
                ("9", "Falar com atendente"),
                ("00", "Voltar ao menu principal"),
            ]
        )

    # ---------------------------
    # TIPO DE SERVIÇO
    # ---------------------------

    if session["etapa"] == "tipo_servico":
        if mensagem == "0":
            session["etapa"] = "endereco"
            return "📍 Informe novamente o endereço do local."

        if mensagem == "1":
            session["dados"]["tipo_servico"] = "Sepultamento"
        elif mensagem == "2":
            session["dados"]["tipo_servico"] = "Cremação"
        else:
            return "Escolha 1 ou 2. Digite 0 para voltar, 9 para atendente ou 00 para menu principal."

        session["etapa"] = "porte_corpo"

        return criar_menu(
            "Qual o porte do corpo?",
            [
                ("1", "Até 80kg"),
                ("2", "80kg até 120kg"),
                ("3", "Acima de 120kg"),
                ("0", "Voltar"),
                ("9", "Falar com atendente"),
                ("00", "Voltar ao menu principal"),
            ]
        )

    # ---------------------------
    # PORTE DO CORPO
    # ---------------------------

    if session["etapa"] == "porte_corpo":
        if mensagem == "0":
            session["etapa"] = "tipo_servico"
            return criar_menu(
                "⚰️ Qual o tipo de serviço?",
                [
                    ("1", "Sepultamento"),
                    ("2", "Cremação"),
                    ("9", "Falar com atendente"),
                    ("00", "Voltar ao menu principal"),
                ]
            )

        opcoes = {
            "1": "Até 80kg",
            "2": "80kg até 120kg",
            "3": "Acima de 120kg",
        }

        if mensagem not in opcoes:
            return "Escolha 1, 2 ou 3. Digite 0 para voltar, 9 para atendente ou 00 para menu principal."

        session["dados"]["porte_corpo"] = opcoes[mensagem]
        session["etapa"] = "tipo_urna"

        return criar_menu(
            "Escolha o tipo de urna:",
            [
                ("1", "Simples"),
                ("2", "Intermediária"),
                ("3", "Premium"),
                ("0", "Voltar"),
                ("9", "Falar com atendente"),
                ("00", "Voltar ao menu principal"),
            ]
        )

    # ---------------------------
    # TIPO DE URNA
    # ---------------------------

    if session["etapa"] == "tipo_urna":
        if mensagem == "0":
            session["etapa"] = "porte_corpo"
            return criar_menu(
                "Qual o porte do corpo?",
                [
                    ("1", "Até 80kg"),
                    ("2", "80kg até 120kg"),
                    ("3", "Acima de 120kg"),
                    ("0", "Voltar"),
                    ("9", "Falar com atendente"),
                    ("00", "Voltar ao menu principal"),
                ]
            )

        opcoes = {
            "1": "Simples",
            "2": "Intermediária",
            "3": "Premium",
        }

        if mensagem not in opcoes:
            return "Escolha 1, 2 ou 3. Digite 0 para voltar, 9 para atendente ou 00 para menu principal."

        session["dados"]["tipo_urna"] = opcoes[mensagem]
        session["etapa"] = "urna_modelo"

        urnas = listar_urnas()
        session["urnas"] = urnas

        opcoes_menu = []
        for i, urna in enumerate(urnas):
            nome_urna = urna.get("nome", f"Urna {i+1}")
            preco_urna = float(urna.get("preco", 0.0) or 0.0)
            opcoes_menu.append((str(i + 1), f'{nome_urna} - {formatar_reais(preco_urna)}'))

        opcoes_menu.append(("0", "Voltar"))
        opcoes_menu.append(("9", "Falar com atendente"))
        opcoes_menu.append(("00", "Voltar ao menu principal"))

        return criar_menu("Escolha o modelo da urna:", opcoes_menu)

    # ---------------------------
    # MODELO URNA
    # ---------------------------

    if session["etapa"] == "urna_modelo":
        if mensagem == "0":
            session["etapa"] = "tipo_urna"
            return criar_menu(
                "Escolha o tipo de urna:",
                [
                    ("1", "Simples"),
                    ("2", "Intermediária"),
                    ("3", "Premium"),
                    ("0", "Voltar"),
                    ("9", "Falar com atendente"),
                    ("00", "Voltar ao menu principal"),
                ]
            )

        urnas = session.get("urnas", [])

        try:
            urna = urnas[int(mensagem) - 1]
        except Exception:
            return "Escolha uma opção válida. Digite 0 para voltar, 9 para atendente ou 00 para menu principal."

        session["dados"]["modelo_urna"] = urna.get("nome")
        session["dados"]["urna_id"] = urna.get("id")
        session["dados"]["urna_imagem"] = urna.get("imagem")
        session["dados"]["valor_urna_modelo"] = float(urna.get("preco", 0.0) or 0.0)

        session["etapa"] = "velorio"

        imagem = urna.get("imagem")
        texto_imagem = f"\n📷 Foto da urna: {imagem}" if imagem else ""

        return criar_menu(
            f"Modelo selecionado: {urna.get('nome')}{texto_imagem}\n\nHaverá velório?",
            [
                ("1", "Sim"),
                ("2", "Não"),
                ("0", "Voltar"),
                ("9", "Falar com atendente"),
                ("00", "Voltar ao menu principal"),
            ]
        )

    # ---------------------------
    # VELÓRIO
    # ---------------------------

    if session["etapa"] == "velorio":
        if mensagem == "0":
            session["etapa"] = "urna_modelo"

            urnas = session.get("urnas", [])
            opcoes_menu = []
            for i, urna in enumerate(urnas):
                nome_urna = urna.get("nome", f"Urna {i+1}")
                preco_urna = float(urna.get("preco", 0.0) or 0.0)
                opcoes_menu.append((str(i + 1), f'{nome_urna} - {formatar_reais(preco_urna)}'))

            opcoes_menu.append(("0", "Voltar"))
            opcoes_menu.append(("9", "Falar com atendente"))
            opcoes_menu.append(("00", "Voltar ao menu principal"))

            return criar_menu("Escolha o modelo da urna:", opcoes_menu)

        opcoes = {
            "1": "Sim",
            "2": "Não",
        }

        if mensagem not in opcoes:
            return "Escolha 1 ou 2. Digite 0 para voltar, 9 para atendente ou 00 para menu principal."

        session["dados"]["velorio"] = opcoes[mensagem]
        session["etapa"] = "translado"

        return criar_menu(
            "Haverá translado?",
            [
                ("1", "Sim"),
                ("2", "Não"),
                ("0", "Voltar"),
                ("9", "Falar com atendente"),
                ("00", "Voltar ao menu principal"),
            ]
        )

    # ---------------------------
    # TRANSLADO
    # ---------------------------

    if session["etapa"] == "translado":
        if mensagem == "0":
            session["etapa"] = "velorio"
            return criar_menu(
                "Haverá velório?",
                [
                    ("1", "Sim"),
                    ("2", "Não"),
                    ("0", "Voltar"),
                    ("9", "Falar com atendente"),
                    ("00", "Voltar ao menu principal"),
                ]
            )

        opcoes = {
            "1": "Sim",
            "2": "Não",
        }

        if mensagem not in opcoes:
            return "Escolha 1 ou 2. Digite 0 para voltar, 9 para atendente ou 00 para menu principal."

        session["dados"]["translado"] = opcoes[mensagem]
        session["etapa"] = "local_entrega"

        return """
📍 Informe o local de entrega.

Digite:
0  - Voltar
9  - Falar com atendente
00 - Voltar ao menu principal
"""

    # ---------------------------
    # LOCAL ENTREGA
    # ---------------------------

    if session["etapa"] == "local_entrega":
        if mensagem == "0":
            session["etapa"] = "translado"
            return criar_menu(
                "Haverá translado?",
                [
                    ("1", "Sim"),
                    ("2", "Não"),
                    ("0", "Voltar"),
                    ("9", "Falar com atendente"),
                    ("00", "Voltar ao menu principal"),
                ]
            )

        session["dados"]["local_entrega"] = mensagem
        session["etapa"] = "observacao"

        return criar_menu(
            "Deseja adicionar alguma observação?",
            [
                ("1", "Sim"),
                ("2", "Não"),
                ("0", "Voltar"),
                ("9", "Falar com atendente"),
                ("00", "Voltar ao menu principal"),
            ]
        )

    # ---------------------------
    # OBSERVAÇÃO
    # ---------------------------

    if session["etapa"] == "observacao":
        if mensagem == "0":
            session["etapa"] = "local_entrega"
            return """
📍 Informe novamente o local de entrega.

Digite:
0  - Voltar
9  - Falar com atendente
00 - Voltar ao menu principal
"""

        if mensagem == "1":
            session["etapa"] = "digitar_observacao"
            return """
Digite a observação.

Digite:
0  - Voltar
9  - Falar com atendente
00 - Voltar ao menu principal
"""
        elif mensagem == "2":
            session["dados"]["observacao"] = "Nenhuma"
            session["dados"]["valor_total"] = _calcular_valor_total(session["dados"])
            session["etapa"] = "resumo"
        else:
            return "Escolha 1 ou 2. Digite 0 para voltar, 9 para atendente ou 00 para menu principal."

    # ---------------------------
    # DIGITAR OBSERVAÇÃO
    # ---------------------------

    if session["etapa"] == "digitar_observacao":
        if mensagem == "0":
            session["etapa"] = "observacao"
            return criar_menu(
                "Deseja adicionar alguma observação?",
                [
                    ("1", "Sim"),
                    ("2", "Não"),
                    ("0", "Voltar"),
                    ("9", "Falar com atendente"),
                    ("00", "Voltar ao menu principal"),
                ]
            )

        session["dados"]["observacao"] = mensagem
        session["dados"]["valor_total"] = _calcular_valor_total(session["dados"])
        session["etapa"] = "resumo"

    # ---------------------------
    # RESUMO FINAL
    # ---------------------------

    if session["etapa"] == "resumo":
        dados = session["dados"]
        valor_total = float(dados.get("valor_total", 0.0) or 0.0)
        valor_sinal = round(valor_total * 0.10, 2)

        session["etapa"] = "confirmacao"

        return f"""
📋 RESUMO DO ATENDIMENTO

Nome: {session.get("nome")}
Endereço: {dados.get("endereco")}
Serviço: {dados.get("tipo_servico")}
Porte do corpo: {dados.get("porte_corpo")}
Tipo de urna: {dados.get("tipo_urna")}
Modelo da urna: {dados.get("modelo_urna")}
Velório: {dados.get("velorio")}
Translado: {dados.get("translado")}
Local de entrega: {dados.get("local_entrega")}
Observação: {dados.get("observacao")}

💰 Valor total estimado: {formatar_reais(valor_total)}
💳 Sinal para garantia (10%): {formatar_reais(valor_sinal)}

1 - Confirmar e gerar link de pagamento
2 - Corrigir
9 - Falar com atendente
00 - Voltar ao menu principal
"""

    # ---------------------------
    # CONFIRMAÇÃO
    # ---------------------------

    if session["etapa"] == "confirmacao":
        if mensagem == "1":
            dados = session["dados"]
            valor_total = float(dados.get("valor_total", 0.0) or 0.0)
            referencia_externa = gerar_referencia_externa("funeraria")

            pagamento = gerar_link_pagamento_sinal(
                valor_total=valor_total,
                nome_cliente=session.get("nome", "Cliente"),
                referencia_externa=referencia_externa,
            )

            payload = {
                "tipo": "funeraria",
                "telefone": session.get("numero"),
                "nome": session.get("nome"),
                "endereco": dados.get("endereco"),
                "tipo_servico": dados.get("tipo_servico"),
                "porte_corpo": dados.get("porte_corpo"),
                "tipo_urna": dados.get("tipo_urna"),
                "modelo_urna": dados.get("modelo_urna"),
                "urna_id": dados.get("urna_id"),
                "urna_imagem": dados.get("urna_imagem"),
                "valor_urna_modelo": dados.get("valor_urna_modelo"),
                "velorio": dados.get("velorio"),
                "translado": dados.get("translado"),
                "local_entrega": dados.get("local_entrega"),
                "observacao": dados.get("observacao"),
                "valor_total": valor_total,
                "valor_sinal": pagamento["valor_sinal"],
                "link_pagamento": pagamento["link_pagamento"],
                "mercado_pago_preference_id": pagamento["preference_id"],
                "external_reference": referencia_externa,
                "status": "aguardando_pagamento_sinal",
                "criado_em": datetime.now().isoformat(),
            }

            salvar_pedido(payload)

            session["etapa"] = "finalizado"
            session["encerrar_bot"] = True

            return f"""
✅ Pedido confirmado com sucesso.

Para garantir o atendimento, realize o pagamento do sinal de 10%:

💳 Valor do sinal: {formatar_reais(pagamento["valor_sinal"])}
🔗 Link de pagamento:
{pagamento["link_pagamento"]}

Assim que o pagamento for identificado, o atendimento poderá seguir normalmente.
"""

        if mensagem == "2":
            session["etapa"] = "endereco"
            session["dados"] = {}
            session.pop("urnas", None)
            return "Vamos reiniciar o atendimento funerário.\n\n📍 Informe o endereço do local."

        return "Escolha 1 ou 2. Digite 9 para atendente ou 00 para menu principal."