import re
import unicodedata
from difflib import SequenceMatcher


def _normalizar(texto):
    texto = texto.lower().strip()

    texto = "".join(
        caractere
        for caractere in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caractere) != "Mn"
    )

    texto = re.sub(r"[^\w\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


COMANDOS = {
    "adicionar tarefa": [
        "adicionar tarefa",
        "adicione tarefa",
        "adicione a tarefa",
        "adiciona tarefa",
        "criar tarefa",
        "crie tarefa",
        "crie a tarefa",
        "nova tarefa",
    ],

    "concluir tarefa": [
        "concluir tarefa",
        "conclua tarefa",
        "conclua a tarefa",
        "finalizar tarefa",
        "marcar tarefa",
    ],

    "remover tarefa": [
        "remover tarefa",
        "remova tarefa",
        "remova a tarefa",
        "apagar tarefa",
        "excluir tarefa",
        "deletar tarefa",
    ],

    "listar tarefas": [
        "listar tarefas",
        "minhas tarefas",
        "quais sao minhas tarefas",
        "mostrar tarefas",
        "mostre minhas tarefas",
    ],
}


def corrigir_comando_rapido(frase):
    texto = _normalizar(frase)

    # Primeiro tenta reconhecimento exato.
    for comando_canonico, variacoes in COMANDOS.items():
        for variacao in variacoes:
            if texto.startswith(variacao):
                restante = texto[len(variacao):].strip()

                if restante:
                    return f"{comando_canonico} {restante}"

                return comando_canonico

    # Depois tolera pequenos erros do reconhecimento de voz.
    palavras = texto.split()

    for comando_canonico, variacoes in COMANDOS.items():
        for variacao in variacoes:
            quantidade = len(variacao.split())

            if len(palavras) < quantidade:
                continue

            inicio = " ".join(
                palavras[:quantidade]
            )

            similaridade = SequenceMatcher(
                None,
                inicio,
                variacao,
            ).ratio()

            if similaridade >= 0.72:
                restante = " ".join(
                    palavras[quantidade:]
                ).strip()

                if restante:
                    return f"{comando_canonico} {restante}"

                return comando_canonico

    return frase