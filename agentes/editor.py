"""
Agente Editor do ORION.

Possui dois modos:

RÁPIDO:
usa regras locais e responde imediatamente.

INTELIGENTE:
usa IA para decidir melhor onde o corte
deve começar e terminar.
"""

import json
import re

from core import llm


MARGEM_ANTES = 3.0
MARGEM_DEPOIS = 4.0


def preparar_corte(destaque):
    """
    Modo rápido.
    Não usa IA.
    """

    if not isinstance(destaque, dict):
        return None

    inicio = destaque.get("inicio")
    fim = destaque.get("fim")

    if inicio is None or fim is None:
        return {
            "trecho": destaque.get("trecho", ""),
            "prioridade": destaque.get(
                "prioridade",
                "media",
            ),
            "inicio": None,
            "fim": None,
            "duracao": None,
            "status": "sem_tempo",
            "modo": "rapido",
        }

    inicio_corte = max(
        0.0,
        float(inicio) - MARGEM_ANTES,
    )

    fim_corte = (
        float(fim) + MARGEM_DEPOIS
    )

    duracao = fim_corte - inicio_corte

    return {
        "trecho": destaque.get("trecho", ""),
        "prioridade": destaque.get(
            "prioridade",
            "media",
        ),
        "inicio": round(inicio_corte, 2),
        "fim": round(fim_corte, 2),
        "duracao": round(duracao, 2),
        "status": "pronto_para_corte",
        "modo": "rapido",
    }


def preparar_cortes(destaques):
    """
    Prepara vários cortes rapidamente.
    """

    cortes = []

    for destaque in destaques:
        corte = preparar_corte(destaque)

        if corte:
            cortes.append(corte)

    cortes.sort(
        key=lambda item: (
            item["prioridade"] != "alta",
            item["inicio"]
            if item["inicio"] is not None
            else float("inf"),
        )
    )

    return cortes


def _extrair_json(resposta):
    """
    Extrai um JSON da resposta da IA.
    """

    if not resposta:
        return None

    texto = str(resposta).strip()

    texto = re.sub(
        r"```json",
        "",
        texto,
        flags=re.IGNORECASE,
    )

    texto = texto.replace("```", "")

    inicio = texto.find("{")
    fim = texto.rfind("}")

    if inicio == -1 or fim == -1:
        return None

    try:
        return json.loads(
            texto[inicio:fim + 1]
        )

    except Exception:
        return None


def preparar_corte_inteligente(
    destaque,
    contexto="",
):
    """
    Usa IA para decidir os melhores
    pontos de início e fim do corte.
    """

    corte_rapido = preparar_corte(destaque)

    if corte_rapido is None:
        return None

    if (
        destaque.get("inicio") is None
        or destaque.get("fim") is None
    ):
        return corte_rapido

    if not llm.usar_llm_disponivel():
        return corte_rapido

    inicio_evento = float(
        destaque["inicio"]
    )

    fim_evento = float(
        destaque["fim"]
    )

    trecho = destaque.get(
        "trecho",
        "",
    )

    prompt = f"""
Você é o Editor Inteligente do ORION.

Sua função é escolher o melhor trecho para
um vídeo curto de redes sociais.

MOMENTO DETECTADO:
{trecho}

INÍCIO DO MOMENTO:
{inicio_evento} segundos

FIM DO MOMENTO:
{fim_evento} segundos

CONTEXTO:
{contexto}

Escolha um ponto de início que preserve o contexto
e um ponto de fim que preserve a conclusão ou reação.

REGRAS:
- Não invente acontecimentos.
- O corte deve ter no máximo 90 segundos.
- Não comece antes de 30 segundos antes do evento.
- Não termine mais de 45 segundos depois do evento.
- Priorize um vídeo dinâmico.
- Não escreva explicações fora do JSON.

Responda SOMENTE:

{{
    "inicio": 0.0,
    "fim": 0.0,
    "motivo": "motivo curto da decisão",
    "formato": "vertical"
}}
"""

    try:
        resposta = llm.gerar_resposta(
            prompt
        )

        decisao = _extrair_json(
            resposta
        )

        if not decisao:
            return corte_rapido

        inicio = float(
            decisao.get(
                "inicio",
                corte_rapido["inicio"],
            )
        )

        fim = float(
            decisao.get(
                "fim",
                corte_rapido["fim"],
            )
        )

        # Limites para evitar cortes absurdos.

        inicio_minimo = max(
            0.0,
            inicio_evento - 30.0,
        )

        fim_maximo = (
            fim_evento + 45.0
        )

        inicio = max(
            inicio_minimo,
            inicio,
        )

        fim = min(
            fim_maximo,
            fim,
        )

        if fim <= inicio:
            return corte_rapido

        if fim - inicio > 90:
            fim = inicio + 90

        return {
            "trecho": trecho,
            "prioridade": destaque.get(
                "prioridade",
                "media",
            ),
            "inicio": round(inicio, 2),
            "fim": round(fim, 2),
            "duracao": round(
                fim - inicio,
                2,
            ),
            "status": "pronto_para_corte",
            "modo": "inteligente",
            "motivo_editor": decisao.get(
                "motivo",
                "",
            ),
            "formato": decisao.get(
                "formato",
                "vertical",
            ),
        }

    except Exception:
        # Se a IA falhar, o ORION continua funcionando.
        return corte_rapido


def executar(intencao, dados=None):
    """
    Entrada principal do Agente Editor.
    """

    dados = dados or {}

    if intencao != "preparar_edicao":
        return "Não reconheci essa solicitação de edição."

    destaque = dados.get("destaque")

    if not destaque:
        return (
            "Preciso de um momento "
            "para preparar o corte."
        )

    modo = dados.get(
        "modo",
        "rapido",
    )

    if modo == "inteligente":
        corte = preparar_corte_inteligente(
            destaque,
            contexto=dados.get(
                "contexto",
                "",
            ),
        )

    else:
        corte = preparar_corte(
            destaque
        )

    if corte is None:
        return "Não consegui preparar esse corte."

    if corte["inicio"] is None:
        return (
            "Encontrei o trecho, mas ainda não tenho "
            "os horários necessários para cortar o vídeo."
        )

    return (
        f"Corte {corte['modo']} preparado. "
        f"Início em {corte['inicio']} segundos, "
        f"fim em {corte['fim']} segundos, "
        f"duração de {corte['duracao']} segundos."
    )