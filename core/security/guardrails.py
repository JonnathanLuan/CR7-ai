"""Validações simples antes de executar ações externas."""

from core.runtime.resultado import ResultadoExecucao


def validar_mensagem(mensagem: str) -> ResultadoExecucao:
    if not isinstance(mensagem, str) or not mensagem.strip():
        return ResultadoExecucao.erro("A mensagem não pode estar vazia.", "mensagem_vazia")
    if len(mensagem) > 20000:
        return ResultadoExecucao.erro("A mensagem excede o limite permitido.", "mensagem_grande")
    return ResultadoExecucao.ok("Mensagem válida.")
