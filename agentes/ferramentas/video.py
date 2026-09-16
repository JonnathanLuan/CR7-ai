"""
Ferramentas de vídeo do ORION.

Transforma segmentos temporários da live
em clips MP4.
"""

import math
import subprocess
from pathlib import Path


def _listar_segmentos(pasta):
    pasta = Path(pasta)

    arquivos = list(
        pasta.glob("parte_*.ts")
    )

    arquivos.sort(
        key=lambda arquivo:
        arquivo.stat().st_mtime
    )

    return arquivos


def gerar_clip_buffer(
    pasta_buffer="buffer_live",
    arquivo_saida="clips/clip_teste.mp4",
    segundos=20,
    duracao_segmento=5,
):
    """
    Gera um MP4 usando os segmentos mais
    recentes existentes no buffer.
    """

    segmentos = _listar_segmentos(
        pasta_buffer
    )

    if not segmentos:
        return {
            "status": "sem_segmentos",
        }

    quantidade = max(
        1,
        math.ceil(
            segundos / duracao_segmento
        ),
    )

    selecionados = segmentos[-quantidade:]

    saida = Path(
        arquivo_saida
    )

    saida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lista_concat = Path(
        pasta_buffer
    ) / "lista_clip.txt"

    linhas = []

    for segmento in selecionados:
        caminho = (
            segmento.resolve()
            .as_posix()
        )

        linhas.append(
            f"file '{caminho}'"
        )

    lista_concat.write_text(
        "\n".join(linhas),
        encoding="utf-8",
    )

    comando = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(lista_concat),
        "-c",
        "copy",
        "-movflags",
        "+faststart",
        str(saida),
    ]

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
    )

    if resultado.returncode != 0:
        return {
            "status": "erro",
            "erro": resultado.stderr,
        }

    if not saida.exists():
        return {
            "status": "erro",
            "erro": "O arquivo MP4 não foi criado.",
        }

    tamanho_mb = (
        saida.stat().st_size
        / 1024
        / 1024
    )

    return {
        "status": "clip_criado",
        "arquivo": str(
            saida.resolve()
        ),
        "segmentos": len(
            selecionados
        ),
        "tamanho_mb": round(
            tamanho_mb,
            2,
        ),
    }