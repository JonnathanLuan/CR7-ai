import ast


def gerar_arvore(codigo):
    """
    Gera a árvore sintática (AST) do código.
    """

    try:
        return ast.parse(codigo), None

    except SyntaxError as erro:
        return None, erro