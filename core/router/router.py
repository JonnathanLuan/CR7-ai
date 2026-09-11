"""Router central do ORION: decide o caminho antes do LLM."""

from dataclasses import dataclass
from core.decisor import decidir as decidir_regras


@dataclass(frozen=True)
class Rota:
    tipo: str
    confianca: float
    motivo: str
    usar_llm: bool


class Router:
    def rotear(self, texto: str) -> Rota:
        decisao = decidir_regras(texto)
        usar_llm = decisao.tipo in {"conversa", "desconhecida"}
        return Rota(decisao.tipo, decisao.confianca, decisao.motivo, usar_llm)


router = Router()
