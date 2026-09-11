"""API pública do subsistema LLM do ORION."""

from .compat import gerar_resposta, usar_llm_disponivel
from .manager import LLMManager
from .providers import LLMProvider

__all__ = ["gerar_resposta", "usar_llm_disponivel", "LLMManager", "LLMProvider"]
