def criar_menu(titulo, opcoes):

    texto = f"\n{titulo}\n\n"

    for numero, nome in opcoes:
        texto += f"{numero} - {nome}\n"

    return texto