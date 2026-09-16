"""
Ferramentas de pesquisa na internet do ORION.
"""

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS


TIMEOUT_SEGUNDOS = 10
TAMANHO_MAXIMO_PAGINA = 4000


def buscar_na_internet(consulta, max_resultados=5):
    """
    Pesquisa na internet e retorna uma lista
    com título, link e resumo.
    """

    consulta = str(consulta).strip()

    if not consulta:
        return "Preciso de um termo de busca."

    try:
        with DDGS() as motor:
            resultados = motor.text(
                consulta,
                region="br-pt",
                max_results=max_resultados,
                backend="auto",
            )

    except Exception as erro:
        return (
            "Não consegui pesquisar agora. "
            f"Erro: {erro}"
        )

    if not resultados:
        return "Não encontrei nenhum resultado para essa busca."

    formatados = []

    for resultado in resultados:
        formatados.append(
            {
                "titulo": resultado.get("title", ""),
                "link": resultado.get("href", ""),
                "resumo": resultado.get("body", ""),
            }
        )

    return formatados


def ler_pagina_web(url):
    """
    Abre uma página da internet e extrai texto legível.
    """

    url = str(url).strip()

    if not url.startswith(("http://", "https://")):
        return "URL inválida."

    cabecalhos = {
        "User-Agent": "Mozilla/5.0 ORION/1.0"
    }

    try:
        resposta = requests.get(
            url,
            headers=cabecalhos,
            timeout=TIMEOUT_SEGUNDOS,
        )

        resposta.raise_for_status()

    except requests.RequestException as erro:
        return (
            "Não consegui abrir essa página. "
            f"Erro: {erro}"
        )

    sopa = BeautifulSoup(
        resposta.text,
        "html.parser",
    )

    for elemento in sopa(
        [
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript",
        ]
    ):
        elemento.decompose()

    texto = " ".join(
        sopa.stripped_strings
    )

    if not texto:
        return "Não encontrei texto legível nessa página."

    if len(texto) > TAMANHO_MAXIMO_PAGINA:
        texto = (
            texto[:TAMANHO_MAXIMO_PAGINA]
            + "..."
        )

    return texto