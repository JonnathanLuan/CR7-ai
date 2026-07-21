from agentes.ferramentas.analisador_detalhes_funcoes import analisar_funcoes
from agentes.ferramentas.programador import analisar_codigo


def executar(intencao, dados=None):

    if intencao == "analisar_codigo":
        return analisar_codigo(None)

    return (
        "Sou o agente Programador, mas ainda não sei executar "
        "essa solicitação."
    )