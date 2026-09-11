"""Gerenciador de provedores, mantendo a interface simples do ORION."""

import config

from .providers import LLMProvider


class LLMManager:
    def __init__(self):
        self._providers: dict[str, LLMProvider] = {}

    def registrar(self, provider: LLMProvider):
        self._providers[provider.nome] = provider

    def obter(self, nome=None):
        return self._providers.get(nome or config.PROVEDOR_LLM)

    def disponivel(self):
        provider = self.obter()
        return bool(provider and provider.disponivel())

    def gerar(self, comando: str) -> str:
        provider = self.obter()
        if provider is None:
            raise RuntimeError(f"Provedor LLM '{config.PROVEDOR_LLM}' não está registrado.")
        if not provider.disponivel():
            raise RuntimeError(f"Provedor LLM '{provider.nome}' não está disponível.")
        return provider.gerar(comando)
