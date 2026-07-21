from core.historico import obter_ultima_fala_usuario
from core.ia import executar_intencao
from core.nlp.extrator import extrair_dados
from core.nlp.intencoes import detectar_intencao
from core.nlp.normalizador import normalizar


def interpretar(comando):
    texto_normalizado = normalizar(comando)

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