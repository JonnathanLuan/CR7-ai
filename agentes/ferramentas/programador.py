import ast

from agentes.ferramentas.analisador_codigo import gerar_arvore
from agentes.ferramentas.analisador_funcoes import (
    obter_funcoes,
    obter_funcoes_grandes,
)
from agentes.ferramentas.analisador_classes import obter_classes
from agentes.ferramentas.analisador_imports import obter_importacoes
from agentes.ferramentas.analisador_complexidade import obter_sugestoes


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

    return (
        "Análise concluída.\n\n"
        f"Linhas de código: {quantidade_linhas}\n"
        f"Funções encontradas: {len(funcoes)} ({nomes_funcoes})\n"
        f"Classes encontradas: {len(classes)} ({nomes_classes})\n"
        f"Importações encontradas: {len(importacoes)}\n\n"
        "Sugestões:\n"
        f"{texto_sugestoes}"
    )