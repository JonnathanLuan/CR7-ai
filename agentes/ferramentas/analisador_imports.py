import ast


def obter_importacoes(arvore):
    """
    Retorna todas as importações do código.
    """

    return [
        no
        for no in ast.walk(arvore)
        if isinstance(no, (ast.Import, ast.ImportFrom))
    ]