"""
Integração da ORION com um modelo de linguagem (LLM) externo.

Esse módulo é o que permite à ORION conversar livremente sobre
qualquer assunto (não só os comandos fixos do sistema de regras)
e, através de "function calling", decidir sozinha quando deve
usar uma das ferramentas reais do projeto (tarefas, abrir
programas, analisar código) em vez de só responder em texto.

Funciona com dois provedores possíveis (config.PROVEDOR_LLM):
  - "openai"     -> usa a lib `openai`
  - "anthropic"  -> usa a lib `anthropic`

Se nenhuma chave de API estiver configurada, `usar_llm_disponivel()`
retorna False e a ORION continua funcionando normalmente só com o
sistema de regras (core/nlp).
"""

import json

import config
from agentes.ferramentas.gerenciador_tarefas import (
    adicionar_tarefa,
    concluir_tarefa,
    listar_tarefas,
    remover_tarefa,
)
from agentes.ferramentas.programador import analisar_codigo
from agentes.ferramentas.pesquisa import buscar_na_internet, ler_pagina_web
from core.historico import carregar_historico
from core.memoria import carregar_memoria, salvar_memoria
from plugins.gerenciador import executar_plugin


PROMPT_SISTEMA = (
    "Você é a {nome}, uma assistente pessoal em português do Brasil, "
    "direta, simpática e prestativa. Você foi criada por {autor}. "
    "Quando o pedido do usuário puder ser resolvido com uma das "
    "ferramentas disponíveis (tarefas, abrir programas, analisar "
    "código, pesquisar na internet), use a ferramenta em vez de "
    "apenas descrever o que faria. Sempre que o assunto exigir "
    "informação atual, específica ou que você não tem certeza "
    "(notícias, preços, tutoriais técnicos, passo a passo de algo, "
    "dados que podem ter mudado), use 'buscar_na_internet' antes de "
    "responder, e use 'ler_pagina_web' quando precisar aprofundar "
    "em um resultado específico. Para qualquer outro assunto, "
    "converse normalmente, de forma objetiva e sem enrolação."
)


# ==========================
# DEFINIÇÃO DAS FERRAMENTAS
# ==========================
# Formato compatível com a API de "tools" da OpenAI.
# (a conversão para o formato da Anthropic é feita em
# `_ferramentas_para_anthropic`)

