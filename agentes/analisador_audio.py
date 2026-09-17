"""
Analisador de áudio do ORION.

Analisa segmentos da live procurando
mudanças de volume que podem indicar:

- gritos
- comemorações
- sustos
- rage
- reações fortes
"""

import re
import statistics
import subprocess
from pathlib import Path


def _duracao(caminho):
    """
    Obtém a duração do arquivo usando FFprobe.
    """

    comando = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(caminho),
    ]

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=15,
        )

        if resultado.returncode != 0:
            return None

        return round(
            float(resultado.stdout.strip()),
            2,
        )

    except Exception:
        return None


def analisar_segmento(caminho):
    """
    Mede o volume médio e o pico máximo
    de um segmento de vídeo.
    """

    caminho = Path(caminho)

    if not caminho.exists():
        return None

    comando = [
        "ffmpeg",
        "-hide_banner",
        "-nostats",
        "-i",
        str(caminho),
        "-vn",
        "-af",
        "volumedetect",
        "-f",
        "null",
        "-",
    ]

    try:
        resultado = subprocess.run(
            comando,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )

    except Exception:
        return None

    texto = resultado.stderr

    media = re.search(
        r"mean_volume:\s*(-?\d+(?:\.\d+)?)\s*dB",
        texto,
    )

    maximo = re.search(
        r"max_volume:\s*(-?\d+(?:\.\d+)?)\s*dB",
        texto,
    )

    if not media:
        return None

    return {
        "arquivo": str(caminho),
        "duracao": _duracao(caminho),
        "volume_medio_db": float(
            media.group(1)
        ),
        "volume_maximo_db": (
            float(maximo.group(1))
            if maximo
            else None
        ),
    }


def analisar_buffer(
    pasta="buffer_live",
):
    """
    Analisa todos os segmentos existentes
    no buffer da live.
    """

    pasta = Path(pasta)

    segmentos = list(
        pasta.glob("parte_*.ts")
    )

    segmentos.sort(
        key=lambda arquivo:
        arquivo.stat().st_mtime
    )

    resultados = []

    for segmento in segmentos:
        analise = analisar_segmento(
            segmento
        )

        if analise:
            resultados.append(
                analise
            )

    return resultados


def detectar_reacoes(
    analises,
    aumento_db=4.0,
):
    """
    Compara cada segmento com o volume normal
    da transmissão.

    Quanto mais próximo de zero estiver o valor
    em dB, mais alto é o áudio.
    """

    if not analises:
        return []

    volumes = [
        item["volume_medio_db"]
        for item in analises
    ]

    volume_base = statistics.median(
        volumes
    )

    resultados = []

    for indice, item in enumerate(
        analises
    ):
        diferenca = (
            item["volume_medio_db"]
            - volume_base
        )

        if diferenca >= 6:
            intensidade = "forte"

        elif diferenca >= aumento_db:
            intensidade = "media"

        else:
            continue

        resultados.append(
            {
                "segmento": indice,
                "arquivo": item["arquivo"],
                "intensidade": intensidade,
                "aumento_db": round(
                    diferenca,
                    2,
                ),
                "volume_medio_db":
                    item["volume_medio_db"],
                "volume_base_db":
                    round(volume_base, 2),
                "possivel_evento":
                    "reacao_audio",
            }
        )

    return resultados