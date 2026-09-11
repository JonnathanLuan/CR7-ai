"""
Gerenciador de tarefas da ORION — agora em SQLite (core/banco.py)
em vez de data/tarefas.json.
"""

from datetime import datetime

from core import banco


def carregar_tarefas():
    with banco.conectar() as conexao:
        linhas = conexao.execute(
            "SELECT id, descricao, concluida FROM tarefas ORDER BY id ASC"
        ).fetchall()

    return [
        {
            "id": linha["id"],
            "descricao": linha["descricao"],
            "concluida": bool(linha["concluida"]),
        }
        for linha in linhas
    ]


def adicionar_tarefa(descricao):
    descricao = str(descricao).strip()

    if not descricao:
        return "A descrição da tarefa não pode ficar vazia."

    with banco.conectar() as conexao:
        conexao.execute(
            "INSERT INTO tarefas (descricao, concluida, criada_em) VALUES (?, 0, ?)",
            (descricao, datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
        )

    return f'Tarefa adicionada: "{descricao}".'


def adicionar_lembrete(descricao, lembrar_em):
    descricao = str(descricao).strip()

    if not descricao or not lembrar_em:
        return "Não consegui criar o lembrete."

    with banco.conectar() as conexao:
        conexao.execute(
            """
            INSERT INTO tarefas
            (descricao, concluida, criada_em, lembrar_em, avisada)
            VALUES (?, 0, ?, ?, 0)
            """,
            (
                descricao,
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                lembrar_em,
            ),
        )

    horario = datetime.strptime(
        lembrar_em,
        "%Y-%m-%d %H:%M:%S"
    )

    return (
        f"Lembrete criado: {descricao}, "
        f"às {horario.strftime('%H:%M')}."
    )


def listar_tarefas():
    tarefas = carregar_tarefas()

    if not tarefas:
        return "Você ainda não possui tarefas cadastradas."

    linhas = []

    for tarefa in tarefas:
        status = "Concluída" if tarefa["concluida"] else "Pendente"
        linhas.append(f'{tarefa["id"]}. {tarefa["descricao"]} - {status}')

    return "\n".join(linhas)


def remover_tarefa(id_tarefa):
    with banco.conectar() as conexao:
        cursor = conexao.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))

    if cursor.rowcount == 0:
        return "Tarefa não encontrada."

    return "Tarefa removida com sucesso."


def concluir_tarefa(id_tarefa):
    with banco.conectar() as conexao:
        cursor = conexao.execute(
            "UPDATE tarefas SET concluida = 1 WHERE id = ?", (id_tarefa,)
        )

    if cursor.rowcount == 0:
        return "Tarefa não encontrada."

    return "Tarefa concluída com sucesso."
