from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from core.bot import responder
from integracoes.zapi import enviar_resposta

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
        # CAPTURA DADOS
        # ---------------------------

        numero = data.get("phone")
        mensagem = None

        # 🔹 clique em botão (PRIORIDADE)
        if "buttonsResponseMessage" in data:
            mensagem = data["buttonsResponseMessage"].get("buttonId")

        # 🔹 texto normal
        elif "text" in data and data["text"]:
            mensagem = data["text"].get("message")

        # 🔹 fallback
        elif "message" in data:
            mensagem = data.get("message")

        # ---------------------------
        # VALIDAÇÃO
        # ---------------------------

        if not numero or not mensagem:
            print("⚠️ Ignorado: sem número ou mensagem")
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
        # ENVIO INTELIGENTE (CORRIGIDO)
        # ---------------------------

        print("📤 enviando para Z-API...")

        enviar_resposta(resposta, numero)

        return JSONResponse(content={"status": "ok"})

    except Exception as e:
        print("❌ ERRO:", str(e))
        return JSONResponse(content={"erro": str(e)})