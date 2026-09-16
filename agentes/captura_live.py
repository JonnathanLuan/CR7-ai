"""
Captura de lives do ORION.

Plataformas:
- Twitch
- Kick

Usa stream leve para monitoramento
e qualidade alta para gerar clips.
"""

import streamlink

from streamlink.exceptions import (
    NoPluginError,
    PluginError,
    StreamlinkError,
)


QUALIDADES_ANALISE = (
    "audio_only",
    "160p",
    "360p",
    "480p",
    "worst",
)


def _obter_streams(url):
    try:
        return streamlink.streams(
            str(url).strip()
        )

    except (
        NoPluginError,
        PluginError,
        StreamlinkError,
    ):
        return {}

    except Exception:
        return {}


def verificar_live(url):
    """
    Verifica se a transmissão está disponível.
    """

    url = str(url).strip()

    if not url:
        return {
            "status": "url_invalida",
            "streams": [],
        }

    try:
        streams = streamlink.streams(url)

    except NoPluginError:
        return {
            "status": "plataforma_nao_suportada",
            "streams": [],
        }

    except PluginError as erro:
        return {
            "status": "erro_plugin",
            "erro": str(erro),
            "streams": [],
        }

    except StreamlinkError as erro:
        return {
            "status": "erro_streamlink",
            "erro": str(erro),
            "streams": [],
        }

    except Exception as erro:
        return {
            "status": "erro",
            "erro": str(erro),
            "streams": [],
        }

    if not streams:
        return {
            "status": "offline",
            "streams": [],
        }

    qualidades = list(
        streams.keys()
    )

    qualidade_analise = None

    for qualidade in QUALIDADES_ANALISE:
        if qualidade in streams:
            qualidade_analise = qualidade
            break

    return {
        "status": "online",
        "streams": qualidades,
        "qualidade_analise": qualidade_analise,
        "qualidade_clip": (
            "best"
            if "best" in streams
            else qualidades[-1]
        ),
    }


def escolher_stream_analise(url):
    """
    Escolhe automaticamente a transmissão
    mais leve disponível.
    """

    streams = _obter_streams(url)

    if not streams:
        return None

    for qualidade in QUALIDADES_ANALISE:
        if qualidade in streams:
            return {
                "qualidade": qualidade,
                "stream": streams[qualidade],
            }

    return {
        "qualidade": "best",
        "stream": streams.get("best"),
    }


def escolher_stream_clip(url):
    """
    Escolhe a melhor qualidade disponível
    para gerar o clip final.
    """

    streams = _obter_streams(url)

    if not streams:
        return None

    if "best" in streams:
        return {
            "qualidade": "best",
            "stream": streams["best"],
        }

    nome, stream = list(
        streams.items()
    )[-1]

    return {
        "qualidade": nome,
        "stream": stream,
    }