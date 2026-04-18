import os
import requests
from dotenv import load_dotenv

load_dotenv()

ZAPI_BASE_URL = os.getenv("ZAPI_BASE_URL")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")


# ==================================================
# TEXTO
# ==================================================

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

    print("📥 STATUS:", response.status_code)
    print("📥 RESPOSTA:", response.text)

    return response.json()


# ==================================================
# BOTÕES
# ==================================================

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

    print("📥 STATUS:", response.status_code)
    print("📥 RESPOSTA:", response.text)

    return response.json()


# ==================================================
# IMAGEM
# ==================================================

def enviar_imagem(phone, url_imagem):
    url = f"{ZAPI_BASE_URL}/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-image"

    payload = {
        "phone": phone,
        "image": url_imagem
    }

    headers = {
        "Client-Token": ZAPI_CLIENT_TOKEN
    }

    print("📤 Enviando IMAGEM:", payload)
    print("🌐 URL FINAL:", url)

    response = requests.post(url, json=payload, headers=headers)

    print("📥 STATUS:", response.status_code)
    print("📥 RESPOSTA:", response.text)

    return response.json()


# ==================================================
# VIDEO
# ==================================================

def enviar_video(phone, url_video):
    url = f"{ZAPI_BASE_URL}/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-video"

    payload = {
        "phone": phone,
        "video": url_video
    }

    headers = {
        "Client-Token": ZAPI_CLIENT_TOKEN
    }

    print("📤 Enviando VIDEO:", payload)
    print("🌐 URL FINAL:", url)

    response = requests.post(url, json=payload, headers=headers)

    print("📥 STATUS:", response.status_code)
    print("📥 RESPOSTA:", response.text)

    return response.json()


# ==================================================
# DISPATCHER
# ==================================================

def enviar_mensagem(msg, numero):

    print("📤 Enviando:", msg)

    if not isinstance(msg, dict):
        print("❌ Mensagem inválida:", msg)
        return

    tipo = msg.get("tipo")

    if tipo == "texto":
        return enviar_texto(numero, msg.get("mensagem"))

    elif tipo == "botoes":
        return enviar_botoes(
            numero,
            msg.get("mensagem"),
            msg.get("botoes")
        )

    elif tipo == "imagem":
        return enviar_imagem(numero, msg.get("url"))

    elif tipo == "video":
        return enviar_video(numero, msg.get("url"))

    else:
        print("❌ Tipo desconhecido:", tipo)


# ==================================================
# RESPOSTA LISTA OU ÚNICA
# ==================================================

def enviar_resposta(resposta, numero):

    if isinstance(resposta, list):
        for item in resposta:
            enviar_mensagem(item, numero)
    else:
        enviar_mensagem(resposta, numero)