"""
Buffer circular de lives do ORION.

Mantém apenas os últimos segundos da transmissão
em pequenos arquivos temporários.
"""

import math
import subprocess
import sys
from pathlib import Path

from agentes.captura_live import verificar_live
from agentes.analisador_audio import analisar_buffer, detectar_reacoes


class BufferLive:
    def __init__(
        self,
        url,
        duracao_buffer=120,
        duracao_segmento=5,
        pasta="buffer_live",
    ):
        self.url = url
        self.duracao_buffer = duracao_buffer
        self.duracao_segmento = duracao_segmento

        self.pasta = Path(pasta)

        self.streamlink_process = None
        self.ffmpeg_process = None

        self.qualidade = None

    def _escolher_qualidade(self, streams):
        """
        Dá preferência a boa qualidade para
        permitir gerar o clip depois.
        """

        preferencias = (
            "1080p60",
            "1080p",
            "720p60",
            "720p",
            "best",
        )

        for qualidade in preferencias:
            if qualidade in streams:
                return qualidade

        return "best"

    def _limpar_buffer_antigo(self):
        self.pasta.mkdir(
            parents=True,
            exist_ok=True,
        )

        for arquivo in self.pasta.glob(
            "parte_*.ts"
        ):
            try:
                arquivo.unlink()
            except Exception:
                pass

    def iniciar(self):
        """
        Inicia Streamlink + FFmpeg.
        """

        if self.ffmpeg_process is not None:
            return {
                "status": "ja_rodando",
                "qualidade": self.qualidade,
            }

        info = verificar_live(
            self.url
        )

        if info.get("status") != "online":
            return info

        self.qualidade = self._escolher_qualidade(
            info.get("streams", [])
        )

        self._limpar_buffer_antigo()

        quantidade_segmentos = max(
            4,
            math.ceil(
                self.duracao_buffer
                / self.duracao_segmento
            ),
        )

        comando_streamlink = [
            sys.executable,
            "-m",
            "streamlink",
            "--stdout",
            self.url,
            self.qualidade,
        ]

        comando_ffmpeg = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",

            "-i",
            "pipe:0",

            "-map",
            "0:v?",

            "-map",
            "0:a?",

            "-c",
            "copy",

            "-f",
            "segment",

            "-segment_time",
            str(self.duracao_segmento),

            "-segment_wrap",
            str(quantidade_segmentos),

            "-reset_timestamps",
            "1",

            str(
                self.pasta
                / "parte_%03d.ts"
            ),
        ]

        self.streamlink_process = subprocess.Popen(
            comando_streamlink,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

        self.ffmpeg_process = subprocess.Popen(
            comando_ffmpeg,
            stdin=self.streamlink_process.stdout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if self.streamlink_process.stdout:
            self.streamlink_process.stdout.close()

        return {
            "status": "buffer_iniciado",
            "qualidade": self.qualidade,
            "duracao_buffer": self.duracao_buffer,
            "segmento": self.duracao_segmento,
            "quantidade_segmentos": quantidade_segmentos,
            "pasta": str(
                self.pasta.resolve()
            ),
        }

    def listar_segmentos(self):
        """
        Lista os arquivos existentes,
        do mais antigo ao mais recente.
        """

        arquivos = list(
            self.pasta.glob(
                "parte_*.ts"
            )
        )

        arquivos.sort(
            key=lambda arquivo:
            arquivo.stat().st_mtime
        )

        return arquivos

    def analisar_audio(self):
        """
        Analisa o áudio dos segmentos atuais do buffer
        e procura possíveis reações.
        """

        analises = analisar_buffer(
            str(self.pasta)
        )

        reacoes = detectar_reacoes(
            analises
        )

        return {
            "status": "analise_concluida",
            "segmentos_analisados": len(
                analises
            ),
            "reacoes_detectadas": len(
                reacoes
            ),
            "reacoes": reacoes,
        }

    def parar(self):
        """
        Encerra o buffer.
        """

        if self.ffmpeg_process:
            try:
                self.ffmpeg_process.terminate()
                self.ffmpeg_process.wait(
                    timeout=5
                )
            except Exception:
                try:
                    self.ffmpeg_process.kill()
                except Exception:
                    pass

        if self.streamlink_process:
            try:
                self.streamlink_process.terminate()
                self.streamlink_process.wait(
                    timeout=5
                )
            except Exception:
                try:
                    self.streamlink_process.kill()
                except Exception:
                    pass

        self.ffmpeg_process = None
        self.streamlink_process = None

        return {
            "status": "buffer_parado",
            "segmentos": len(
                self.listar_segmentos()
            ),
        }