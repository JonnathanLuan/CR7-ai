"""Contrato base para agentes do ORION."""

from abc import ABC, abstractmethod
from core.runtime.contexto import ContextoExecucao
from core.runtime.resultado import ResultadoExecucao


class AgenteBase(ABC):
    nome = "agente"
    descricao = "Agente ORION"

    @abstractmethod
    def executar(self, contexto: ContextoExecucao) -> ResultadoExecucao:
        raise NotImplementedError
