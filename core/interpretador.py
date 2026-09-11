import re

from agentes.ferramentas.leitor_arquivo import ler_arquivo
from agentes.ferramentas.programador import MENSAGEM_SOLICITAR_CODIGO, analisar_codigo
from core.historico import obter_ultima_fala_usuario
from core.ia import executar_intencao
from core.logger import logger
from core.nlp.extrator import extrair_dados
from core.nlp.intencoes import detectar_intencao
from core.nlp.normalizador import normalizar
from core.router import router
from core.runtime import ContextoExecucao
from core.security import validar_mensagem
from core import llm


def interpretar(comando):
    validacao = validar_mensagem(comando)
    if not validacao.sucesso:
        return validacao.mensagem

    contexto = ContextoExecucao(comando)
    texto_normalizado = normalizar(comando)
    rota = router.rotear(texto_normalizado)
    contexto.adicionar_evento("rota", tipo=rota.tipo, confianca=rota.confianca)
    logger.info("Rota: tipo=%s confiança=%.2f motivo=%s", rota.tipo, rota.confianca, rota.motivo)

    padrao_arquivo = re.search(r"(?:analise|analisar|verifique|verificar)\s+(?:o\s+)?arquivo\s+([a-zA-Z0-9_./\\-]+\.py)", comando, re.IGNORECASE)
    if padrao_arquivo:
        caminho = padrao_arquivo.group(1)
        codigo = ler_arquivo(caminho)
        if codigo is None:
            return f'Não encontrei o arquivo "{caminho}".\nVerifique se o nome e o caminho estão corretos.'
        return f'Arquivo analisado: "{caminho}"\n\n{analisar_codigo(codigo)}'

    if any(p in texto_normalizado for p in ("analise o codigo", "analisar codigo", "analise este codigo", "verifique o codigo", "verificar codigo")):
        return MENSAGEM_SOLICITAR_CODIGO

    if any(p in texto_normalizado for p in ("o que eu falei por ultimo", "qual foi a ultima coisa que eu falei", "qual foi minha ultima mensagem")):
        ultima = obter_ultima_fala_usuario()
        return f'Você falou por último: "{ultima}".' if ultima else "Ainda não há nenhuma conversa registrada."

    intencao = detectar_intencao(texto_normalizado)
    if intencao == "desconhecida" and llm.usar_llm_disponivel():
        try:
            return llm.gerar_resposta(comando)
        except Exception as erro:  # noqa: BLE001
            logger.exception("Falha ao consultar o LLM: %s", erro)
            return "Tive um problema ao consultar minha IA. Verifique o provedor configurado e tente novamente."

    dados = extrair_dados(intencao, comando)
    return executar_intencao(intencao, dados)
