import json
from pathlib import Path


ARQUIVO_TAREFAS = Path("data/tarefas.json")


def carregar_tarefas():
    if not ARQUIVO_TAREFAS.exists():
        return []

    try:
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except (json.JSONDecodeError, OSError):
        return []


def salvar_tarefas(tarefas):
    ARQUIVO_TAREFAS.parent.mkdir(parents=True, exist_ok=True)

    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as arquivo:
        json.dump(
            tarefas,
            arquivo,
            ensure_ascii=False,
            indent=4,
        )

def adicionar_tarefa(descricao):
    descricao = str(descricao).strip()

    if not descricao:
        return "A descrição da tarefa não pode ficar vazia."

    tarefas = carregar_tarefas()

    novo_id = 1

    if tarefas:
        novo_id = max(
            tarefa["id"]
            for tarefa in tarefas
        ) + 1

    nova_tarefa = {
        "id": novo_id,
        "descricao": descricao,
        "concluida": False,
    }

    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)

    return f'Tarefa adicionada: "{descricao}".'    

def listar_tarefas():
    tarefas = carregar_tarefas()

    if not tarefas:
        return "Você ainda não possui tarefas cadastradas."

    linhas = []

    for tarefa in tarefas:
        status = "Concluída" if tarefa["concluida"] else "Pendente"

        linhas.append(
            f'{tarefa["id"]}. {tarefa["descricao"]} - {status}'
        )

    return "\n".join(linhas) 

def remover_tarefa(id_tarefa):
    tarefas = carregar_tarefas()

    for tarefa in tarefas:

        if tarefa["id"] == id_tarefa:

            tarefas.remove(tarefa)

            salvar_tarefas(tarefas)

            return "Tarefa removida com sucesso."

    return "Tarefa não encontrada."   

def remover_tarefa(id_tarefa):
    tarefas = carregar_tarefas()

    for tarefa in tarefas:

        if tarefa["id"] == id_tarefa:

            tarefas.remove(tarefa)

            salvar_tarefas(tarefas)

            return "Tarefa removida com sucesso."

    return "Tarefa não encontrada."

def concluir_tarefa(id_tarefa):
    tarefas = carregar_tarefas()

    for tarefa in tarefas:

        if tarefa["id"] == id_tarefa:

            tarefa["concluida"] = True

            salvar_tarefas(tarefas)

            return "Tarefa concluída com sucesso."

    return "Tarefa não encontrada."