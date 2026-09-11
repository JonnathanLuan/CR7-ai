"""Compatibilidade do decisor antigo com o Router do ORION."""

from dataclasses import dataclass


@dataclass
class Decisao:
    tipo: str
    confianca: float
    motivo: str


def decidir(texto: str) -> Decisao:
    texto = (texto or "").lower().strip()
    if not texto:
        return Decisao("vazio", 1.0, "Nenhuma mensagem foi informada.")
    if any(p in texto for p in ("qual é meu nome", "qual meu nome", "meu nome", "onde eu moro", "o que você sabe sobre mim", "lembra de mim")):
        return Decisao("memoria", .95, "A solicitação parece consultar informações da memória.")
    if any(p in texto for p in ("analise meu codigo", "analisar meu codigo", "analise este codigo", "analisar este codigo", "verifique meu codigo", "analise o arquivo", "analisar o arquivo")):
        return Decisao("programacao", .95, "A solicitação envolve análise de código.")
    if texto.startswith(("abra ", "abrir ", "feche ", "fechar ", "execute ", "executar ")):
        return Decisao("comando", .90, "A solicitação parece pedir uma ação no computador.")
    return Decisao("conversa", .50, "Nenhuma intenção conhecida foi identificada.")
