"""Ferramentas nativas registradas no núcleo do ORION.

As dependências opcionais são importadas sob demanda para que o núcleo
continue testável mesmo em uma instalação mínima.
"""

from core.ferramentas.registro import Ferramenta, registro


def _tarefas():
    from agentes.ferramentas.gerenciador_tarefas import (
        adicionar_tarefa, concluir_tarefa, listar_tarefas, remover_tarefa,
    )
    return adicionar_tarefa, concluir_tarefa, listar_tarefas, remover_tarefa


def _adicionar_tarefa(descricao):
    return _tarefas()[0](descricao)


def _concluir_tarefa(id_tarefa):
    return _tarefas()[1](id_tarefa)


def _listar_tarefas():
    return _tarefas()[2]()


def _remover_tarefa(id_tarefa):
    return _tarefas()[3](id_tarefa)


def _abrir_programa(programa: str):
    from plugins.gerenciador import executar_plugin
    aberto = executar_plugin("sistema", "abrir_programa", programa)
    return f"Programa '{programa}' aberto com sucesso." if aberto else f"Não encontrei o programa '{programa}' na lista de programas conhecidos."


def _lembrar_informacao(chave: str, valor: str):
    from core.memoria import carregar_memoria, salvar_memoria
    memoria = carregar_memoria()
    memoria.setdefault("informacoes", {})[chave] = valor
    salvar_memoria(memoria)
    return f"Guardei: {chave} = {valor}."


def _formatar_resultados_busca(resultados):
    if isinstance(resultados, str):
        return resultados
    return "\n\n".join(
        f"{i}. {r.get('titulo', '')}\n   Link: {r.get('link', '')}\n   Resumo: {r.get('resumo', '')}"
        for i, r in enumerate(resultados, 1)
    )


def _buscar_na_internet(consulta, max_resultados=5):
    from agentes.ferramentas.pesquisa import buscar_na_internet
    return _formatar_resultados_busca(buscar_na_internet(consulta, max_resultados))


def _ler_pagina_web(url):
    from agentes.ferramentas.pesquisa import ler_pagina_web
    return ler_pagina_web(url)


def _analisar_codigo(codigo):
    from agentes.ferramentas.programador import analisar_codigo
    return analisar_codigo(codigo)


def registrar_ferramentas_nativas():
    if registro.listar():
        return registro

    registro.registrar(Ferramenta(
        "adicionar_tarefa", "Adiciona uma nova tarefa.", _adicionar_tarefa,
        {"type": "object", "properties": {"descricao": {"type": "string"}}, "required": ["descricao"]}, tags=("tarefas",),
    ))
    registro.registrar(Ferramenta(
        "listar_tarefas", "Lista tarefas pendentes e concluídas.", _listar_tarefas,
        {"type": "object", "properties": {}}, tags=("tarefas",),
    ))
    registro.registrar(Ferramenta(
        "concluir_tarefa", "Conclui uma tarefa pelo ID.", _concluir_tarefa,
        {"type": "object", "properties": {"id_tarefa": {"type": "integer"}}, "required": ["id_tarefa"]},
        risco="medio", requer_confirmacao=True, tags=("tarefas",),
    ))
    registro.registrar(Ferramenta(
        "remover_tarefa", "Remove uma tarefa pelo ID.", _remover_tarefa,
        {"type": "object", "properties": {"id_tarefa": {"type": "integer"}}, "required": ["id_tarefa"]},
        risco="medio", requer_confirmacao=True, tags=("tarefas",),
    ))
    registro.registrar(Ferramenta(
        "abrir_programa", "Abre um programa conhecido no computador.", _abrir_programa,
        {"type": "object", "properties": {"programa": {"type": "string"}}, "required": ["programa"]},
        risco="medio", requer_confirmacao=True, tags=("sistema",),
    ))
    registro.registrar(Ferramenta(
        "lembrar_informacao", "Guarda uma informação na memória de longo prazo.", _lembrar_informacao,
        {"type": "object", "properties": {"chave": {"type": "string"}, "valor": {"type": "string"}}, "required": ["chave", "valor"]}, tags=("memoria",),
    ))
    registro.registrar(Ferramenta(
        "buscar_na_internet", "Pesquisa informação atual na internet.", _buscar_na_internet,
        {"type": "object", "properties": {"consulta": {"type": "string"}, "max_resultados": {"type": "integer"}}, "required": ["consulta"]}, tags=("web",),
    ))
    registro.registrar(Ferramenta(
        "ler_pagina_web", "Lê o conteúdo principal de uma URL.", _ler_pagina_web,
        {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}, tags=("web",),
    ))
    registro.registrar(Ferramenta(
        "analisar_codigo", "Analisa código Python com AST.", _analisar_codigo,
        {"type": "object", "properties": {"codigo": {"type": "string"}}, "required": ["codigo"]}, tags=("programacao",),
    ))
    return registro


registrar_ferramentas_nativas()
