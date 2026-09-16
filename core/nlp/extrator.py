import re
from core.agenda import extrair_lembrete

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
    Extrai o nome do programa mesmo em frases naturais.

    Exemplos:
        Abra o Paint.
        Poderia abrir o Paint?
        CR7, poderia abrir o Paint para mim?
        Consegue abrir a calculadora?
    """

    frase_original = frase.strip()

    padroes = [
        r"(?:cr7[\s,]*)?poderia abrir\s+(?:o |a )?(.+)",
        r"(?:cr7[\s,]*)?pode abrir\s+(?:o |a )?(.+)",
        r"(?:cr7[\s,]*)?consegue abrir\s+(?:o |a )?(.+)",
        r"(?:cr7[\s,]*)?quero que abra\s+(?:o |a )?(.+)",
        r"(?:cr7[\s,]*)?abra\s+(?:o |a )?(.+)",
        r"(?:cr7[\s,]*)?abre\s+(?:o |a )?(.+)",
        r"(?:cr7[\s,]*)?abrir\s+(?:o |a )?(.+)",
    ]

    for padrao in padroes:
        resultado = re.search(padrao, frase_original, flags=re.IGNORECASE)

        if resultado:
            programa = resultado.group(1)

            # Remove expressões de cortesia no final
            programa = re.sub(
                r"\s+(por favor|pra mim|para mim)[\s.!?]*$",
                "",
                programa,
                flags=re.IGNORECASE,
            )

            programa = limpar_valor(programa)
            programa = programa.lower()

            if programa:
                return programa

    return None


def extrair_descricao_tarefa(frase):
    """
    Extrai a descrição de uma nova tarefa.

    Exemplos:
        Adicionar tarefa Comprar pão.
        Criar tarefa Estudar Python.
    """

    frase_original = frase.strip()
    frase_minuscula = frase_original.lower()

    padroes = [
        "adicionar tarefa ",
        "adicione a tarefa ",
        "adicione tarefa ",
        "criar tarefa ",
        "crie a tarefa ",
        "nova tarefa ",
    ]

    for padrao in padroes:
        if frase_minuscula.startswith(padrao):
            descricao = frase_original[len(padrao):]
            descricao = limpar_valor(descricao)

            if descricao:
                return descricao

    return None


def extrair_id_tarefa(frase):
    """
    Extrai o número (ID) de uma tarefa citada na frase.

    Exemplos:
        Concluir tarefa 3.
        Remover tarefa 1.
    """

    resultado = re.search(r"(\d+)", frase)

    if resultado:
        return int(resultado.group(1))

    return None

def extrair_consulta_pesquisa(frase):
    """
    Extrai o assunto que o usuário deseja pesquisar.
    """

    frase_original = frase.strip()
    frase_minuscula = frase_original.lower()

    padroes = [
        "pesquise na internet sobre ",
        "procure na internet sobre ",
        "busque na internet sobre ",
        "pesquise na internet ",
        "procure na internet ",
        "busque na internet ",
        "o que há de novo sobre ",
        "o que ha de novo sobre ",
        "pesquise sobre ",
        "procure sobre ",
        "busque sobre ",
        "pesquise ",
        "pesquisar ",
        "procure ",
        "buscar ",
        "busque ",
    ]

    for padrao in padroes:
        if frase_minuscula.startswith(padrao):
            consulta = frase_original[len(padrao):].strip()

            if consulta:
                return consulta

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

    elif intencao == "adicionar_lembrete":
        lembrete = extrair_lembrete(frase)

        if lembrete:
            dados["descricao"] = lembrete["descricao"]
            dados["lembrar_em"] = lembrete["lembrar_em"]

    elif intencao == "adicionar_tarefa":
        descricao = extrair_descricao_tarefa(frase)

        if descricao:
            dados["descricao"] = descricao

    elif intencao == "pesquisar_internet":
        consulta = extrair_consulta_pesquisa(frase)

        if consulta:
            dados["consulta"] = consulta

    elif intencao in ("concluir_tarefa", "remover_tarefa"):
        id_tarefa = extrair_id_tarefa(frase)

        if id_tarefa is not None:
            dados["id_tarefa"] = id_tarefa

    return dados