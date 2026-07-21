# ==========================
# IMPORTAÇÕES
# ==========================

from agentes.gerente import executar_agente


# ==========================
# EXECUTOR PRINCIPAL
# ==========================

def executar_intencao(intencao, dados=None):
    """
    Encaminha a intenção para o Gerente de Agentes.

    Esta função permanece no core para manter
    compatibilidade com o restante do projeto.
    """

    return executar_agente(intencao, dados)