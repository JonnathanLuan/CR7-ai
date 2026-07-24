def avaliar_funcao(funcao):
    """
    Avalia a qualidade básica de uma função.
    """

    nota = 10
    observacoes = []

    # Docstring
    if not funcao["possui_docstring"]:
        nota -= 1
        observacoes.append(
            "Adicionar uma docstring para documentar a função."
        )

    # Tamanho
    if funcao["quantidade_linhas"] > 30:
        nota -= 2
        observacoes.append(
            "A função está grande e pode ser dividida."
        )

    elif funcao["quantidade_linhas"] > 20:
        nota -= 1
        observacoes.append(
            "A função pode ser simplificada."
        )

    # Parâmetros
    if len(funcao["parametros"]) > 5:
        nota -= 1
        observacoes.append(
            "Muitos parâmetros. Considere agrupar informações."
        )

    if nota < 0:
        nota = 0

    return {
        "nota": nota,
        "observacoes": observacoes,
    }