from fastapi import FastAPI, Request
from core.bot import responder

app = FastAPI()


@app.get("/")
def home():
    return {"status": "Bot online 🚀"}


@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    print("Recebido:", data)  # debug

    mensagem = data.get("text", {}).get("message")
    numero = data.get("phone")

    if not mensagem or not numero:
        return {"status": "erro"}

    resposta = responder(numero, mensagem)

    return {
        "reply": resposta
    }