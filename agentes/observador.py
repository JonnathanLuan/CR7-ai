"""
Agente Observador do ORION.

Perfis iniciais:
- EA FC 27
- GTA 6

Analisa transcrições procurando momentos
com potencial para virar clips.
"""

import re


PERFIS = {
    "eafc27": {
        "alta": {
            "gol": "gol",
            "golaço": "gol",
            "golaco": "gol",
            "pênalti": "penalti",
            "penalti": "penalti",
            "virada": "virada",
            "defesa incrível": "defesa",
            "defesa absurda": "defesa",
            "gol contra": "falha",
            "expulso": "cartao",
            "cartão vermelho": "cartao",
            "cartao vermelho": "cartao",
            "bug": "bug",
            "quebrou o jogo": "bug",
        },

        "media": {
            "trave": "jogada",
            "perdeu": "falha",
            "errou": "falha",
            "falha": "falha",
            "que isso": "reacao",
            "não acredito": "reacao",
            "nao acredito": "reacao",
            "absurdo": "reacao",
            "incrível": "reacao",
            "incrivel": "reacao",
            "ridículo": "engracado",
            "ridiculo": "engracado",
            "kkkk": "engracado",
            "risada": "engracado",
            "engraçado": "engracado",
            "engracado": "engracado",
            "que vergonha": "engracado",
            "do nada": "engracado",
            "rage": "rage",
            "roubado": "rage",
        },
    },

    "gta6": {
        "alta": {
            "explodiu": "explosao",
            "explosão": "explosao",
            "explosao": "explosao",
            "perseguição": "perseguicao",
            "perseguicao": "perseguicao",
            "polícia": "policia",
            "policia": "policia",
            "acidente": "acidente",
            "bateu": "acidente",
            "capotou": "acidente",
            "morreu": "morte",
            "bug": "bug",
            "glitch": "bug",
        },

        "media": {
            "que isso": "reacao",
            "não acredito": "reacao",
            "nao acredito": "reacao",
            "absurdo": "reacao",
            "kkkk": "engracado",
            "risada": "engracado",
            "engraçado": "engracado",
            "engracado": "engracado",
            "do nada": "engracado",
            "que loucura": "caos",
            "caos": "caos",
            "fugiu": "fuga",
            "escapou": "fuga",
            "quase": "tensao",
        },
    },
}


PALAVRAS_GERAIS = {
    "alta": {
        "recorde": "momento_raro",
        "campeão": "vitoria",
        "campeao": "vitoria",
        "vitória": "vitoria",
        "vitoria": "vitoria",
    },

    "media": {
        "incrível": "reacao",
        "incrivel": "reacao",
        "surpresa": "reacao",
        "funcionou": "resultado",
        "conseguimos": "resultado",
        "final": "momento_final",
    },
}


def _normalizar(texto):
    return " ".join(
        str(texto).strip().split()
    )


def _separar_frases(texto):
    partes = re.split(
        r"(?<=[.!?])\s+",
        texto,
    )

    return [
        parte.strip()
        for parte in partes
        if parte.strip()
    ]


def _avaliar_texto(texto, perfil):
    texto_minusculo = texto.lower()

    configuracao = PERFIS.get(
        perfil,
        {},
    )

    motivos = []
    categorias = []

    encontrou_alta = False
    encontrou_media = False

    grupos = [
        (
            configuracao.get("alta", {}),
            "alta",
        ),
        (
            configuracao.get("media", {}),
            "media",
        ),
        (
            PALAVRAS_GERAIS["alta"],
            "alta",
        ),
        (
            PALAVRAS_GERAIS["media"],
            "media",
        ),
    ]

    for palavras, nivel in grupos:
        for palavra, categoria in palavras.items():
            if palavra in texto_minusculo:
                if palavra not in motivos:
                    motivos.append(palavra)

                if categoria not in categorias:
                    categorias.append(categoria)

                if nivel == "alta":
                    encontrou_alta = True

                elif nivel == "media":
                    encontrou_media = True

    if encontrou_alta:
        prioridade = "alta"
        potencial = "alto"

    elif encontrou_media:
        prioridade = "media"
        potencial = "medio"

    else:
        prioridade = None
        potencial = None

    # Reação + evento aumenta o potencial do clip.
    if (
        len(categorias) >= 2
        and prioridade is not None
    ):
        potencial = "alto"

    return {
        "motivos": motivos,
        "categorias": categorias,
        "prioridade": prioridade,
        "potencial_clip": potencial,
    }


def analisar_conteudo(
    conteudo,
    perfil="eafc27",
):
    """
    Analisa texto sem marcações de tempo.
    """

    texto = _normalizar(conteudo)

    if not texto:
        return []

    frases = _separar_frases(texto)

    destaques = []

    for frase in frases:
        analise = _avaliar_texto(
            frase,
            perfil,
        )

        if analise["prioridade"]:
            destaques.append(
                {
                    "perfil": perfil,
                    "trecho": frase,
                    "motivos": analise["motivos"],
                    "categorias": analise["categorias"],
                    "prioridade": analise["prioridade"],
                    "potencial_clip": analise["potencial_clip"],
                    "inicio": None,
                    "fim": None,
                }
            )

    return destaques


def analisar_segmentos(
    segmentos,
    perfil="eafc27",
):
    """
    Analisa uma transcrição que possui
    início e fim de cada segmento.
    """

    destaques = []

    for segmento in segmentos:
        texto = _normalizar(
            segmento.get(
                "texto",
                "",
            )
        )

        if not texto:
            continue

        analise = _avaliar_texto(
            texto,
            perfil,
        )

        if analise["prioridade"]:
            destaques.append(
                {
                    "perfil": perfil,
                    "trecho": texto,
                    "motivos": analise["motivos"],
                    "categorias": analise["categorias"],
                    "prioridade": analise["prioridade"],
                    "potencial_clip": analise["potencial_clip"],
                    "inicio": segmento.get("inicio"),
                    "fim": segmento.get("fim"),
                }
            )

    return destaques


def executar(intencao, dados=None):
    """
    Entrada principal do Agente Observador.
    """

    dados = dados or {}

    if intencao != "observar_conteudo":
        return "Não reconheci essa solicitação de observação."

    perfil = dados.get(
        "perfil",
        "eafc27",
    )

    if perfil not in PERFIS:
        return (
            "Ainda não tenho um perfil de observação "
            "para esse jogo."
        )

    segmentos = dados.get(
        "segmentos"
    )

    if segmentos:
        destaques = analisar_segmentos(
            segmentos,
            perfil=perfil,
        )

    else:
        conteudo = dados.get(
            "conteudo",
            "",
        ).strip()

        if not conteudo:
            return "Preciso de um conteúdo para analisar."

        destaques = analisar_conteudo(
            conteudo,
            perfil=perfil,
        )

    if not destaques:
        return (
            "Analisei o conteúdo, mas não encontrei "
            "um momento com potencial de clip."
        )

    destaque = destaques[0]

    categorias = ", ".join(
        destaque["categorias"]
    )

    return (
        f"Encontrei um momento para clip. "
        f"Perfil {perfil}. "
        f"Categoria: {categorias}. "
        f"Prioridade {destaque['prioridade']}. "
        f"Potencial {destaque['potencial_clip']}. "
        f"Trecho: {destaque['trecho']}"
    )