from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

from core.bot import responder
from integracoes.zapi import enviar_texto, enviar_botoes

load_dotenv()

app = FastAPI()


# ---------------------------
# ROTA HOME
# ---------------------------
@app.get("/")
async def home():
    return {"status": "Bot online 🚀"}


# ---------------------------
# WEBHOOK Z-API
# ---------------------------
@app.post("/webhook")
async def webhook(request: Request):

    try:
        data = await request.json()

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
            return JSONResponse(content={"status": "ignorado"})

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

        if isinstance(resposta, dict) and resposta.get("tipo") == "texto":
            enviar_texto(numero, resposta["mensagem"])

        elif isinstance(resposta, dict) and resposta.get("tipo") == "botoes":

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

        return JSONResponse(content={"status": "ok"})

    except Exception as e:
        print("❌ ERRO:", str(e))
        return JSONResponse(content={"erro": str(e)})


# ---------------------------
# START SERVIDOR
# ---------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)