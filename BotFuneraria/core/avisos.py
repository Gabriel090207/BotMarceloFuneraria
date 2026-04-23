from integracoes.zapi import enviar_texto

NUMERO_AVISOS = "5516993996654"


def enviar_aviso_interno(titulo, linhas):
    mensagem = f"🚨 *{titulo}*\n\n" + "\n".join(linhas)
    return enviar_texto(NUMERO_AVISOS, mensagem)


def aviso_funeraria(nome, telefone, dados, servico=None):
    linhas = [
        f"👤 Nome: {nome or '-'}",
        f"📞 Telefone: {telefone or '-'}",
        f"🕯️ Velório: {dados.get('velorio', '-')}",
        f"🏛️ Local do velório: {dados.get('local_velorio', '-')}",
        f"📅 Data do velório: {dados.get('data_velorio', '-')}",
        f"📍 Local do ente querido: {dados.get('local_corpo', '-')}",
        f"📌 Endereço atual: {dados.get('endereco_local_corpo', '-')}",
        f"⚖️ Porte: {dados.get('porte', '-')}",
    ]

    if dados.get("hospital_nome"):
        linhas.append(f"🏥 Hospital: {dados.get('hospital_nome')}")

    if dados.get("liberacao_hospital"):
        linhas.append(f"🧾 Liberação no necrotério: {dados.get('liberacao_hospital')}")

    if servico:
        linhas.append(f"⚰️ Serviço: {servico.get('nome', '-')}")
        linhas.append(f"💰 Valor: {servico.get('preco', '-')}")

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