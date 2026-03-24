from datetime import datetime

from core.firebase import salvar_pedido
from core.urnas import listar_urnas
from core.pagamentos import formatar_reais


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


def _menu(titulo, opcoes):
    return {
        "tipo": "botoes",
        "mensagem": titulo,
        "botoes": [{"id": op[0], "label": op[1]} for op in opcoes]
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

    return {
        "tipo": "texto",
        "mensagem": "Voltando ao menu principal..."
    }


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

    nome = session.get("nome", "Cliente")

    # atalhos globais
    if mensagem == "9":
        return _ir_para_atendente(session, mensagem)

    if session["etapa"] != "inicio" and mensagem == "00":
        return _voltar_menu_principal(session)

    # ---------------------------
    # INICIO
    # ---------------------------

    if session["etapa"] == "inicio":
        session["dados"] = {}
        session["etapa"] = "endereco"

        return {
            "tipo": "texto",
            "mensagem": f"""⚰️ Atendimento Funerário

{nome}, vamos iniciar seu atendimento.

📍 Informe o endereço do local."""
        }

    # ---------------------------
    # ENDEREÇO
    # ---------------------------

    if session["etapa"] == "endereco":
        session["dados"]["nome"] = nome
        session["dados"]["endereco"] = mensagem
        session["etapa"] = "tipo_servico"

        return _menu(
            "⚰️ Qual o tipo de serviço?",
            [
                ("1", "Sepultamento"),
                ("2", "Cremação"),
                ("9", "Falar com atendente"),
                ("00", "Menu principal"),
            ]
        )

    # ---------------------------
    # TIPO SERVIÇO
    # ---------------------------

    if session["etapa"] == "tipo_servico":

        if mensagem == "1":
            session["dados"]["tipo_servico"] = "Sepultamento"
        elif mensagem == "2":
            session["dados"]["tipo_servico"] = "Cremação"
        else:
            return {"tipo": "texto", "mensagem": "Escolha 1 ou 2."}

        session["etapa"] = "porte_corpo"

        return _menu(
            "Qual o porte do corpo?",
            [
                ("1", "Até 80kg"),
                ("2", "80kg até 120kg"),
                ("3", "Acima de 120kg"),
                ("0", "Voltar"),
                ("9", "Atendente"),
                ("00", "Menu"),
            ]
        )

    # ---------------------------
    # PORTE CORPO
    # ---------------------------

    if session["etapa"] == "porte_corpo":

        opcoes = {
            "1": "Até 80kg",
            "2": "80kg até 120kg",
            "3": "Acima de 120kg",
        }

        if mensagem not in opcoes:
            return {"tipo": "texto", "mensagem": "Escolha 1, 2 ou 3."}

        session["dados"]["porte_corpo"] = opcoes[mensagem]
        session["etapa"] = "tipo_urna"

        return _menu(
            "Escolha o tipo de urna:",
            [
                ("1", "Simples"),
                ("2", "Intermediária"),
                ("3", "Premium"),
                ("0", "Voltar"),
                ("9", "Atendente"),
                ("00", "Menu"),
            ]
        )

    # ---------------------------
    # TIPO URNA
    # ---------------------------

    if session["etapa"] == "tipo_urna":

        opcoes = {
            "1": "Simples",
            "2": "Intermediária",
            "3": "Premium",
        }

        if mensagem not in opcoes:
            return {"tipo": "texto", "mensagem": "Escolha 1, 2 ou 3."}

        session["dados"]["tipo_urna"] = opcoes[mensagem]
        session["etapa"] = "urna_modelo"

        urnas = listar_urnas()
        session["urnas"] = urnas

        botoes = []
        for i, urna in enumerate(urnas):
            botoes.append((str(i+1), f"{urna['nome']} - {formatar_reais(urna['preco'])}"))

        botoes += [("0", "Voltar"), ("9", "Atendente"), ("00", "Menu")]

        return _menu("Escolha o modelo da urna:", botoes)

    # ---------------------------
    # MODELO URNA
    # ---------------------------

    if session["etapa"] == "urna_modelo":

        urnas = session.get("urnas", [])

        try:
            urna = urnas[int(mensagem)-1]
        except:
            return {"tipo": "texto", "mensagem": "Escolha válida."}

        session["dados"]["modelo_urna"] = urna["nome"]
        session["dados"]["valor_urna_modelo"] = urna["preco"]

        session["etapa"] = "velorio"

        return _menu(
            f"Modelo: {urna['nome']}\n\nHaverá velório?",
            [
                ("1", "Sim"),
                ("2", "Não"),
                ("0", "Voltar"),
                ("9", "Atendente"),
                ("00", "Menu"),
            ]
        )

    # ---------------------------
    # VELÓRIO
    # ---------------------------

    if session["etapa"] == "velorio":

        if mensagem not in ["1", "2"]:
            return {"tipo": "texto", "mensagem": "Escolha 1 ou 2."}

        session["dados"]["velorio"] = "Sim" if mensagem == "1" else "Não"
        session["etapa"] = "translado"

        return _menu(
            "Haverá translado?",
            [
                ("1", "Sim"),
                ("2", "Não"),
                ("0", "Voltar"),
                ("9", "Atendente"),
                ("00", "Menu"),
            ]
        )

    # ---------------------------
    # TRANSLADO
    # ---------------------------

    if session["etapa"] == "translado":

        if mensagem not in ["1", "2"]:
            return {"tipo": "texto", "mensagem": "Escolha 1 ou 2."}

        session["dados"]["translado"] = "Sim" if mensagem == "1" else "Não"
        session["etapa"] = "local"

        return {
            "tipo": "texto",
            "mensagem": "📍 Informe o local de entrega."
        }

    # ---------------------------
    # LOCAL
    # ---------------------------

    if session["etapa"] == "local":

        session["dados"]["local_entrega"] = mensagem
        session["etapa"] = "confirmacao"

        total = _calcular_valor_total(session["dados"])

        return _menu(
            f"Resumo\n\nValor: {formatar_reais(total)}\n\nConfirmar?",
            [
                ("1", "Confirmar"),
                ("2", "Refazer"),
                ("9", "Atendente"),
                ("00", "Menu"),
            ]
        )

    # ---------------------------
    # CONFIRMAÇÃO (🔥 AQUI ESTÁ A MÁGICA)
    # ---------------------------

    if session["etapa"] == "confirmacao":

        if mensagem == "1":

            dados = session["dados"]
            valor_total = _calcular_valor_total(dados)

            payload = {
                "tipo": "funeraria",
                "telefone": session.get("numero"),  # 🔥 vem automático do WhatsApp
                "nome": session.get("nome"),
                "endereco": dados.get("endereco"),
                "tipo_servico": dados.get("tipo_servico"),
                "porte_corpo": dados.get("porte_corpo"),
                "tipo_urna": dados.get("tipo_urna"),
                "modelo_urna": dados.get("modelo_urna"),
                "valor_urna_modelo": dados.get("valor_urna_modelo"),
                "velorio": dados.get("velorio"),
                "translado": dados.get("translado"),
                "local_entrega": dados.get("local_entrega"),
                "valor_total": valor_total,
                "status": "novo",
                "criado_em": datetime.now().isoformat(),
            }

            salvar_pedido(payload)

            session["etapa"] = "finalizado"
            session["encerrar_bot"] = True

            return {
                "tipo": "texto",
                "mensagem": f"""✅ Pedido confirmado com sucesso!

📞 Telefone: {session.get("numero")}

Em breve nossa equipe entrará em contato."""
            }

        if mensagem == "2":
            session["etapa"] = "inicio"
            return {
                "tipo": "texto",
                "mensagem": "Reiniciando atendimento..."
            }

        return {"tipo": "texto", "mensagem": "Escolha válida."}