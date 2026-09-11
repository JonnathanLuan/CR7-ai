"""Políticas de segurança para ferramentas e ações do ORION."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PoliticaFerramenta:
    risco: str
    requer_confirmacao: bool = False


POLITICAS = {
    "baixo": PoliticaFerramenta("baixo", False),
    "medio": PoliticaFerramenta("medio", True),
    "alto": PoliticaFerramenta("alto", True),
}
