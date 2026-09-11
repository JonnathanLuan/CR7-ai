"""
Memória permanente da ORION.

Mantém a mesma interface pública de antes (carregar_memoria /
salvar_memoria), mas agora apoiada em SQLite (core/banco.py)
em vez de um arquivo JSON solto.
"""

from core import banco


def carregar_memoria():
    """
    Carrega toda a memória no mesmo formato que o restante do
    projeto já espera: um dicionário com chaves diretas
    (nome, idade, cidade, ...) e uma sub-chave "informacoes"
    para os dados genéricos aprendidos com o usuário.
    """

    memoria = {"informacoes": {}}

    with banco.conectar() as conexao:
        linhas = conexao.execute("SELECT chave, valor FROM memoria").fetchall()

    for linha in linhas:
        chave = linha["chave"]
        valor = linha["valor"]

        if chave.startswith("info:"):
            memoria["informacoes"][chave[len("info:"):]] = valor
        else:
            memoria[chave] = valor

    return memoria


def salvar_memoria(memoria):
    """
    Persiste o dicionário de memória inteiro no banco,
    substituindo o conteúdo salvo anteriormente.
    """

    informacoes = memoria.get("informacoes", {}) or {}

    with banco.conectar() as conexao:
        for chave, valor in memoria.items():
            if chave == "informacoes" or valor is None:
                continue

            conexao.execute(
                "INSERT OR REPLACE INTO memoria (chave, valor) VALUES (?, ?)",
                (chave, str(valor)),
            )

        for chave, valor in informacoes.items():
            conexao.execute(
                "INSERT OR REPLACE INTO memoria (chave, valor) VALUES (?, ?)",
                (f"info:{chave}", str(valor)),
            )
