"""
Integração da ORION com modelos de linguagem (LLM).

Provedores disponíveis:
- openai
- anthropic
- ollama
- gemini
"""

import json
import urllib.error
import urllib.request

import config
from core.historico import carregar_historico
from core.memoria import carregar_memoria, salvar_memoria
from core.ferramentas.registro import registro
from tools.builtin import registrar_ferramentas_nativas


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
            "description": "Abre um programa conhecido no computador do usuário.",
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
            "description": "Guarda uma informação pessoal do usuário na memória de longo prazo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "chave": {
                        "type": "string",
                        "description": "Nome da informação.",
                    },
                    "valor": {
                        "type": "string",
                        "description": "Valor da informação.",
                    },
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
                "Pesquisa um termo na internet e devolve título, "
                "link e resumo dos resultados."
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
                        "description": "Quantidade máxima de resultados.",
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
            "description": "Abre uma URL específica e devolve o texto principal da página.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Endereço completo da página.",
                    }
                },
                "required": ["url"],
            },
        },
    },
]


# ==========================
# IMPLEMENTAÇÃO DAS FERRAMENTAS
# ==========================

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
        return resultados

    linhas = []

    for indice, resultado in enumerate(resultados, start=1):
        linhas.append(
            f"{indice}. {resultado['titulo']}\n"
            f"   Link: {resultado['link']}\n"
            f"   Resumo: {resultado['resumo']}"
        )

    return "\n\n".join(linhas)


def executar_ferramenta(nome, argumentos):
    """Executa uma ferramenta pelo registro central."""
    registrar_ferramentas_nativas()
    return registro.executar(nome, argumentos or {}, confirmar=True)


# ==========================
# DISPONIBILIDADE
# ==========================

def _ferramentas_registradas():
    registrar_ferramentas_nativas()
    return registro.schemas_openai()


def usar_llm_disponivel():
    """
    Verifica se o provedor configurado está disponível.
    """

    if not config.USAR_LLM:
        return False

    if config.PROVEDOR_LLM == "ollama":
        return True

    if config.PROVEDOR_LLM == "anthropic":
        return bool(config.ANTHROPIC_API_KEY)

    if config.PROVEDOR_LLM == "gemini":
        return bool(config.GEMINI_API_KEY)

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
    prompt_sistema = PROMPT_SISTEMA.format(
        nome=config.NOME,
        autor=config.AUTOR,
    )

    prompt_sistema += "\n\n" + _montar_contexto_memoria()

    mensagens = [
        {
            "role": "system",
            "content": prompt_sistema,
        }
    ]

    historico = carregar_historico(
        limite=config.HISTORICO_CONTEXTO
    )

    if historico:
        linhas = ["CONTEXTO RECENTE DA CONVERSA:"]

        for troca in historico:
            linhas.append(
                f"Usuário: {troca['usuario']}"
            )
            linhas.append(
                f"CR7: {troca['orion']}"
            )

        mensagens.append(
            {
                "role": "system",
                "content": "\n".join(linhas),
            }
        )

    mensagens.append(
        {
            "role": "user",
            "content": comando,
        }
    )

    return mensagens


# ==========================
# PROVEDOR: OPENAI
# ==========================

def _responder_openai(comando):
    from openai import OpenAI

    cliente = OpenAI(
        api_key=config.OPENAI_API_KEY
    )

    mensagens = _montar_mensagens(comando)

    for _ in range(4):
        resposta = cliente.chat.completions.create(
            model=config.MODELO_OPENAI,
            messages=mensagens,
            tools=_ferramentas_registradas(),
        )

        mensagem = resposta.choices[0].message

        if not mensagem.tool_calls:
            return mensagem.content or "Não consegui gerar uma resposta."

        mensagens.append(mensagem)

        for chamada in mensagem.tool_calls:
            argumentos = json.loads(
                chamada.function.arguments or "{}"
            )

            resultado = executar_ferramenta(
                chamada.function.name,
                argumentos,
            )

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
    registrar_ferramentas_nativas()
    return registro.schemas_anthropic()


