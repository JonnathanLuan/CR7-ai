"""Orquestrador de agentes com compatibilidade com a API anterior."""

from agentes import assistente, programador

AGENTES = {
    "assistente": assistente.executar,
    "programador": programador.executar,
}

MAPA_AGENTES = {
    "saudacao": "assistente", "informar_nome": "assistente", "perguntar_nome": "assistente",
    "informar_idade": "assistente", "perguntar_idade": "assistente", "informar_cidade": "assistente",
    "perguntar_cidade": "assistente", "consultar_informacao": "assistente", "aprender_informacao": "assistente",
    "abrir_programa": "assistente", "listar_tarefas": "assistente", "adicionar_tarefa": "assistente",
    "concluir_tarefa": "assistente", "remover_tarefa": "assistente", "analisar_codigo": "programador",
    "adicionar_lembrete": "assistente",

}


def escolher_agente(intencao, dados=None):
    return MAPA_AGENTES.get(intencao, "assistente")


def executar_agente(intencao, dados=None):
    agente = AGENTES.get(escolher_agente(intencao, dados))
    if agente is None:
        return "Não encontrei um agente capaz de executar essa solicitação."
    return agente(intencao, dados)
