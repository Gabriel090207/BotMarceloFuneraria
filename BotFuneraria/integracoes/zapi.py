import os
import requests
from dotenv import load_dotenv

load_dotenv()

ZAPI_BASE_URL = os.getenv("ZAPI_BASE_URL")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")


def enviar_texto(phone, mensagem):
    url = f"{ZAPI_BASE_URL}/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text-message"

    payload = {
        "phone": phone,
        "message": mensagem
    }

    print("📤 Enviando TEXTO:", payload)

    response = requests.post(url, json=payload)

    print("📥 Z-API STATUS:", response.status_code)
    print("📥 Z-API RESPOSTA:", response.text)

    return response.json()


def enviar_botoes(phone, mensagem, botoes):
    url = f"{ZAPI_BASE_URL}/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-button-list"

    payload = {
        "phone": phone,
        "message": mensagem,
        "buttonList": {
            "buttons": botoes
        }
    }

    print("📤 Enviando BOTÕES:", payload)

    response = requests.post(url, json=payload)

    print("📥 Z-API STATUS:", response.status_code)
    print("📥 Z-API RESPOSTA:", response.text)

    return response.json()