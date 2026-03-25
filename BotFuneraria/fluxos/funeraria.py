from datetime import datetime
import unicodedata

from core.firebase import salvar_pedido
from core.urnas import listar_urnas
from core.pagamentos import formatar_reais


def normalizar(txt):
    txt = str(txt).lower().strip()
    txt = unicodedata.normalize("NFD", txt)
    return "".join(c for c in txt if unicodedata.category(c) != "Mn")


def menu(txt, op):
    return {
        "tipo": "botoes",
        "mensagem": txt,
        "botoes": [{"id": i, "label": l} for i, l in op]
    }


def voltar_menu_principal(session):
    session["fluxo"] = None
    session["etapa"] = "inicio"
    session["subfluxo"] = None

    return {
        "tipo": "botoes",
        "mensagem": "🔙 Voltamos ao menu principal",
        "botoes": [
            {"id": "1", "label": "Serviços funerários"},
            {"id": "2", "label": "Planos familiares"},
            {"id": "3", "label": "Planos empresariais"},
            {"id": "4", "label": "Floricultura"},
            {"id": "5", "label": "Atendente"},
        ]
    }


def fluxo_funeraria(session, mensagem):

    if "etapa" not in session:
        session["etapa"] = "inicio"

    if "dados" not in session:
        session["dados"] = {}

    if "subfluxo" not in session:
        session["subfluxo"] = None

    nome = session.get("nome", "Cliente")

    # -------------------
    # GLOBAL
    # -------------------

    if mensagem == "00":
        return voltar_menu_principal(session)

    # -------------------
    # MENU SERVIÇOS
    # -------------------

    if session["etapa"] == "inicio":

        session["etapa"] = "menu"

        return menu(
            f"⚰️ Serviços Funerários\n\n{nome}, como podemos ajudar?",
            [
                ("1", "Sepultamento"),
                ("2", "Cremação"),
                ("3", "Translado"),
                ("4", "Salas de velório"),
                ("5", "Atendente"),
            ]
        )

    # -------------------
    # ESCOLHA
    # -------------------

    if session["etapa"] == "menu":

        if mensagem == "1":
            session["subfluxo"] = "sepultamento"
            session["etapa"] = "endereco"
            return {"tipo": "texto", "mensagem": "📍 Endereço do local:"}

        if mensagem == "2":
            session["subfluxo"] = "cremacao"
            session["etapa"] = "endereco"
            return {"tipo": "texto", "mensagem": "📍 Endereço do local:"}

        if mensagem == "3":
            session["subfluxo"] = "translado"
            session["etapa"] = "origem"
            return {"tipo": "texto", "mensagem": "📍 Local de retirada:"}

        if mensagem == "4":
            session["subfluxo"] = "velorio"
            session["etapa"] = "tipo_sala"
            return menu("Escolha o tipo de sala:", [
                ("1", "Pequena"),
                ("2", "Média"),
                ("3", "Grande"),
            ])

        if mensagem == "5":
            from fluxos.atendente import fluxo_atendente
            return fluxo_atendente(session, mensagem)

    # =========================================
    # SEPULTAMENTO + CREMAÇÃO (MESMO FLUXO BASE)
    # =========================================

    if session["subfluxo"] in ["sepultamento", "cremacao"]:

        # ENDEREÇO
        if session["etapa"] == "endereco":
            session["dados"]["endereco"] = mensagem
            session["etapa"] = "tipo_urna"

            return menu("Escolha o tipo de urna:", [
                ("1", "Simples"),
                ("2", "Intermediária"),
                ("3", "Premium"),
                ("0", "Voltar"),
            ])

        # TIPO URNA
        if session["etapa"] == "tipo_urna":

            if mensagem == "0":
                session["etapa"] = "endereco"
                return {"tipo": "texto", "mensagem": "Informe o endereço novamente"}

            tipos = {
                "1": "simples",
                "2": "intermediaria",
                "3": "premium"
            }

            if mensagem not in tipos:
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            session["tipo_urna"] = tipos[mensagem]
            session["etapa"] = "lista_urnas"

            urnas = listar_urnas()

            filtradas = [
                u for u in urnas
                if normalizar(u.get("tipo")) == tipos[mensagem]
            ]

            session["urnas"] = filtradas

            botoes = []
            for i, u in enumerate(filtradas):
                botoes.append((str(i+1), f"{u['nome']} - {formatar_reais(float(u['preco']))}"))

            botoes.append(("0", "Voltar"))

            return menu("Escolha a urna:", botoes)

        # LISTA URNAS
        if session["etapa"] == "lista_urnas":

            if mensagem == "0":
                session["etapa"] = "tipo_urna"
                return fluxo_funeraria(session, "reload")

            try:
                urna = session["urnas"][int(mensagem)-1]
            except:
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            session["urna"] = urna
            session["etapa"] = "confirmar"

            img = urna.get("imagens", [])
            img = img[0] if img else ""

            return menu(
                f"{urna['nome']}\n{formatar_reais(float(urna['preco']))}\n📷 {img}",
                [
                    ("1", "Confirmar"),
                    ("2", "Trocar"),
                    ("0", "Voltar"),
                ]
            )

        # CONFIRMAR
        if session["etapa"] == "confirmar":

            if mensagem == "2" or mensagem == "0":
                session["etapa"] = "lista_urnas"
                return fluxo_funeraria(session, "reload")

            if mensagem != "1":
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            session["etapa"] = "final"

            total = float(session["urna"]["preco"])

            return menu(
                f"Resumo\n\nUrna: {session['urna']['nome']}\nValor: {formatar_reais(total)}",
                [
                    ("1", "Confirmar pedido"),
                    ("2", "Refazer"),
                ]
            )

        # FINAL
        if session["etapa"] == "final":

            if mensagem == "2":
                session["etapa"] = "inicio"
                return {"tipo": "texto", "mensagem": "Reiniciando..."}

            if mensagem == "1":

                salvar_pedido({
                    "tipo": session["subfluxo"],
                    "telefone": session.get("numero"),
                    "nome": session.get("nome"),
                    "urna": session["urna"],
                    "status": "novo",
                    "criado_em": datetime.now().isoformat()
                })

                session["encerrar_bot"] = True

                return {
                    "tipo": "texto",
                    "mensagem": "✅ Pedido registrado! Em breve entraremos em contato."
                }

    # =========================================
    # TRANSLADO
    # =========================================

    if session["subfluxo"] == "translado":

        if session["etapa"] == "origem":
            session["dados"]["origem"] = mensagem
            session["etapa"] = "destino"
            return {"tipo": "texto", "mensagem": "📍 Local de destino:"}

        if session["etapa"] == "destino":
            session["dados"]["destino"] = mensagem
            session["etapa"] = "confirmar"

            return menu(
                "Confirmar translado?",
                [
                    ("1", "Confirmar"),
                    ("2", "Refazer"),
                ]
            )

        if session["etapa"] == "confirmar":

            if mensagem == "1":

                salvar_pedido({
                    "tipo": "translado",
                    "telefone": session.get("numero"),
                    "dados": session["dados"],
                    "status": "novo",
                    "criado_em": datetime.now().isoformat()
                })

                session["encerrar_bot"] = True

                return {"tipo": "texto", "mensagem": "✅ Solicitação registrada"}

            if mensagem == "2":
                session["etapa"] = "inicio"
                return {"tipo": "texto", "mensagem": "Reiniciando..."}

    # =========================================
    # VELÓRIO
    # =========================================

    if session["subfluxo"] == "velorio":

        if session["etapa"] == "tipo_sala":

            salas = {
                "1": "Pequena",
                "2": "Média",
                "3": "Grande"
            }

            if mensagem not in salas:
                return {"tipo": "texto", "mensagem": "Escolha válida"}

            session["dados"]["sala"] = salas[mensagem]
            session["etapa"] = "data"

            return {"tipo": "texto", "mensagem": "📅 Informe a data desejada:"}

        if session["etapa"] == "data":
            session["dados"]["data"] = mensagem
            session["etapa"] = "confirmar"

            return menu(
                "Confirmar reserva?",
                [
                    ("1", "Confirmar"),
                    ("2", "Refazer"),
                ]
            )

        if session["etapa"] == "confirmar":

            if mensagem == "1":

                salvar_pedido({
                    "tipo": "velorio",
                    "telefone": session.get("numero"),
                    "dados": session["dados"],
                    "status": "novo",
                    "criado_em": datetime.now().isoformat()
                })

                session["encerrar_bot"] = True

                return {"tipo": "texto", "mensagem": "✅ Reserva registrada"}

            if mensagem == "2":
                session["etapa"] = "inicio"
                return {"tipo": "texto", "mensagem": "Reiniciando..."}

    return {"tipo": "texto", "mensagem": "Escolha válida."}