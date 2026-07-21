# ==========================
# IMPORTAÇÕES
# ==========================

from core.memoria import carregar_memoria, salvar_memoria
from core.personalidade import (
    resposta_aprendeu,
    resposta_nao_sei,
    resposta_saudacao,
)
from plugins.gerenciador import executar_plugin


# ==========================
# FUNÇÕES AUXILIARES
# ==========================

def aprender(chave, valor, memoria):
    """
    Salva uma informação genérica na memória.
    """

    if "informacoes" not in memoria:
        memoria["informacoes"] = {}

    memoria["informacoes"][chave] = valor
    salvar_memoria(memoria)


def obter_pronome_possessivo(chave):
    """
    Escolhe entre os pronomes possessivos "Seu" e "Sua".

    Esta é uma solução inicial baseada em uma lista
    de palavras masculinas conhecidas.
    """

    chaves_masculinas = {
        "time",
        "nome",
        "carro",
        "filme favorito",
        "livro favorito",
        "jogo favorito",
        "trabalho",
        "emprego",
        "aniversário",
        "aniversario",
        "endereço",
        "endereco",
        "telefone",
        "animal favorito",
        "esporte favorito",
    }

    if chave.lower() in chaves_masculinas:
        return "Seu"

    return "Sua"


# ==========================
# EXECUTOR DE NOME
# ==========================

def executar_nome(intencao, dados, memoria):
    """
    Executa as intenções relacionadas ao nome.
    """

    if intencao == "informar_nome":
        nome = dados.get("nome")

        if not nome:
            return "Não consegui entender seu nome."

        memoria["nome"] = nome
        salvar_memoria(memoria)

        return f"Prazer em conhecer você, {nome}."

    if intencao == "perguntar_nome":
        nome = memoria.get("nome")

        if nome:
            return f"Seu nome é {nome}."

        return "Ainda não sei seu nome."

    return None


# ==========================
# EXECUTOR DE IDADE
# ==========================

def executar_idade(intencao, dados, memoria):
    """
    Executa as intenções relacionadas à idade.
    """

    if intencao == "informar_idade":
        idade = dados.get("idade")

        if not idade:
            return "Não consegui entender sua idade."

        memoria["idade"] = idade
        salvar_memoria(memoria)

        return f"Entendido. Você tem {idade} anos."

    if intencao == "perguntar_idade":
        idade = memoria.get("idade")

        if idade:
            return f"Você tem {idade} anos."

        return "Ainda não sei sua idade."

    return None


# ==========================
# EXECUTOR DE CIDADE
# ==========================

def executar_cidade(intencao, dados, memoria):
    """
    Executa as intenções relacionadas à cidade.
    """

    if intencao == "informar_cidade":
        cidade = dados.get("cidade")

        if not cidade:
            return "Não consegui entender onde você mora."

        memoria["cidade"] = cidade
        salvar_memoria(memoria)

        return f"Agora sei que você mora em {cidade}."

    if intencao == "perguntar_cidade":
        cidade = memoria.get("cidade")

        if cidade:
            return f"Você mora em {cidade}."

        return "Ainda não sei onde você mora."

    return None


# ==========================
# EXECUTOR DE INFORMAÇÕES
# ==========================

def executar_informacao(intencao, dados, memoria):
    """
    Executa as intenções relacionadas às informações genéricas.
    """

    if intencao == "aprender_informacao":
        chave = dados.get("chave")
        valor = dados.get("valor")

        if not chave or not valor:
            return "Não consegui entender a informação."

        aprender(chave, valor, memoria)

        pronome = obter_pronome_possessivo(chave)

        return f"{resposta_aprendeu()} {pronome} {chave} é {valor}."

    if intencao == "consultar_informacao":
        chave = dados.get("chave")

        if not chave:
            return "Não consegui entender o que você deseja consultar."

        informacoes = memoria.get("informacoes", {})
        valor = informacoes.get(chave)

        pronome = obter_pronome_possessivo(chave)
        pronome_minusculo = pronome.lower()

        if valor:
            return f"{pronome} {chave} é {valor}."

        return f"Ainda não sei qual é {pronome_minusculo} {chave}."

    return None


# ==========================
# EXECUTOR DO SISTEMA
# ==========================

def executar_sistema(intencao, dados):
    """
    Executa comandos relacionados ao sistema operacional.
    """

    if intencao == "abrir_programa":
        programa = dados.get("programa")

        if not programa:
            return "Não consegui identificar qual programa você deseja abrir."

        programa_aberto = executar_plugin(
            "sistema",
            "abrir_programa",
            programa,
        )

        if programa_aberto:
            return f"Abrindo {programa}."

        return f"Não encontrei o programa {programa}."

    return None


# ==========================
# EXECUTOR DO ASSISTENTE
# ==========================

def executar(intencao, dados=None):
    """
    Executa as intenções direcionadas ao agente Assistente.
    """

    memoria = carregar_memoria()

    if dados is None:
        dados = {}

    # -------------------------
    # SAUDAÇÃO
    # -------------------------

    if intencao == "saudacao":
        return resposta_saudacao()

    # -------------------------
    # SISTEMA
    # -------------------------

    resposta = executar_sistema(intencao, dados)

    if resposta is not None:
        return resposta

    # -------------------------
    # NOME
    # -------------------------

    resposta = executar_nome(intencao, dados, memoria)

    if resposta is not None:
        return resposta

    # -------------------------
    # IDADE
    # -------------------------

    resposta = executar_idade(intencao, dados, memoria)

    if resposta is not None:
        return resposta

    # -------------------------
    # CIDADE
    # -------------------------

    resposta = executar_cidade(intencao, dados, memoria)

    if resposta is not None:
        return resposta

    # -------------------------
    # INFORMAÇÕES GENÉRICAS
    # -------------------------

    resposta = executar_informacao(intencao, dados, memoria)

    if resposta is not None:
        return resposta

    # -------------------------
    # INTENÇÃO DESCONHECIDA
    # -------------------------

    return resposta_nao_sei()