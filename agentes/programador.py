from agentes.ferramentas.programador import analisar_codigo


def executar(intencao, dados=None):
    if intencao == "analisar_codigo":
        codigo = (dados or {}).get("codigo")
        return analisar_codigo(codigo)
    return "Sou o agente Programador, mas ainda não sei executar essa solicitação."
