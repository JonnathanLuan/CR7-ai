import re

from agentes.ferramentas.leitor_arquivo import ler_arquivo
from agentes.ferramentas.programador import (
    MENSAGEM_SOLICITAR_CODIGO,
    analisar_codigo,
)
from core.historico import obter_ultima_fala_usuario
from core.ia import executar_intencao
from core.nlp.extrator import extrair_dados
from core.nlp.intencoes import detectar_intencao
from core.nlp.normalizador import normalizar


def interpretar(comando):
    texto_normalizado = normalizar(comando)

    # -------------------------
    # ANALISAR ARQUIVO
    # -------------------------

    padrao_arquivo = re.search(
        r"(?:analise|analisar|verifique|verificar)\s+(?:o\s+)?arquivo\s+([a-zA-Z0-9_./\\-]+\.py)",
        comando,
        re.IGNORECASE,
    )

    if padrao_arquivo:
        caminho_arquivo = padrao_arquivo.group(1)

        codigo = ler_arquivo(caminho_arquivo)

        if codigo is None:
            return (
                f'Não encontrei o arquivo "{caminho_arquivo}".\n'
                "Verifique se o nome e o caminho estão corretos."
            )

        resultado = analisar_codigo(codigo)

        return (
            f'Arquivo analisado: "{caminho_arquivo}"\n\n'
            f"{resultado}"
        )

    # -------------------------
    # ANALISAR CÓDIGO COLADO
    # -------------------------

    if (
        "analise o codigo" in texto_normalizado
        or "analisar codigo" in texto_normalizado
        or "analise este codigo" in texto_normalizado
        or "verifique o codigo" in texto_normalizado
        or "verificar codigo" in texto_normalizado
    ):
        return MENSAGEM_SOLICITAR_CODIGO

    # -------------------------
    # CONSULTAR ÚLTIMA MENSAGEM
    # -------------------------

    if (
        "o que eu falei por ultimo" in texto_normalizado
        or "qual foi a ultima coisa que eu falei" in texto_normalizado
        or "qual foi minha ultima mensagem" in texto_normalizado
    ):
        ultima_fala = obter_ultima_fala_usuario()

        if ultima_fala:
            return f'Você falou por último: "{ultima_fala}".'

        return "Ainda não há nenhuma conversa registrada."

    # -------------------------
    # DETECTAR INTENÇÃO
    # -------------------------

    intencao = detectar_intencao(texto_normalizado)

    # -------------------------
    # EXTRAIR DADOS
    # -------------------------

    dados = extrair_dados(intencao, comando)

    # -------------------------
    # EXECUTAR INTENÇÃO
    # -------------------------

    return executar_intencao(intencao, dados)