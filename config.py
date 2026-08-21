import os

from dotenv import load_dotenv

load_dotenv()

# ==========================
# INFORMAÇÕES GERAIS
# ==========================

NOME = "CR7 IA"

VERSAO = "0.4 Alpha"

AUTOR = "Jonnathan Luan"

DATA_CRIACAO = "17/07/2026"


# ==========================
# INTELIGÊNCIA ARTIFICIAL (LLM)
# ==========================

# "openai" ou "anthropic". Veja o .env.example.
PROVEDOR_LLM = os.getenv("PROVEDOR_LLM", "openai")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODELO_OPENAI = os.getenv("MODELO_OPENAI", "gpt-4o-mini")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODELO_ANTHROPIC = os.getenv("MODELO_ANTHROPIC", "claude-sonnet-4-5")

# Quantas trocas de mensagens recentes são enviadas como
# contexto para o LLM quando ele é acionado.
HISTORICO_CONTEXTO = int(os.getenv("HISTORICO_CONTEXTO", "10"))

# Se True, ORION tenta usar o LLM sempre que o sistema de
# regras não reconhecer o comando. Se False, mantém o
# comportamento antigo ("ainda não sei responder isso").
USAR_LLM = os.getenv("USAR_LLM", "true").lower() in ("1", "true", "sim")
