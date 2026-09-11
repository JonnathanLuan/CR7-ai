"""Ponte de compatibilidade entre o Core e os agentes."""

from agentes.gerente import executar_agente


def executar_intencao(intencao, dados=None):
    return executar_agente(intencao, dados)
