from integracoes.zapi import enviar_texto

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
def aviso_funeraria(nome, telefone, dados, servico=None):
    linhas = [
        f"👤 Nome: {nome or '-'}",
        f"📞 Telefone: {telefone or '-'}",
    ]

    if dados.get("velorio"):
        linhas.append(f"🕯️ Velório: {label_velorio(dados.get('velorio'))}")

    if dados.get("local_velorio"):
        linhas.append(f"🏛️ Local do velório: {label_local_velorio(dados.get('local_velorio'))}")

    if dados.get("endereco_velorio"):
        linhas.append(f"📍 Endereço do velório: {dados.get('endereco_velorio')}")

    if dados.get("data_velorio"):
        linhas.append(f"📅 Data do velório: {dados.get('data_velorio')}")

    if dados.get("local_corpo"):
        linhas.append(f"📍 Local do ente querido: {label_local_corpo(dados.get('local_corpo'))}")

    if dados.get("hospital_nome"):
        linhas.append(f"🏥 Hospital: {dados.get('hospital_nome')}")

    if dados.get("endereco_local_corpo"):
        linhas.append(f"📌 Endereço atual: {dados.get('endereco_local_corpo')}")

    if dados.get("liberacao_hospital"):
        linhas.append(f"🧾 Liberação no necrotério: {dados.get('liberacao_hospital')}")

    if dados.get("porte"):
        linhas.append(f"⚖️ Porte: {label_porte(dados.get('porte'))}")

    if dados.get("destino"):
        linhas.append(f"⚱️ Destino: {dados.get('destino')}")

    if dados.get("cemiterio"):
        linhas.append(f"🪦 Cemitério: {dados.get('cemiterio')}")

    if dados.get("despedida"):
        linhas.append(f"🙏 Despedida: {dados.get('despedida')}")

    if servico:
        if servico.get("nome"):
            linhas.append(f"⚰️ Serviço: {servico.get('nome')}")

        if servico.get("preco"):
            linhas.append(f"💰 Valor: {servico.get('preco')}")

    return enviar_aviso_interno("Novo atendimento funerário", linhas)

def aviso_orcamento(nome, telefone, dados):
    servico = dados.get("servico", {})

    linhas = [
        f"👤 Nome: {dados.get('nome') or nome or '-'}",
        f"📞 Telefone: {telefone or '-'}",
        f"🏢 Interesse: {servico.get('nome', '-')}",
        f"🏙️ Cidade: {dados.get('cidade', '-')}",
        f"📅 Data: {dados.get('data', '-')}",
    ]

    return enviar_aviso_interno("Novo orçamento funerário", linhas)


def aviso_floricultura(nome, telefone, carrinho):
    linhas = [
        f"👤 Nome: {nome or '-'}",
        f"📞 Telefone: {telefone or '-'}",
        "🌸 Pedido:",
    ]

    if carrinho:
        for item in carrinho:
            linhas.append(f"• {item}")
    else:
        linhas.append("• Sem itens informados")

    return enviar_aviso_interno("Novo pedido floricultura", linhas)


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
    linhas = [
        f"👤 Nome: {nome or '-'}",
        f"📞 Telefone: {telefone or '-'}",
        f"📍 Origem: {origem}",
    ]

    return enviar_aviso_interno("Cliente pediu atendente", linhas)