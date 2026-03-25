from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from core.bot import responder
from integracoes.zapi import enviar_texto, enviar_botoes

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

        numero = data.get("phone")

        mensagem = None

        # ---------------------------
        # CAPTURA MENSAGEM (🔥 CORRETO)
        # ---------------------------

        # texto normal
        if "text" in data and data["text"]:
            mensagem = data["text"].get("message")

        # botão clicado (🔥 ESSENCIAL)
        elif "buttonsResponseMessage" in data:
            mensagem = data["buttonsResponseMessage"].get("buttonId")

        # fallback
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

        print("👉 resposta do bot:", resposta)

        if not resposta:
            return JSONResponse(content={"status": "ok"})

        # ---------------------------
        # ENVIO PARA Z-API
        # ---------------------------

        print("📤 enviando para Z-API...")

        if isinstance(resposta, dict):

            if resposta.get("tipo") == "texto":
                enviar_texto(numero, resposta["mensagem"])

            elif resposta.get("tipo") == "botoes":

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
            enviar_texto(numero, str(resposta))

        return JSONResponse(content={"status": "ok"})

    except Exception as e:
        print("❌ ERRO:", str(e))
        return JSONResponse(content={"erro": str(e)})