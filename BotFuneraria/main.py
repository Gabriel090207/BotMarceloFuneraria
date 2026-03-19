from dotenv import load_dotenv
import os

from core.bot import responder

# Carrega variáveis do .env
load_dotenv()

numero = "cliente_teste"

print("🤖 Bot iniciado...\n")

while True:

    msg = input("Cliente: ")

    resposta = responder(numero, msg)

    if resposta:
        print("Bot:", resposta)