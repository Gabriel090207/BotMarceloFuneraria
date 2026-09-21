import re


def normalizar_telefone_brasileiro(numero):
    """Retorna DDI 55 + DDD + telefone, ou None para entrada inválida.

    Aceita strings com DDD de dois dígitos, opcionalmente entre parênteses.
    Permite espaços entre DDI, DDD e assinante, e hífen antes dos quatro
    últimos dígitos do assinante. Usa somente dígitos ASCII.
    O sinal + é permitido apenas no início de um número internacional.
    Não acrescenta nem remove o nono dígito e não verifica existência da linha.
    """
    if not isinstance(numero, str):
        return None

    texto = numero.strip(" ")
    formato = (
        r"(?:\+?55 *)?"                 # DDI opcional, com ou sem +.
        r"(?:[0-9]{2}|\([0-9]{2}\)) *"  # DDD simples ou entre parênteses.
        r"[0-9]{4,5}-?[0-9]{4}"         # Assinante, com hífen opcional.
    )
    if not re.fullmatch(formato, texto):
        return None

    digitos = re.sub(r"[ ()-]", "", texto.lstrip("+"))

    if len(digitos) in (12, 13):
        if not digitos.startswith("55"):
            return None
        nacional = digitos[2:]
    elif len(digitos) in (10, 11) and not texto.startswith("+"):
        nacional = digitos
    else:
        return None

    # DDD de dois dígitos sem zero e assinante de oito ou nove dígitos.
    if not re.fullmatch(r"[1-9]{2}[2-9][0-9]{7,8}", nacional):
        return None

    return "55" + nacional


def eh_numero_interno(numero):
    """Consulta numeros_internos/{telefone_normalizado}, sem gravar dados.

    Apenas ativo=True (booleano) habilita o cadastro. Entrada inválida,
    documento ausente ou inativo retorna False. Falhas do Firebase/Firestore
    são propagadas ao chamador, nunca convertidas em cadastro inexistente.
    """
    telefone = normalizar_telefone_brasileiro(numero)
    if telefone is None:
        return False

    from core.firebase import db

    documento = db.collection("numeros_internos").document(telefone).get()
    if not documento.exists:
        return False

    dados = documento.to_dict() or {}
    return dados.get("ativo") is True
