import ast

from agentes.ferramentas.analisador_codigo import gerar_arvore
from agentes.ferramentas.analisador_funcoes import (
    obter_funcoes,
    obter_funcoes_grandes,
)
from agentes.ferramentas.analisador_classes import obter_classes
from agentes.ferramentas.analisador_imports import obter_importacoes
from agentes.ferramentas.analisador_complexidade import obter_sugestoes
from agentes.ferramentas.analisador_detalhes_funcoes import analisar_funcoes
from agentes.ferramentas.analisador_qualidade import avaliar_funcao
from agentes.ferramentas.analisador_fluxo import explicar_funcao

MENSAGEM_SOLICITAR_CODIGO = (
    "Cole o código que deseja analisar.\n"
    "Quando terminar, digite FIM em uma nova linha."
)


def analisar_codigo(codigo):

    if codigo is None or not str(codigo).strip():
        return MENSAGEM_SOLICITAR_CODIGO

    codigo = str(codigo)

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

    funcoes = obter_funcoes(arvore)
    detalhes_funcoes = analisar_funcoes(arvore)
    classes = obter_classes(arvore)
    importacoes = obter_importacoes(arvore)
    funcoes_grandes = obter_funcoes_grandes(arvore)

    sugestoes = obter_sugestoes(
        quantidade_linhas,
        funcoes,
        funcoes_grandes,
    )

    nomes_funcoes = ", ".join(funcoes) if funcoes else "nenhuma"
    nomes_classes = ", ".join(classes) if classes else "nenhuma"

    texto_sugestoes = "\n".join(
        f"- {item}"
        for item in sugestoes
    )

    relatorios_funcoes = []

    for funcao in detalhes_funcoes:
        
        avaliacao = avaliar_funcao(funcao)
        funcao_ast = next(
    (
        node
        for node in ast.walk(arvore)
        if isinstance(node, ast.FunctionDef)
        and node.name == funcao["nome"]
    ),
    None,
)

        explicacao = explicar_funcao(funcao_ast)
        parametros = ", ".join(funcao["parametros"])

        if not parametros:
            parametros = "nenhum"

        possui_docstring = (
            "Sim"
            if funcao["possui_docstring"]
            else "Não"
        )

        observacoes = avaliacao["observacoes"]

        if observacoes:
            texto_observacoes = "\n".join(
                f"- {observacao}"
                for observacao in observacoes
            )
        else:
            texto_observacoes = (
                "- Nenhuma melhoria básica identificada."
            )

        relatorios_funcoes.append(
            f"Função: {funcao['nome']}\n"
            f"Objetivo: {explicacao['objetivo']}\n"
            f"Linhas: {funcao['quantidade_linhas']}\n"
            f"Parâmetros: {parametros}\n"
            f"Docstring: {possui_docstring}\n"
            f"Nota de qualidade: {avaliacao['nota']}/10\n"
            f"Observações:\n"
            f"{texto_observacoes}"
        )

    if relatorios_funcoes:
        texto_detalhes_funcoes = "\n\n".join(relatorios_funcoes)
    else:
        texto_detalhes_funcoes = "Nenhuma função encontrada."

    return (
        "Análise concluída.\n\n"
        f"Linhas de código: {quantidade_linhas}\n"
        f"Funções encontradas: {len(funcoes)} ({nomes_funcoes})\n"
        f"Classes encontradas: {len(classes)} ({nomes_classes})\n"
        f"Importações encontradas: {len(importacoes)}\n\n"
        "Sugestões:\n"
        f"{texto_sugestoes}\n\n"
        "Detalhes das funções:\n"
        f"{texto_detalhes_funcoes}"
    )