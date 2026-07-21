import ast

from agentes.ferramentas.analisador_codigo import gerar_arvore


MENSAGEM_SOLICITAR_CODIGO = (
    "Cole o código que deseja analisar.\n"
    "Quando terminar, digite FIM em uma nova linha."
)


def analisar_codigo(codigo):
    if codigo is None or not str(codigo).strip():
        return MENSAGEM_SOLICITAR_CODIGO

    codigo = str(codigo)

    # Gera a árvore sintática
    arvore, erro = gerar_arvore(codigo)

    if erro:
        linha = erro.lineno or "desconhecida"
        mensagem = erro.msg or "erro de sintaxe"

        return (
            "Encontrei um erro de sintaxe.\n\n"
            f"Linha: {linha}\n"
            f"Problema: {mensagem}"
        )

    quantidade_linhas = len(codigo.splitlines())

    funcoes = [
        no.name
        for no in ast.walk(arvore)
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    classes = [
        no.name
        for no in ast.walk(arvore)
        if isinstance(no, ast.ClassDef)
    ]

    importacoes = [
        no
        for no in ast.walk(arvore)
        if isinstance(no, (ast.Import, ast.ImportFrom))
    ]

    sugestoes = []

    if quantidade_linhas > 100:
        sugestoes.append(
            "O código possui muitas linhas. Considere dividi-lo em módulos menores."
        )

    if not funcoes and quantidade_linhas > 20:
        sugestoes.append(
            "Considere organizar partes do código em funções."
        )

    funcoes_grandes = []

    for no in ast.walk(arvore):
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):
            linha_final = getattr(no, "end_lineno", no.lineno)
            tamanho = linha_final - no.lineno + 1

            if tamanho > 30:
                funcoes_grandes.append(no.name)

    if funcoes_grandes:
        nomes = ", ".join(funcoes_grandes)

        sugestoes.append(
            f"As funções {nomes} possuem muitas linhas e podem ser divididas."
        )

    if not sugestoes:
        sugestoes.append(
            "Não encontrei problemas estruturais evidentes nesta análise inicial."
        )

    nomes_funcoes = ", ".join(funcoes) if funcoes else "nenhuma"
    nomes_classes = ", ".join(classes) if classes else "nenhuma"

    texto_sugestoes = "\n".join(
        f"- {sugestao}"
        for sugestao in sugestoes
    )

    return (
        "Análise concluída.\n\n"
        f"Linhas de código: {quantidade_linhas}\n"
        f"Funções encontradas: {len(funcoes)} ({nomes_funcoes})\n"
        f"Classes encontradas: {len(classes)} ({nomes_classes})\n"
        f"Importações encontradas: {len(importacoes)}\n\n"
        "Sugestões:\n"
        f"{texto_sugestoes}"
    )