"""Executor central do pipeline do ORION."""

from core.runtime.contexto import ContextoExecucao
from core.runtime.resultado import ResultadoExecucao


def executar(etapa, contexto: ContextoExecucao) -> ResultadoExecucao:
    """Executa uma etapa e converte exceções em resultados padronizados."""
    contexto.adicionar_evento("inicio_etapa", etapa=getattr(etapa, "__name__", str(etapa)))
    try:
        resultado = etapa(contexto)
        if isinstance(resultado, ResultadoExecucao):
            final = resultado
        else:
            final = ResultadoExecucao.ok(str(resultado), dados=resultado)
    except Exception as erro:  # noqa: BLE001
        contexto.adicionar_evento("erro_etapa", erro=str(erro))
        final = ResultadoExecucao.erro(str(erro), codigo="exception")
    contexto.adicionar_evento("fim_etapa", sucesso=final.sucesso, codigo=final.codigo)
    return final
