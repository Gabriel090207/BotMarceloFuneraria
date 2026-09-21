from integracoes.zapi import enviar_texto
from core.notificacoes import criar_notificacao

NUMERO_AVISOS = "5592995131313"
NUMERO_PLANTONISTA = "5592995131313"


def enviar_aviso_interno(titulo, linhas):
    mensagem = f"🚨 *{titulo}*\n\n" + "\n".join(linhas)
    return enviar_texto(NUMERO_AVISOS, mensagem)


# =========================
# FORMATADORES
# =========================

def label_velorio(valor):
    mapa = {
        "1": "Sim",
        "2": "Não",
        "sim": "Sim",
        "nao": "Não",
    }
    return mapa.get(str(valor).lower(), str(valor))


def label_local_velorio(valor):
    mapa = {
        "1": "Na Funerária Canaã",
        "2": "Em igreja ou residência",
        "funeraria": "Na Funerária Canaã",
        "externo": "Em igreja ou residência",
    }
    return mapa.get(str(valor).lower(), str(valor))


def label_local_corpo(valor):
    mapa = {
        "1": "Hospital",
        "2": "Residência",
        "3": "IML",
        "4": "Outro",
    }
    return mapa.get(str(valor), str(valor))


def label_porte(valor):
    mapa = {
        "1": "Até 85kg",
        "2": "Entre 85kg e 130kg",
        "3": "Acima de 130kg",
    }
    return mapa.get(str(valor), str(valor))


# =========================
# AVISOS
# =========================
def aviso_funeraria(nome, telefone, dados, servico=None, *, pedido_id):
    snapshot = {}
    if servico and servico.get("nome"):
        snapshot["servico_nome"] = servico["nome"]
    if dados.get("data_velorio"):
        snapshot["data_velorio"] = dados["data_velorio"]

    return criar_notificacao(
        tipo="funeraria_resumo_confirmado",
        titulo="Atendimento funerário confirmado",
        telefone_cliente=telefone,
        nome_cliente=nome,
        origem="Serviços funerários",
        pedido_id=pedido_id,
        dados=snapshot,
    )


def aviso_orcamento(nome, telefone, dados):
    servico = dados.get("servico", {})

    return criar_notificacao(
        tipo="orcamento_funerario_solicitado",
        titulo="Orçamento funerário solicitado",
        telefone_cliente=telefone,
        nome_cliente=dados.get("nome") or nome,
        origem="Orçamento funerário",
        dados={
            "servico": servico.get("nome"),
            "cidade": dados.get("cidade"),
            "data": dados.get("data"),
        },
    )


def aviso_floricultura(nome, telefone, carrinho):
    return criar_notificacao(
        tipo="floricultura_pedido_solicitado",
        titulo="Pedido de floricultura",
        telefone_cliente=telefone,
        nome_cliente=nome,
        origem="Floricultura",
        dados={"itens": [{"nome": item} for item in (carrinho or [])]},
    )


def aviso_planos(nome, telefone, dados=None):
    dados = dados or {}

    linhas = [
        f"👤 Nome: {nome or '-'}",
        f"📞 Telefone: {telefone or '-'}",
    ]

    for chave, valor in dados.items():
        linhas.append(f"• {chave}: {valor}")

    return enviar_aviso_interno("Novo atendimento planos", linhas)


def aviso_financeiro(nome, telefone, dados=None):
    dados = dados or {}

    linhas = [
        f"👤 Nome: {nome or '-'}",
        f"📞 Telefone: {telefone or '-'}",
    ]

    for chave, valor in dados.items():
        linhas.append(f"• {chave}: {valor}")

    return enviar_aviso_interno("Novo atendimento financeiro", linhas)


def aviso_atendente(nome, telefone, origem):
    return criar_notificacao(
        tipo="atendimento_humano_solicitado",
        titulo="Atendimento humano solicitado",
        telefone_cliente=telefone,
        nome_cliente=nome,
        origem=origem,
    )