def _responder_anthropic(comando):
    import anthropic

    cliente = anthropic.Anthropic(
        api_key=config.ANTHROPIC_API_KEY
    )

    prompt_sistema = PROMPT_SISTEMA.format(
        nome=config.NOME,
        autor=config.AUTOR,
    )

    prompt_sistema += "\n\n" + _montar_contexto_memoria()

    mensagens = []

    for troca in carregar_historico(
        limite=config.HISTORICO_CONTEXTO
    ):
        mensagens.append(
            {
                "role": "user",
                "content": troca["usuario"],
            }
        )

        mensagens.append(
            {
                "role": "assistant",
                "content": troca["orion"],
            }
        )

    mensagens.append(
        {
            "role": "user",
            "content": comando,
        }
    )

    for _ in range(4):
        resposta = cliente.messages.create(
            model=config.MODELO_ANTHROPIC,
            max_tokens=1024,
            system=prompt_sistema,
            messages=mensagens,
            tools=_ferramentas_para_anthropic(),
        )

        blocos_ferramenta = [
            bloco
            for bloco in resposta.content
            if bloco.type == "tool_use"
        ]

        if not blocos_ferramenta:
            texto = "".join(
                bloco.text
                for bloco in resposta.content
                if bloco.type == "text"
            )

            return texto or "Não consegui gerar uma resposta."

        mensagens.append(
            {
                "role": "assistant",
                "content": resposta.content,
            }
        )

        resultados = []

        for bloco in blocos_ferramenta:
            resultado = executar_ferramenta(
                bloco.name,
                bloco.input,
            )

            resultados.append(
                {
                    "type": "tool_result",
                    "tool_use_id": bloco.id,
                    "content": str(resultado),
                }
            )

        mensagens.append(
            {
                "role": "user",
                "content": resultados,
            }
        )

    return "Tentei usar várias ferramentas, mas não consegui concluir o pedido."


# ==========================
# PROVEDOR: OLLAMA
# ==========================

def _responder_ollama(comando):
    """Conversa com Ollama e suporta tool calling quando o modelo oferecer suporte."""
    mensagens = _montar_mensagens(comando)
    dados = {
        "model": config.MODELO_OLLAMA,
        "messages": mensagens,
        "stream": False,
        "keep_alive": "10m",
        "tools": _ferramentas_registradas(),
    }
    url = config.OLLAMA_URL.rstrip("/") + "/api/chat"

    for _ in range(4):
        requisicao = urllib.request.Request(
            url, data=json.dumps(dados).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(requisicao, timeout=300) as resposta:
                resultado = json.loads(resposta.read().decode("utf-8"))
        except urllib.error.URLError as erro:
            raise RuntimeError(
                "Não foi possível conectar ao Ollama. Verifique se o Ollama está aberto."
            ) from erro

        mensagem = resultado.get("message", {})
        chamadas = mensagem.get("tool_calls") or []
        if not chamadas:
            return mensagem.get("content") or "Não consegui gerar uma resposta."

        mensagens.append(mensagem)
        for chamada in chamadas:
            funcao = chamada.get("function", {})
            nome = funcao.get("name", "")
            argumentos = funcao.get("arguments") or {}
            if isinstance(argumentos, str):
                try:
                    argumentos = json.loads(argumentos)
                except json.JSONDecodeError:
                    argumentos = {}
            resultado_tool = executar_ferramenta(nome, argumentos)
            mensagens.append({
                "role": "tool",
                "content": str(resultado_tool),
            })
        dados["messages"] = mensagens

    return "Tentei usar várias ferramentas, mas não consegui concluir o pedido."


# ==========================
# PROVEDOR: GEMINI
# ==========================

def _responder_gemini(comando):
    """
    Responde usando o Gemini com suporte a function calling.
    """

    if not config.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY não configurada no arquivo .env."
        )

    try:
        from google import genai
        from google.genai import types

        cliente = genai.Client(
            api_key=config.GEMINI_API_KEY
        )

        prompt_sistema = PROMPT_SISTEMA.format(
            nome=config.NOME,
            autor=config.AUTOR,
        )

        contexto_memoria = _montar_contexto_memoria()

        historico = carregar_historico(
            limite=config.HISTORICO_CONTEXTO
        )

        partes_prompt = [
            prompt_sistema,
            "",
            "MEMÓRIA:",
            contexto_memoria,
        ]

        if historico:
            partes_prompt.extend(
                [
                    "",
                    "CONTEXTO RECENTE DA CONVERSA:",
                ]
            )

            for troca in historico:
                partes_prompt.append(
                    f"Usuário: {troca['usuario']}"
                )
                partes_prompt.append(
                    f"CR7 IA: {troca['orion']}"
                )

        prompt = "\n".join(partes_prompt)

        # ==========================
        # FERRAMENTAS
        # ==========================

        ferramentas_gemini = []

        registrar_ferramentas_nativas()
        for ferramenta in registro.listar():
            ferramentas_gemini.append(
                types.FunctionDeclaration(
                    name=ferramenta.nome,
                    description=ferramenta.descricao,
                    parameters_json_schema=ferramenta.parametros,
                )
            )

        tool = types.Tool(
            function_declarations=ferramentas_gemini
        )

        config_gemini = types.GenerateContentConfig(
            system_instruction=prompt,
            tools=[tool],
        )

        # ==========================
        # HISTÓRICO DA CONVERSAÇÃO
        # ==========================

        conteudos = [
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        text=comando
                    )
                ],
            )
        ]

        # ==========================
        # LOOP DE FUNCTION CALLING
        # ==========================

        for _ in range(4):

            resposta = cliente.models.generate_content(
                model=config.MODELO_GEMINI,
                contents=conteudos,
                config=config_gemini,
            )

            if not resposta.candidates:
                return "Não consegui obter uma resposta do Gemini."

            conteudo_modelo = resposta.candidates[0].content

            # Guarda EXATAMENTE o turno do Gemini.
            conteudos.append(conteudo_modelo)

            chamadas = []

            for parte in conteudo_modelo.parts or []:
                if getattr(parte, "function_call", None):
                    chamadas.append(parte.function_call)

            # ==========================
            # RESPOSTA NORMAL
            # ==========================

            if not chamadas:
                texto = getattr(resposta, "text", None)

                if texto:
                    return texto.strip()

                return "Não consegui gerar uma resposta."

            # ==========================
            # EXECUTAR FERRAMENTAS
            # ==========================

            partes_resposta = []

            for chamada in chamadas:

                nome_ferramenta = chamada.name

                argumentos = dict(
                    chamada.args or {}
                )

              

                resultado = executar_ferramenta(
                    nome_ferramenta,
                    argumentos,
                )

             

                partes_resposta.append(
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=nome_ferramenta,
                            response={
                                "resultado": str(resultado)
                            },
                        )
                    )
                )

            # IMPORTANTE:
            # O function_response precisa vir imediatamente
            # depois do Content que contém o function_call.
            conteudos.append(
                types.Content(
                    role="user",
                    parts=partes_resposta,
                )
            )

        return (
            "A operação foi iniciada, mas não consegui "
            "finalizar a resposta."
        )

    except Exception as erro:
        raise RuntimeError(
            f"Erro ao consultar o Gemini: {erro}"
        ) from erro
