import ast


def obter_classes(arvore):
    """
    Retorna todas as classes encontradas.
    """

    return [
        no.name
        for no in ast.walk(arvore)
        if isinstance(no, ast.ClassDef)
    ]