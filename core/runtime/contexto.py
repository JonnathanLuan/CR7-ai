"""Contexto de uma execução do ORION."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import uuid


@dataclass
class ContextoExecucao:
    """Estado transitório compartilhado entre router, agente e tools."""

    mensagem: str
    sessao_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    execucao_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    criado_em: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    dados: dict[str, Any] = field(default_factory=dict)
    metadados: dict[str, Any] = field(default_factory=dict)

    def adicionar_evento(self, nome: str, **dados: Any) -> None:
        eventos = self.metadados.setdefault("eventos", [])
        eventos.append({"nome": nome, "dados": dados})
