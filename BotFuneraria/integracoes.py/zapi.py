import os
import requests
from dotenv import load_dotenv

load_dotenv()

ZAPI_BASE_URL = os.getenv("ZAPI_BASE_URL")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")


def enviar_texto(phone, mensagem):
    url = f"{ZAPI_BASE_URL}/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"

    payload = {
        "phone": phone,
        "message": mensagem
    }

    response = requests.post(url, json=payload)

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

    response = requests.post(url, json=payload)

    return response.json()