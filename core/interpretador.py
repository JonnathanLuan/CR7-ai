import re

from agentes.ferramentas.leitor_arquivo import ler_arquivo
from agentes.ferramentas.programador import (
    MENSAGEM_SOLICITAR_CODIGO,
    analisar_codigo,
)

from core import llm
from core.historico import obter_ultima_fala_usuario
from core.ia import executar_intencao
from core.logger import logger

from core.nlp.comandos_rapidos import corrigir_comando_rapido
from core.nlp.extrator import extrair_dados
from core.nlp.intencoes import detectar_intencao
from core.nlp.normalizador import normalizar

from core.router import router
from core.runtime import ContextoExecucao
from core.security import validar_mensagem


def interpretar(comando):
    # ==========================================
    # SEGURANÇA
    # ==========================================

    validacao = validar_mensagem(comando)

    if not validacao.sucesso:
        return validacao.mensagem

    # ==========================================
    # CORREÇÃO RÁPIDA DE COMANDOS DE VOZ
    # ==========================================

    comando_original = comando

    comando = corrigir_comando_rapido(comando)

    if comando != comando_original:
        logger.info(
            "Comando de voz ajustado: %s -> %s",
            comando_original,
            comando,
        )

    # ==========================================
    # CONTEXTO E NORMALIZAÇÃO
    # ==========================================

    contexto = ContextoExecucao(comando)

    texto_normalizado = normalizar(comando)

    rota = router.rotear(texto_normalizado)

    contexto.adicionar_evento(
        "rota",
        tipo=rota.tipo,
        confianca=rota.confianca,
    )

    logger.info(
        "Rota: tipo=%s confiança=%.2f motivo=%s",
        rota.tipo,
        rota.confianca,
        rota.motivo,
    )

    # ==========================================
    # IDENTIDADE DO ORION
    # ==========================================

    if texto_normalizado in (
        "quem e voce",
        "quem voce e",
        "quem e o orion",
        "o que e o orion",
    ):
        return (
            "Eu sou ORION, seu assistente pessoal. "
            "Fui criado por Jonnathan Luan para ajudar com informações, "
            "pesquisas, tarefas e automações."
        )

    # ==========================================
    # ANÁLISE DE ARQUIVOS PYTHON
    # ==========================================

    padrao_arquivo = re.search(
        r"(?:analise|analisar|verifique|verificar)\s+"
        r"(?:o\s+)?arquivo\s+"
        r"([a-zA-Z0-9_./\\-]+\.py)",
        comando,
        re.IGNORECASE,
    )

    if padrao_arquivo:
        caminho = padrao_arquivo.group(1)

        codigo = ler_arquivo(caminho)

        if codigo is None:
            return (
                f'Não encontrei o arquivo "{caminho}".\n'
                "Verifique se o nome e o caminho estão corretos."
            )

        return (
            f'Arquivo analisado: "{caminho}"\n\n'
            f"{analisar_codigo(codigo)}"
        )

    # ==========================================
    # ANÁLISE DE CÓDIGO
    # ==========================================

    if any(
        p in texto_normalizado
        for p in (
            "analise o codigo",
            "analisar codigo",
            "analise este codigo",
            "verifique o codigo",
            "verificar codigo",
        )
    ):
        return MENSAGEM_SOLICITAR_CODIGO

    # ==========================================
    # MEMÓRIA / HISTÓRICO
    # ==========================================

    if any(
        p in texto_normalizado
        for p in (
            "o que eu falei por ultimo",
            "qual foi a ultima coisa que eu falei",
            "qual foi minha ultima mensagem",
        )
    ):
        ultima = obter_ultima_fala_usuario()

        if ultima:
            return f'Você falou por último: "{ultima}".'

        return "Ainda não há nenhuma conversa registrada."

    # ==========================================
    # DETECÇÃO DE INTENÇÃO
    # ==========================================

    intencao = detectar_intencao(texto_normalizado)

    # ==========================================
    # IA
    # ==========================================

        # ==========================================
    # RESPOSTA RÁPIDA PARA COMANDO INCOMPLETO
    # ==========================================

    if intencao == "desconhecida":

        inicios_de_pergunta = (
            "o que",
            "como",
            "por que",
            "porque",
            "quem",
            "qual",
            "quais",
            "quando",
            "onde",
            "explique",
            "me explique",
            "fale sobre",
            "conte",
            "me conte",
            "pesquise",
            "procure",
            "busque",
        )

        palavras = texto_normalizado.split()

        if (
            len(palavras) <= 4
            and not texto_normalizado.startswith(
                inicios_de_pergunta
            )
        ):
            return (
                "Não entendi o comando. "
                "Tente novamente."
            )

        # ======================================
        # IA SOMENTE QUANDO REALMENTE NECESSÁRIA
        # ======================================

        if llm.usar_llm_disponivel():
            try:
                return llm.gerar_resposta(comando)

            except Exception as erro:
                logger.exception(
                    "Falha ao consultar o LLM: %s",
                    erro,
                )

                return (
                    "Tive um problema ao consultar minha IA. "
                    "Tente novamente."
                )

    # ==========================================
    # EXECUÇÃO DO COMANDO
    # ==========================================

    dados = extrair_dados(
        intencao,
        comando,
    )

    return executar_intencao(
        intencao,
        dados,
    )