FERRAMENTAS = [
    {
        "type": "function",
        "function": {
            "name": "adicionar_tarefa",
            "description": "Adiciona uma nova tarefa à lista de tarefas do usuário.",
            "parameters": {
                "type": "object",
                "properties": {
                    "descricao": {
                        "type": "string",
                        "description": "Descrição da tarefa a ser criada.",
                    }
                },
                "required": ["descricao"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "listar_tarefas",
            "description": "Lista todas as tarefas cadastradas, pendentes e concluídas.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "concluir_tarefa",
            "description": "Marca uma tarefa existente como concluída, pelo ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id_tarefa": {
                        "type": "integer",
                        "description": "ID numérico da tarefa a concluir.",
                    }
                },
                "required": ["id_tarefa"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remover_tarefa",
            "description": "Remove uma tarefa existente da lista, pelo ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id_tarefa": {
                        "type": "integer",
                        "description": "ID numérico da tarefa a remover.",
                    }
                },
                "required": ["id_tarefa"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "abrir_programa",
            "description": "Abre um programa conhecido no computador do usuário (ex: bloco de notas, calculadora, paint).",
            "parameters": {
                "type": "object",
                "properties": {
                    "programa": {
                        "type": "string",
                        "description": "Nome do programa a abrir.",
                    }
                },
                "required": ["programa"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lembrar_informacao",
            "description": "Guarda uma informação pessoal do usuário na memória de longo prazo (ex: time do coração, profissão, filme favorito).",
            "parameters": {
                "type": "object",
                "properties": {
                    "chave": {"type": "string", "description": "Nome da informação, ex: 'time', 'profissão'."},
                    "valor": {"type": "string", "description": "Valor da informação, ex: 'Sport', 'engenheiro'."},
                },
                "required": ["chave", "valor"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_na_internet",
            "description": (
                "Pesquisa um termo na internet (estilo Google) e devolve título, "
                "link e resumo dos resultados. Use para qualquer assunto que exija "
                "informação atual, específica, técnica ou que você não tenha "
                "certeza — ex: 'como trocar o sistema de um celular', 'o que é "
                "terapia cognitivo-comportamental', notícias, preços, tutoriais."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "consulta": {
                        "type": "string",
                        "description": "Termo ou pergunta a pesquisar.",
                    },
                    "max_resultados": {
                        "type": "integer",
                        "description": "Quantos resultados trazer (padrão 5).",
                    },
                },
                "required": ["consulta"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ler_pagina_web",
            "description": (
                "Abre uma URL específica (geralmente um link retornado por "
                "'buscar_na_internet') e devolve o texto principal da página, "
                "para ler um tutorial, artigo ou explicação com mais profundidade."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Endereço completo da página (com http:// ou https://).",
                    }
                },
                "required": ["url"],
            },
        },
    },
]


def _abrir_programa(programa):
    aberto = executar_plugin("sistema", "abrir_programa", programa)
    if aberto:
        return f"Programa '{programa}' aberto com sucesso."
    return f"Não encontrei o programa '{programa}' na lista de programas conhecidos."


def _lembrar_informacao(chave, valor):
    memoria = carregar_memoria()
    memoria.setdefault("informacoes", {})[chave] = valor
    salvar_memoria(memoria)
    return f"Guardei: {chave} = {valor}."


def _formatar_resultados_busca(resultados):
    if isinstance(resultados, str):
        return resultados  # já é uma mensagem de erro/aviso

    linhas = []
    for indice, resultado in enumerate(resultados, start=1):
        linhas.append(
            f"{indice}. {resultado['titulo']}\n"
            f"   Link: {resultado['link']}\n"
            f"   Resumo: {resultado['resumo']}"
        )

    return "\n\n".join(linhas)


DESPACHO_FERRAMENTAS = {
    "adicionar_tarefa": lambda args: adicionar_tarefa(args.get("descricao", "")),
    "listar_tarefas": lambda args: listar_tarefas(),
    "concluir_tarefa": lambda args: concluir_tarefa(int(args.get("id_tarefa"))),
    "remover_tarefa": lambda args: remover_tarefa(int(args.get("id_tarefa"))),
    "abrir_programa": lambda args: _abrir_programa(args.get("programa", "")),
    "lembrar_informacao": lambda args: _lembrar_informacao(
        args.get("chave", ""), args.get("valor", "")
    ),
    "buscar_na_internet": lambda args: _formatar_resultados_busca(
        buscar_na_internet(args.get("consulta", ""), args.get("max_resultados", 5))
    ),
    "ler_pagina_web": lambda args: ler_pagina_web(args.get("url", "")),
}


def executar_ferramenta(nome, argumentos):
    funcao = DESPACHO_FERRAMENTAS.get(nome)

    if funcao is None:
        return f"Ferramenta '{nome}' não existe."

    try:
        return funcao(argumentos)
    except Exception as erro:  # noqa: BLE001 - queremos devolver qualquer erro ao LLM
        return f"Erro ao executar '{nome}': {erro}"


# ==========================
# DISPONIBILIDADE
# ==========================

def usar_llm_disponivel():
    """
    Retorna True se há uma chave de API configurada para o
    provedor escolhido em config.PROVEDOR_LLM.
    """

    if not config.USAR_LLM:
        return False

    if config.PROVEDOR_LLM == "anthropic":
        return bool(config.ANTHROPIC_API_KEY)

    return bool(config.OPENAI_API_KEY)


# ==========================
# CONTEXTO
# ==========================

def _montar_contexto_memoria():
    memoria = carregar_memoria()

    partes = []

    if memoria.get("nome"):
        partes.append(f"Nome do usuário: {memoria['nome']}.")
    if memoria.get("idade"):
        partes.append(f"Idade: {memoria['idade']}.")
    if memoria.get("cidade"):
        partes.append(f"Cidade: {memoria['cidade']}.")

    for chave, valor in memoria.get("informacoes", {}).items():
        partes.append(f"{chave.capitalize()}: {valor}.")

    if not partes:
        return "Ainda não sei nada sobre o usuário."

    return "O que eu sei sobre o usuário até agora -> " + " ".join(partes)


def _montar_mensagens(comando):
    prompt_sistema = PROMPT_SISTEMA.format(nome=config.NOME, autor=config.AUTOR)
    prompt_sistema += "\n\n" + _montar_contexto_memoria()

    mensagens = [{"role": "system", "content": prompt_sistema}]

    for troca in carregar_historico(limite=config.HISTORICO_CONTEXTO):
        mensagens.append({"role": "user", "content": troca["usuario"]})
        mensagens.append({"role": "assistant", "content": troca["orion"]})

    mensagens.append({"role": "user", "content": comando})

    return mensagens


# ==========================
# PROVEDOR: OPENAI
# ==========================

def _responder_openai(comando):
    from openai import OpenAI

    cliente = OpenAI(api_key=config.OPENAI_API_KEY)
    mensagens = _montar_mensagens(comando)

    for _ in range(4):  # limite de segurança contra loops de ferramentas
        resposta = cliente.chat.completions.create(
            model=config.MODELO_OPENAI,
            messages=mensagens,
            tools=FERRAMENTAS,
        )

        mensagem = resposta.choices[0].message

        if not mensagem.tool_calls:
            return mensagem.content or "Não consegui gerar uma resposta."

        mensagens.append(mensagem)

        for chamada in mensagem.tool_calls:
            argumentos = json.loads(chamada.function.arguments or "{}")
            resultado = executar_ferramenta(chamada.function.name, argumentos)

            mensagens.append(
                {
                    "role": "tool",
                    "tool_call_id": chamada.id,
                    "content": str(resultado),
                }
            )

    return "Tentei usar várias ferramentas, mas não consegui concluir o pedido."


# ==========================
# PROVEDOR: ANTHROPIC
# ==========================

def _ferramentas_para_anthropic():
    convertidas = []

    for ferramenta in FERRAMENTAS:
        funcao = ferramenta["function"]
        convertidas.append(
            {
                "name": funcao["name"],
                "description": funcao["description"],
                "input_schema": funcao["parameters"],
            }
        )

    return convertidas


def _responder_anthropic(comando):
    import anthropic

    cliente = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    prompt_sistema = PROMPT_SISTEMA.format(nome=config.NOME, autor=config.AUTOR)
    prompt_sistema += "\n\n" + _montar_contexto_memoria()

    mensagens = []
    for troca in carregar_historico(limite=config.HISTORICO_CONTEXTO):
        mensagens.append({"role": "user", "content": troca["usuario"]})
        mensagens.append({"role": "assistant", "content": troca["orion"]})
    mensagens.append({"role": "user", "content": comando})

    for _ in range(4):
        resposta = cliente.messages.create(
            model=config.MODELO_ANTHROPIC,
            max_tokens=1024,
            system=prompt_sistema,
            messages=mensagens,
            tools=_ferramentas_para_anthropic(),
        )

        blocos_ferramenta = [b for b in resposta.content if b.type == "tool_use"]

        if not blocos_ferramenta:
            texto = "".join(b.text for b in resposta.content if b.type == "text")
            return texto or "Não consegui gerar uma resposta."

        mensagens.append({"role": "assistant", "content": resposta.content})

        resultados = []
        for bloco in blocos_ferramenta:
            resultado = executar_ferramenta(bloco.name, bloco.input)
            resultados.append(
                {
                    "type": "tool_result",
                    "tool_use_id": bloco.id,
                    "content": str(resultado),
                }
            )

        mensagens.append({"role": "user", "content": resultados})

    return "Tentei usar várias ferramentas, mas não consegui concluir o pedido."


# ==========================
# PONTO DE ENTRADA
# ==========================

def gerar_resposta(comando):
    """
    Gera uma resposta usando o LLM configurado, com acesso às
    ferramentas da ORION via function calling. Levanta exceção
    se algo falhar na chamada de API — quem chama decide o que
    fazer (ex: cair de volta pro sistema de regras).
    """

    if config.PROVEDOR_LLM == "anthropic":
        return _responder_anthropic(comando)

    return _responder_openai(comando)
