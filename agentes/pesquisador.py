from agentes.ferramentas.pesquisa import buscar_na_internet


def _encurtar(texto, limite=280):
    texto = " ".join(str(texto).split())

    if len(texto) <= limite:
        return texto

    return texto[:limite].rsplit(" ", 1)[0] + "..."


def executar(intencao, dados=None):
    """
    Agente Pesquisador do ORION.
    Faz pesquisas rápidas na internet.
    """

    dados = dados or {}

    if intencao != "pesquisar_internet":
        return "Não reconheci essa solicitação de pesquisa."

    consulta = dados.get("consulta", "").strip()

    if not consulta:
        return "O que você gostaria que eu pesquisasse?"

    resultados = buscar_na_internet(
        consulta,
        max_resultados=3,
    )

    if isinstance(resultados, str):
        return resultados

    if not resultados:
        return "Não encontrei resultados para essa pesquisa."

    principal = resultados[0]

    titulo = principal.get(
        "titulo",
        "",
    ).strip()

    resumo = principal.get(
        "resumo",
        "",
    ).strip()

    resumo = _encurtar(
        resumo,
        280,
    )

    if titulo and resumo:
        return (
            f"Encontrei. {titulo}. "
            f"{resumo}"
        )

    if resumo:
        return f"Encontrei. {resumo}"

    if titulo:
        return f"Encontrei: {titulo}."

    return "Encontrei resultados, mas não consegui resumir."