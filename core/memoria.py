import json
import os

ARQUIVO = "data/memoria.json"


def carregar_memoria():
    if not os.path.exists(ARQUIVO):
        return {}

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def salvar_memoria(memoria):
    os.makedirs(os.path.dirname(ARQUIVO), exist_ok=True)

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(memoria, arquivo, indent=4, ensure_ascii=False) 