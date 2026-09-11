"""
Camada de acesso ao banco de dados SQLite do CR7 AI / ORION.

Substitui o armazenamento antigo em arquivos JSON soltos
(data/memoria.json, data/historico.json, data/tarefas.json)
por um único banco relacional, mais robusto e mais fácil
de consultar conforme o projeto cresce.

Se já existirem os arquivos JSON antigos, eles são migrados
automaticamente na primeira execução (veja `migrar_json_antigo`).
"""

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

CAMINHO_BANCO = Path("database/orion.db")

CAMINHO_MEMORIA_JSON = Path("data/memoria.json")
CAMINHO_HISTORICO_JSON = Path("data/historico.json")
CAMINHO_TAREFAS_JSON = Path("data/tarefas.json")


# ==========================
# CONEXÃO
# ==========================

@contextmanager
def conectar():
    """
    Fornece uma conexão SQLite dentro de um bloco `with`,
    já com row_factory configurado e commit/close automáticos.
    """

    CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

    try:
        yield conexao
        conexao.commit()
    finally:
        conexao.close()


# ==========================
# CRIAÇÃO DAS TABELAS
# ==========================

def inicializar_banco():
    """
    Cria as tabelas do banco caso ainda não existam.
    Deve ser chamada uma vez no início da aplicação.
    """

    with conectar() as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS memoria (
                chave TEXT PRIMARY KEY,
                valor TEXT NOT NULL
            )
            """
        )

        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                usuario TEXT NOT NULL,
                orion TEXT NOT NULL
            )
            """
        )

        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                concluida INTEGER NOT NULL DEFAULT 0,
                criada_em TEXT NOT NULL
            )
            """
        )

    migrar_json_antigo()


# ==========================
# MIGRAÇÃO DOS JSONs ANTIGOS
# ==========================

def _tabela_vazia(conexao, tabela):
    linha = conexao.execute(f"SELECT COUNT(*) AS total FROM {tabela}").fetchone()
    return linha["total"] == 0


def migrar_json_antigo():
    """
    Importa dados dos antigos arquivos JSON (memoria.json,
    historico.json, tarefas.json) para o SQLite, apenas se
    as tabelas ainda estiverem vazias. É seguro rodar sempre.
    """

    with conectar() as conexao:
        # ---- memória ----
        if CAMINHO_MEMORIA_JSON.exists() and _tabela_vazia(conexao, "memoria"):
            try:
                dados = json.loads(CAMINHO_MEMORIA_JSON.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                dados = {}

            informacoes = dados.pop("informacoes", {}) or {}

            for chave, valor in dados.items():
                if valor is None:
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

        # ---- histórico ----
        if CAMINHO_HISTORICO_JSON.exists() and _tabela_vazia(conexao, "historico"):
            try:
                registros = json.loads(CAMINHO_HISTORICO_JSON.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                registros = []

            for registro in registros:
                conexao.execute(
                    "INSERT INTO historico (data, usuario, orion) VALUES (?, ?, ?)",
                    (
                        registro.get("data", datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                        registro.get("usuario", ""),
                        registro.get("orion", ""),
                    ),
                )

        # ---- tarefas ----
        if CAMINHO_TAREFAS_JSON.exists() and _tabela_vazia(conexao, "tarefas"):
            try:
                tarefas = json.loads(CAMINHO_TAREFAS_JSON.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                tarefas = []

            for tarefa in tarefas:
                conexao.execute(
                    "INSERT INTO tarefas (descricao, concluida, criada_em) VALUES (?, ?, ?)",
                    (
                        tarefa.get("descricao", ""),
                        1 if tarefa.get("concluida") else 0,
                        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    ),
                )
