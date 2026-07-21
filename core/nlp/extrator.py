import re


def limpar_valor(valor):
    """
    Remove espaços e sinais de pontuação do início
    e do final de uma informação.
    """

    valor = valor.strip()
    valor = valor.strip(".,!?;:")
    valor = re.sub(r"\s+", " ", valor)

    return valor


def extrair_nome(frase):
    """
    Extrai o nome informado pelo usuário.
    """

    frase_original = frase.strip()
    frase_minuscula = frase_original.lower()

    padroes = [
        "pode me chamar de ",
        "meu nome é ",
        "meu nome e ",
        "eu me chamo ",
        "me chamo ",
        "eu sou ",
        "sou ",
    ]

    for padrao in padroes:
        posicao = frase_minuscula.find(padrao)

        if posicao != -1:
            inicio = posicao + len(padrao)
            nome = frase_original[inicio:]
            nome = limpar_valor(nome)

            if nome:
                return nome.title()

    return None


def extrair_idade(frase):
    """
    Extrai a idade informada pelo usuário.
    """

    frase_minuscula = frase.lower()

    padroes = [
        r"eu tenho\s+(\d{1,3})\s+anos",
        r"tenho\s+(\d{1,3})\s+anos",
        r"minha idade é\s+(\d{1,3})",
        r"minha idade e\s+(\d{1,3})",
        r"idade\s+(\d{1,3})",
    ]

    for padrao in padroes:
        resultado = re.search(padrao, frase_minuscula)

        if resultado:
            return resultado.group(1)

    return None


def extrair_cidade(frase):
    """
    Extrai a cidade informada pelo usuário.
    """

    frase_original = frase.strip()
    frase_minuscula = frase_original.lower()

    padroes = [
        "eu moro em ",
        "moro em ",
        "eu sou de ",
        "sou de ",
        "minha cidade é ",
        "minha cidade e ",
    ]

    for padrao in padroes:
        if frase_minuscula.startswith(padrao):
            cidade = frase_original[len(padrao):]
            cidade = limpar_valor(cidade)

            if cidade:
                return cidade.title()

    return None


def extrair_informacao_generica(frase):
    """
    Extrai uma informação genérica no formato chave e valor.

    Exemplos:
        Meu time é Sport.
        Minha profissão é professora.
        Minha comida favorita é pizza.
    """

    frase_original = frase.strip()
    frase_minuscula = frase_original.lower()

    padroes = [
        "meu ",
        "minha ",
    ]

    for padrao in padroes:
        if frase_minuscula.startswith(padrao):
            restante = frase_original[len(padrao):]

            partes = re.split(
                r"\s+é\s+|\s+e\s+",
                restante,
                maxsplit=1,
                flags=re.IGNORECASE,
            )

            if len(partes) == 2:
                chave = limpar_valor(partes[0]).lower()
                valor = limpar_valor(partes[1])

                if chave and valor:
                    return chave, valor

    return None, None


def extrair_chave_consulta(frase):
    """
    Extrai a chave de uma pergunta genérica.

    Exemplos:
        Qual meu time?
        Qual minha profissão?
        Qual é minha comida favorita?
    """

    frase_original = frase.strip()
    frase_minuscula = frase_original.lower()

    padroes = [
        "qual é o meu ",
        "qual e o meu ",
        "qual é a minha ",
        "qual e a minha ",
        "qual é meu ",
        "qual e meu ",
        "qual é minha ",
        "qual e minha ",
        "qual meu ",
        "qual minha ",
    ]

    for padrao in padroes:
        if frase_minuscula.startswith(padrao):
            chave = frase_original[len(padrao):]
            chave = limpar_valor(chave)
            chave = chave.lower()

            if chave:
                return chave

    return None


def extrair_programa(frase):
    """
    Extrai o nome do programa que o usuário deseja abrir.

    Exemplos:
        Abra o bloco de notas.
        Abra a calculadora.
        Abrir o Paint.
    """

    frase_original = frase.strip()
    frase_minuscula = frase_original.lower()

    padroes = [
        "abra o ",
        "abra a ",
        "abra ",
        "abrir o ",
        "abrir a ",
        "abrir ",
    ]

    for padrao in padroes:
        if frase_minuscula.startswith(padrao):
            programa = frase_original[len(padrao):]
            programa = limpar_valor(programa)
            programa = programa.lower()

            if programa:
                return programa

    return None


def extrair_dados(intencao, frase):
    """
    Escolhe o extrator adequado de acordo com a intenção.
    """

    dados = {}

    if intencao == "informar_nome":
        nome = extrair_nome(frase)

        if nome:
            dados["nome"] = nome

    elif intencao == "informar_idade":
        idade = extrair_idade(frase)

        if idade:
            dados["idade"] = idade

    elif intencao == "informar_cidade":
        cidade = extrair_cidade(frase)

        if cidade:
            dados["cidade"] = cidade

    elif intencao == "aprender_informacao":
        chave, valor = extrair_informacao_generica(frase)

        if chave and valor:
            dados["chave"] = chave
            dados["valor"] = valor

    elif intencao == "consultar_informacao":
        chave = extrair_chave_consulta(frase)

        if chave:
            dados["chave"] = chave

    elif intencao == "abrir_programa":
        programa = extrair_programa(frase)

        if programa:
            dados["programa"] = programa

    return dados