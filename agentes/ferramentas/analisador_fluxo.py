import ast


def explicar_funcao(funcao_ast):

    nome = funcao_ast.name

    if nome.startswith("obter"):
        objetivo = "Obtém informações."

    elif nome.startswith("carregar"):
        objetivo = "Carrega dados."

    elif nome.startswith("salvar"):
        objetivo = "Salva informações."

    elif nome.startswith("analisar"):
        objetivo = "Analisa dados."

    elif nome.startswith("executar"):
        objetivo = "Executa uma ação."

    elif nome.startswith("receber"):
        objetivo = "Recebe dados do usuário."

    else:
        objetivo = "Executa uma tarefa."

    return {
        "objetivo": objetivo,
    }