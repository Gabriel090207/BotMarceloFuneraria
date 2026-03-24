from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

from core.bot import responder
from integracoesx.zapi import enviar_texto, enviar_botoes

load_dotenv()

app = FastAPI()


@app.get("/")
def home():
    return {"status": "Bot online 🚀"}


@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    try:
        print("📩 JSON recebido:", data)

        # ---------------------------
        # CAPTURA DADOS DA Z-API
        # ---------------------------

        numero = data.get("phone")

        mensagem = None

        if "text" in data and data["text"]:
            mensagem = data["text"].get("message")

        if not mensagem:
            mensagem = data.get("message")

        # ---------------------------
        # VALIDAÇÃO
        # ---------------------------

        if not numero or not mensagem:
            return jsonify({"status": "ignorado"})

        print(f"📲 {numero}: {mensagem}")

        # ---------------------------
        # PROCESSA BOT
        # ---------------------------

        resposta = responder(numero, mensagem)

        if not resposta:
            return JSONResponse(content={"status": "ok"})

        # ---------------------------
        # ENVIO INTELIGENTE
        # ---------------------------

        if resposta.get("tipo") == "texto":
            enviar_texto(numero, resposta["mensagem"])

        elif resposta.get("tipo") == "botoes":

            # 🔹 converte para formato da Z-API
            botoes_formatados = [
                {
                    "id": b["id"],
                    "label": b["label"]
                }
                for b in resposta["botoes"]
            ]

            enviar_botoes(
                numero,
                resposta["mensagem"],
                botoes_formatados
            )

        else:
            # fallback (caso venha string ainda de algum fluxo)
            enviar_texto(numero, str(resposta))

        return jsonify({"status": "ok"})

    except Exception as e:
        print("❌ ERRO:", str(e))
        return jsonify({"erro": str(e)})


# Rodar com:
# uvicorn main:app --reload --host 0.0.0.0 --port 10000