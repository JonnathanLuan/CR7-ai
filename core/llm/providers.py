"""Abstração dos provedores de LLM do ORION."""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    nome = "base"

    @abstractmethod
    def disponivel(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def gerar(self, comando: str) -> str:
        raise NotImplementedError
