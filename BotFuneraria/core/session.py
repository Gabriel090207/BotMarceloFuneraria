sessions = {}


def get_session(numero):

    if numero not in sessions:
        sessions[numero] = {
            "fluxo": None,
            "etapa": "inicio",
            "dados": {}
        }

    return sessions[numero]