import os
import mercadopago

def gerar_link_pagamento_sinal(valor_total, nome_cliente, referencia):

    access_token = os.getenv("MP_ACCESS_TOKEN")

    if not access_token:
        raise Exception("MP_ACCESS_TOKEN não encontrado no .env")

    sdk = mercadopago.SDK(access_token)

    valor_sinal = round(valor_total * 0.10, 2)

    preference = {
        "items": [
            {
                "title": f"Sinal funerária - {nome_cliente}",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": valor_sinal
            }
        ],
        "external_reference": referencia
    }

    response = sdk.preference().create(preference)

    return {
        "link_pagamento": response["response"]["init_point"],
        "valor_sinal": valor_sinal
    }