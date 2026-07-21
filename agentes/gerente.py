# ==========================
# IMPORTAÇÕES
# ==========================

from agentes import assistente
from agentes import programador


# ==========================
# REGISTRO DE AGENTES
# ==========================

AGENTES = {
    "assistente": assistente.executar,
    "programador": programador.executar,
}


# ==========================
# ESCOLHA DO AGENTE
# ==========================

def escolher_agente(intencao, dados=None):

    mapa = {
        "saudacao": "assistente",
        "informar_nome": "assistente",
        "perguntar_nome": "assistente",
        "informar_idade": "assistente",
        "perguntar_idade": "assistente",
        "informar_cidade": "assistente",
        "perguntar_cidade": "assistente",
        "consultar_informacao": "assistente",
        "aprender_informacao": "assistente",
        "abrir_programa": "assistente",

        # Novos agentes
        "analisar_codigo": "programador",
    }

    return mapa.get(intencao, "assistente")



# ==========================
# EXECUÇÃO DO AGENTE
# ==========================

def executar_agente(intencao, dados=None):
    """
    Escolhe e executa o agente responsável pela intenção.
    """

    nome_agente = escolher_agente(intencao, dados)
    agente = AGENTES.get(nome_agente)

    if agente is None:
        return "Não encontrei um agente capaz de executar essa solicitação."

    return agente(intencao, dados)