"""Resultado padronizado das operações internas do ORION."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ResultadoExecucao:
    sucesso: bool
    mensagem: str
    dados: Any = None
    codigo: str = "ok"
    metadados: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, mensagem: str, dados: Any = None, **metadados: Any):
        return cls(True, mensagem, dados, "ok", metadados)

    @classmethod
    def erro(cls, mensagem: str, codigo: str = "erro", **metadados: Any):
        return cls(False, mensagem, None, codigo, metadados)
