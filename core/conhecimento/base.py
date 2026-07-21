from core.memoria import carregar_memoria, salvar_memoria


def salvar(categoria, atributo, valor):
    """
    Salva qualquer conhecimento aprendido pela ORION.
    """

    memoria = carregar_memoria()

    if "conhecimento" not in memoria:
        memoria["conhecimento"] = {}

    if categoria not in memoria["conhecimento"]:
        memoria["conhecimento"][categoria] = {}

    memoria["conhecimento"][categoria][atributo] = valor

    salvar_memoria(memoria)


def consultar(categoria, atributo):
    """
    Consulta um conhecimento armazenado.
    """

    memoria = carregar_memoria()

    return (
        memoria
        .get("conhecimento", {})
        .get(categoria, {})
        .get(atributo)
    )