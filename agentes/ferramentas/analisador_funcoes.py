import ast


def obter_funcoes(arvore):
    """
    Retorna todas as funções encontradas.
    """

    return [
        no.name
        for no in ast.walk(arvore)
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]


def obter_funcoes_grandes(arvore, limite=30):
    """
    Retorna funções maiores que o limite de linhas.
    """

    grandes = []

    for no in ast.walk(arvore):

        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):

            linha_final = getattr(no, "end_lineno", no.lineno)

            tamanho = linha_final - no.lineno + 1

            if tamanho > limite:
                grandes.append(no.name)

    return grandes