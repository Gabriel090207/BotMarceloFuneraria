from core.bot import responder

numero = "cliente_teste"

while True:

    msg = input("Cliente: ")

    resposta = responder(numero, msg)

    print("Bot:", resposta)