import ast


def analisar_funcoes(arvore):
    """
    Retorna informações detalhadas sobre cada função.
    """

    funcoes = []

    for no in ast.walk(arvore):

        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):

            linha_final = getattr(no, "end_lineno", no.lineno)

            parametros = [arg.arg for arg in no.args.args]

            funcoes.append({
                "nome": no.name,
                "linha_inicio": no.lineno,
                "linha_fim": linha_final,
                "quantidade_linhas": linha_final - no.lineno + 1,
                "parametros": parametros,
                "possui_docstring": ast.get_docstring(no) is not None,
            })

    return funcoes