"""
Histórico de conversas da ORION.

Mesma interface pública de antes (registrar_conversa,
obter_ultima_fala_usuario, carregar_historico), agora apoiada
em SQLite em vez de um arquivo JSON solto.
"""

from datetime import datetime

from core import banco


def carregar_historico(limite=None):
    """
    Retorna o histórico de conversas em ordem cronológica.
    Se `limite` for informado, retorna apenas as últimas N conversas
    (útil para dar contexto recente ao LLM sem estourar o prompt).
    """

    with banco.conectar() as conexao:
        if limite:
            linhas = conexao.execute(
                "SELECT data, usuario, orion FROM historico "
                "ORDER BY id DESC LIMIT ?",
                (limite,),
            ).fetchall()
            linhas = list(reversed(linhas))
        else:
            linhas = conexao.execute(
                "SELECT data, usuario, orion FROM historico ORDER BY id ASC"
            ).fetchall()

    return [
        {"data": linha["data"], "usuario": linha["usuario"], "orion": linha["orion"]}
        for linha in linhas
    ]


def registrar_conversa(pergunta, resposta):
    """
    Salva uma troca de mensagens (usuário + ORION) no histórico.
    """

    with banco.conectar() as conexao:
        conexao.execute(
            "INSERT INTO historico (data, usuario, orion) VALUES (?, ?, ?)",
            (
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                pergunta,
                resposta,
            ),
        )


def obter_ultima_fala_usuario():
    """
    Retorna a última mensagem enviada pelo usuário, ou None
    se ainda não houver nenhuma conversa registrada.
    """

    with banco.conectar() as conexao:
        linha = conexao.execute(
            "SELECT usuario FROM historico ORDER BY id DESC LIMIT 1"
        ).fetchone()

    return linha["usuario"] if linha else None
