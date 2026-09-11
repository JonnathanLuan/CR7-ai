import os

from dotenv import load_dotenv

load_dotenv()

# ==========================
# INFORMAÇÕES GERAIS
# ==========================

NOME = "CR7 IA"

VERSAO = "0.5 Alpha - Núcleo"

AUTOR = "Jonnathan Luan"

DATA_CRIACAO = "17/07/2026"


# ==========================
# INTELIGÊNCIA ARTIFICIAL (LLM)
# ==========================

# Provedores disponíveis:
# "openai", "anthropic" ou "ollama"
PROVEDOR_LLM = os.getenv("PROVEDOR_LLM", "ollama")


# ==========================
# OPENAI
# ==========================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODELO_OPENAI = os.getenv("MODELO_OPENAI", "gpt-4o-mini")


# ==========================
# ANTHROPIC
# ==========================

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODELO_ANTHROPIC = os.getenv(
    "MODELO_ANTHROPIC",
    "claude-sonnet-4-5"
)


# ==========================
# GEMINI
# ==========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODELO_GEMINI = os.getenv(
    "MODELO_GEMINI",
    "gemini-3.6-flash"
)


# ==========================
# OLLAMA - IA LOCAL
# ==========================

# Endereço padrão do servidor Ollama
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

# Modelo instalado no computador
MODELO_OLLAMA = os.getenv(
    "MODELO_OLLAMA",
    "qwen2.5:1.5b"
)


# ==========================
# HISTÓRICO
# ==========================

# Quantas trocas de mensagens recentes são enviadas
# como contexto para o LLM.
HISTORICO_CONTEXTO = int(
    os.getenv("HISTORICO_CONTEXTO", "10")
)


# ==========================
# SISTEMA LLM
# ==========================

# Se True, ORION tenta usar o LLM sempre que o sistema
# de regras não reconhecer o comando.
#
# Se False, mantém o comportamento antigo:
# "ainda não sei responder isso".
USAR_LLM = os.getenv(
    "USAR_LLM",
    "true"
).lower() in ("1", "true", "sim")