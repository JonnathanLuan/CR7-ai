"""
Pesquisa na internet da ORION.

Duas ferramentas:
  - buscar_na_internet: faz uma busca (estilo Google) e devolve
    títulos, links e resumos dos resultados.
  - ler_pagina_web: abre uma URL específica e extrai o texto
    principal da página, para leitura mais profunda.

Usa o DuckDuckGo (via `duckduckgo_search`) porque não exige
nenhuma chave de API — funciona direto após instalar a lib.
"""

import re

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

TAMANHO_MAXIMO_PAGINA = 4000  # caracteres, pra não estourar o contexto do LLM
TIMEOUT_SEGUNDOS = 10


def buscar_na_internet(consulta, max_resultados=5):
    """
    Busca `consulta` na internet e devolve uma lista de
    dicionários com 'titulo', 'link' e 'resumo'.
    """

    consulta = str(consulta).strip()

    if not consulta:
        return "Preciso de um termo de busca."

    try:
        with DDGS() as motor:
            resultados = list(motor.text(consulta, region="br-pt", max_results=max_resultados))
    except Exception as erro:  # noqa: BLE001
        return f"Não consegui pesquisar agora (erro: {erro})."

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
    Baixa uma página e devolve o texto principal (sem HTML,
    scripts, menus, etc.), truncado para não ficar gigante.
    """

    url = str(url).strip()

    if not url.startswith(("http://", "https://")):
        return "URL inválida. Preciso de um link completo (começando com http:// ou https://)."

    cabecalhos = {"User-Agent": "Mozilla/5.0 (compatible; ORION-Bot/1.0)"}

    try:
        resposta = requests.get(url, headers=cabecalhos, timeout=TIMEOUT_SEGUNDOS)
        resposta.raise_for_status()
    except requests.RequestException as erro:
        return f"Não consegui abrir essa página (erro: {erro})."

    sopa = BeautifulSoup(resposta.text, "html.parser")

    for indesejado in sopa(["script", "style", "nav", "footer", "header", "noscript"]):
        indesejado.decompose()

    texto = sopa.get_text(separator="\n")
    texto = re.sub(r"\n{2,}", "\n", texto)
    texto = re.sub(r"[ \t]{2,}", " ", texto)
    texto = texto.strip()

    if not texto:
        return "A página abriu, mas não encontrei texto legível nela."

    if len(texto) > TAMANHO_MAXIMO_PAGINA:
        texto = texto[:TAMANHO_MAXIMO_PAGINA] + "\n[...conteúdo truncado...]"

    return texto
