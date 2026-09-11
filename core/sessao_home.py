"""Conversa do painel local, reutilizando o interpretador e o histórico."""

from agentes.ferramentas.programador import MENSAGEM_SOLICITAR_CODIGO, analisar_codigo
from core.historico import registrar_conversa
from core.interpretador import interpretar

PEDIDO_CODIGO_HOME = (
    "Cole o código Python na caixa abaixo e clique em Enviar. "
    "Use Shift+Enter para quebrar linhas. Digite cancelar para voltar à conversa."
)


class SessaoHome:
    def __init__(self):
        self.aguardando_codigo = False

    def responder(self, mensagem):
        if not mensagem.strip():
            return "Digite uma mensagem para começar."
        if self.aguardando_codigo:
            if mensagem.strip().lower() == "cancelar":
                self.aguardando_codigo = False
                return "Análise cancelada. Podemos continuar a conversa."
            resposta = analisar_codigo(mensagem)
            registrar_conversa("[Código enviado para análise]", resposta)
            self.aguardando_codigo = False
            return resposta

        resposta = interpretar(mensagem)
        if resposta == MENSAGEM_SOLICITAR_CODIGO:
            self.aguardando_codigo = True
            resposta = PEDIDO_CODIGO_HOME
        registrar_conversa(mensagem, resposta)
        return resposta
