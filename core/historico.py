import json
import os
from datetime import datetime


CAMINHO_HISTORICO = "data/historico.json"


def carregar_historico():
    if not os.path.exists(CAMINHO_HISTORICO):
        return []

    try:
        with open(CAMINHO_HISTORICO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except (json.JSONDecodeError, OSError):
        return []


def salvar_historico(historico):
    os.makedirs("data", exist_ok=True)

    with open(CAMINHO_HISTORICO, "w", encoding="utf-8") as arquivo:
        json.dump(
            historico,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def registrar_conversa(pergunta, resposta):
    historico = carregar_historico()

    conversa = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "usuario": pergunta,
        "orion": resposta
    }

    historico.append(conversa)

    salvar_historico(historico)


def obter_ultima_fala_usuario():
    historico = carregar_historico()

    if not historico:
        return None

    ultima_conversa = historico[-1]

    return ultima_conversa.get("usuario")