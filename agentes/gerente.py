"""Gerente de agentes do ORION."""

from agentes import (
    assistente,
    pesquisador,
    programador,
)


AGENTES = {
    "assistente": assistente.executar,
    "programador": programador.executar,
    "pesquisador": pesquisador.executar,
}


MAPA_AGENTES = {
    # Assistente
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
    "listar_tarefas": "assistente",
    "adicionar_tarefa": "assistente",
    "concluir_tarefa": "assistente",
    "remover_tarefa": "assistente",
    "adicionar_lembrete": "assistente",

    # Programador
    "analisar_codigo": "programador",

    # Pesquisador
    "pesquisar_internet": "pesquisador",
}


def escolher_agente(intencao, dados=None):
    return MAPA_AGENTES.get(
        intencao,
        "assistente",
    )


def executar_agente(intencao, dados=None):
    nome_agente = escolher_agente(
        intencao,
        dados,
    )

    agente = AGENTES.get(nome_agente)

    if agente is None:
        return (
            "Não encontrei um agente capaz "
            "de executar essa solicitação."
        )

    return agente(
        intencao,
        dados,
    )