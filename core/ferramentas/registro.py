"""Registro central e seguro das ferramentas do ORION."""

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class Ferramenta:
    nome: str
    descricao: str
    handler: Callable[..., Any]
    parametros: dict[str, Any] = field(default_factory=lambda: {"type": "object", "properties": {}})
    risco: str = "baixo"
    requer_confirmacao: bool = False
    tags: tuple[str, ...] = ()

    def schema_openai(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.nome,
                "description": self.descricao,
                "parameters": self.parametros,
            },
        }

    def schema_anthropic(self) -> dict[str, Any]:
        return {
            "name": self.nome,
            "description": self.descricao,
            "input_schema": self.parametros,
        }


class RegistroFerramentas:
    def __init__(self) -> None:
        self._ferramentas: dict[str, Ferramenta] = {}

    def registrar(self, ferramenta: Ferramenta) -> Ferramenta:
        if ferramenta.nome in self._ferramentas:
            raise ValueError(f"Ferramenta já registrada: {ferramenta.nome}")
        self._ferramentas[ferramenta.nome] = ferramenta
        return ferramenta

    def obter(self, nome: str) -> Ferramenta | None:
        return self._ferramentas.get(nome)

    def listar(self) -> list[Ferramenta]:
        return list(self._ferramentas.values())

    def executar(self, nome: str, argumentos: dict[str, Any] | None = None, *, confirmar=False) -> Any:
        ferramenta = self.obter(nome)
        if ferramenta is None:
            return f"Ferramenta '{nome}' não existe."
        if ferramenta.requer_confirmacao and not confirmar:
            return f"A ferramenta '{nome}' exige confirmação antes da execução."
        try:
            return ferramenta.handler(**(argumentos or {}))
        except TypeError as erro:
            return f"Argumentos inválidos para '{nome}': {erro}"
        except Exception as erro:  # noqa: BLE001
            return f"Erro ao executar '{nome}': {erro}"

    def schemas_openai(self) -> list[dict[str, Any]]:
        return [f.schema_openai() for f in self.listar()]

    def schemas_anthropic(self) -> list[dict[str, Any]]:
        return [f.schema_anthropic() for f in self.listar()]


registro = RegistroFerramentas()


def ferramenta(nome: str, descricao: str = "", parametros: dict | None = None, *, risco: str = "baixo", requer_confirmacao: bool = False, tags: tuple[str, ...] = ()):
    """Decorator compatível para registrar uma função como ferramenta."""
    def decorator(func):
        registro.registrar(Ferramenta(
            nome=nome, descricao=descricao or (func.__doc__ or "").strip(), handler=func,
            parametros=parametros or {"type": "object", "properties": {}}, risco=risco,
            requer_confirmacao=requer_confirmacao, tags=tags,
        ))
        return func
    return decorator