# ==========================
# PONTO DE ENTRADA
# ==========================

def gerar_resposta(comando):
    """Gera uma resposta usando o provedor configurado no .env.
    
    Se o Gemini apresentar erro temporário de disponibilidade,
    utiliza o Ollama como fallback.
    """

    provedor = config.PROVEDOR_LLM.lower()

    provedores = {
        "openai": _responder_openai,
        "anthropic": _responder_anthropic,
        "ollama": _responder_ollama,
        "gemini": _responder_gemini,
    }

    funcao = provedores.get(provedor)

    if funcao is None:
        raise RuntimeError(
            f"Provedor LLM desconhecido: {config.PROVEDOR_LLM}. "
            "Use openai, anthropic, ollama ou gemini."
        )

    # ==========================================
    # GEMINI COM FALLBACK PARA OLLAMA
    # ==========================================

    if provedor == "gemini":

        try:
            return funcao(comando)

        except Exception as erro:

            mensagem_erro = str(erro).lower()

            erros_recuperaveis = (
                "503",
                "unavailable",
                "high demand",
                "429",
                "rate limit",
                "timeout",
                "timed out",
                "connection",
                "temporarily",
            )

            if any(
                erro_recuperavel in mensagem_erro
                for erro_recuperavel in erros_recuperaveis
            ):

                print(
                    "\n⚠️ Gemini indisponível temporariamente."
                )

                print(
                    "🔄 Ativando fallback para Ollama..."
                )

                try:
                    resposta = _responder_ollama(comando)

                    print(
                        "✅ Ollama respondeu com sucesso."
                    )

                    return resposta

                except Exception as erro_ollama:

                    raise RuntimeError(
                        "Gemini e Ollama falharam.\n"
                        f"Erro Gemini: {erro}\n"
                        f"Erro Ollama: {erro_ollama}"
                    ) from erro_ollama

            # Erro não recuperável:
            # mantém o comportamento original.
            raise

    # ==========================================
    # OUTROS PROVEDORES
    # ==========================================

    return funcao(comando)