from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from core.bot import responder
from integracoes.zapi import enviar_texto, enviar_botoes, enviar_imagem

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

        # 🔹 texto normal
        if "text" in data and data["text"]:
            mensagem = data["text"].get("message")

        # 🔹 fallback
        if not mensagem:
            mensagem = data.get("message")

        # 🔹 clique em botão
        if "buttonsResponseMessage" in data:
            mensagem = data["buttonsResponseMessage"].get("buttonId")

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
        # ENVIO INTELIGENTE
        # ---------------------------

        print("📤 enviando para Z-API...")

        # ---------------------------
        # TEXTO
        # ---------------------------

        if resposta.get("tipo") == "texto":

            enviar_texto(numero, resposta["mensagem"])

        # ---------------------------
        # BOTÕES
        # ---------------------------

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

        # ---------------------------
        # IMAGEM + BOTÕES
        # ---------------------------

        elif resposta.get("tipo") == "imagem":

            # 🔥 envia imagem primeiro
            enviar_imagem(
                numero,
                resposta["imagem"],
                resposta.get("mensagem", "")
            )

            # 🔥 depois envia botões (se tiver)
            if "botoes" in resposta:

                botoes_formatados = [
                    {
                        "id": b["id"],
                        "label": b["label"]
                    }
                    for b in resposta["botoes"]
                ]

                enviar_botoes(
                    numero,
                    "Escolha uma opção:",
                    botoes_formatados
                )

        # ---------------------------
        # FALLBACK
        # ---------------------------

        else:
            enviar_texto(numero, str(resposta))

        return JSONResponse(content={"status": "ok"})

    except Exception as e:
        print("❌ ERRO:", str(e))
        return JSONResponse(content={"erro": str(e)})