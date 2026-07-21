def detectar_intencao(texto):
    # -------------------------
    # SAUDAÇÃO
    # -------------------------

    saudacoes = {
        "oi",
        "ola",
        "olá",
        "bom dia",
        "boa tarde",
        "boa noite",
        "e ai",
        "e aí",
        "opa",
    }

    if texto in saudacoes:
        return "saudacao"

    # -------------------------
    # ABRIR PROGRAMA
    # -------------------------

    if (
        texto.startswith("abra ")
        or texto.startswith("abrir ")
        or texto.startswith("abra o ")
        or texto.startswith("abra a ")
        or texto.startswith("abrir o ")
        or texto.startswith("abrir a ")
    ):
        return "abrir_programa"

    # -------------------------
    # PERGUNTAR NOME
    # -------------------------

    if (
        "qual meu nome" in texto
        or "qual e meu nome" in texto
        or "qual e o meu nome" in texto
        or "como eu me chamo" in texto
    ):
        return "perguntar_nome"

    # -------------------------
    # PERGUNTAR IDADE
    # -------------------------

    if (
        "qual minha idade" in texto
        or "quantos anos eu tenho" in texto
        or "quantos anos tenho" in texto
    ):
        return "perguntar_idade"

    # -------------------------
    # PERGUNTAR CIDADE
    # -------------------------

    if (
        "onde eu moro" in texto
        or "qual minha cidade" in texto
        or "qual e minha cidade" in texto
        or "qual e a minha cidade" in texto
        or "em que cidade eu moro" in texto
    ):
        return "perguntar_cidade"

    # -------------------------
    # CONSULTAR INFORMAÇÃO
    # -------------------------

    if (
        texto.startswith("qual meu ")
        or texto.startswith("qual minha ")
        or texto.startswith("qual e meu ")
        or texto.startswith("qual e minha ")
        or texto.startswith("qual e o meu ")
        or texto.startswith("qual e a minha ")
    ):
        return "consultar_informacao"

    # -------------------------
    # INFORMAR CIDADE
    # Deve vir antes de informar nome
    # -------------------------

    if (
        texto.startswith("moro em ")
        or texto.startswith("eu moro em ")
        or texto.startswith("sou de ")
        or texto.startswith("eu sou de ")
        or texto.startswith("minha cidade e ")
    ):
        return "informar_cidade"

    # -------------------------
    # INFORMAR IDADE
    # -------------------------

    if (
        ("tenho " in texto and "anos" in texto)
        or texto.startswith("minha idade e ")
    ):
        return "informar_idade"

    # -------------------------
    # INFORMAR NOME
    # -------------------------

    if (
        "me chamo " in texto
        or "eu me chamo " in texto
        or "meu nome e " in texto
        or "pode me chamar de " in texto
        or texto.startswith("sou ")
        or texto.startswith("eu sou ")
    ):
        return "informar_nome"

    # -------------------------
    # APRENDER INFORMAÇÃO
    # -------------------------

    if (
        texto.startswith("meu ")
        or texto.startswith("minha ")
    ) and " e " in texto:
        return "aprender_informacao"

    # -------------------------
    # ANALISAR CÓDIGO
    # -------------------------

    if (
        "analise meu codigo" in texto
        or "analise este codigo" in texto
        or "revise meu codigo" in texto
        or "revise este codigo" in texto
        or "explique este codigo" in texto
    ):
        return "analisar_codigo"

    return "desconhecida"