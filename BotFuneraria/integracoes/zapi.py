import os
import requests
from dotenv import load_dotenv

load_dotenv()

ZAPI_BASE_URL = os.getenv("ZAPI_BASE_URL")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")


def enviar_texto(phone, mensagem):
    url = f"{ZAPI_BASE_URL}/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"

    payload = {
        "phone": phone,
        "message": mensagem
    }

    headers = {
        "Client-Token": ZAPI_CLIENT_TOKEN
    }

    print("📤 Enviando TEXTO:", payload)
    print("🌐 URL FINAL:", url)

    response = requests.post(url, json=payload, headers=headers)

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

    headers = {
        "Client-Token": ZAPI_CLIENT_TOKEN
    }

    print("📤 Enviando BOTÕES:", payload)
    print("🌐 URL FINAL:", url)

    response = requests.post(url, json=payload, headers=headers)

    print("📥 Z-API STATUS:", response.status_code)
    print("📥 Z-API RESPOSTA:", response.text)

    return response.json()

def enviar_imagem(phone, image_url, legenda=None):
    url = f"{ZAPI_BASE_URL}/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-image"

    payload = {
        "phone": phone,
        "image": image_url,
        "caption": legenda or ""
    }

    response = requests.post(url, json=payload)

    print("📤 Enviando IMAGEM:", payload)
    print("📥 Z-API:", response.text)

    return response.json()