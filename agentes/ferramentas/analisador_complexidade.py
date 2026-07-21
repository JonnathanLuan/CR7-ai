def obter_sugestoes(quantidade_linhas, funcoes, funcoes_grandes):
    """
    Gera sugestões iniciais de melhoria.
    """

    sugestoes = []

    if quantidade_linhas > 100:
        sugestoes.append(
            "O código possui muitas linhas. Considere dividi-lo em módulos menores."
        )

    if not funcoes and quantidade_linhas > 20:
        sugestoes.append(
            "Considere organizar partes do código em funções."
        )

    if funcoes_grandes:
        nomes = ", ".join(funcoes_grandes)

        sugestoes.append(
            f"As funções {nomes} possuem muitas linhas e podem ser divididas."
        )

    if not sugestoes:
        sugestoes.append(
            "Não encontrei problemas estruturais evidentes nesta análise inicial."
        )

    return sugestoes