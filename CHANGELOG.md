# 📄 CHANGELOG — ORION

## 🚀 0.5 Alpha — Núcleo Inteligente

### Arquitetura
- Adicionado `core/runtime/` com contexto, execução e resultados padronizados.
- Adicionado `core/router/` para centralizar o roteamento das solicitações.
- Mantida compatibilidade com o decisor anterior em `core/decisor.py`.
- Criada base `AgenteBase` para padronizar agentes futuros.
- Reorganizado o subsistema LLM em `core/llm/`, mantendo a API pública `gerar_resposta()`.
- `gerar_resposta()` voltou a respeitar o provedor definido em `PROVEDOR_LLM` (Ollama, Gemini, OpenAI ou Anthropic).

### Ferramentas
- Criado `RegistroFerramentas` centralizado.
- Ferramentas nativas passaram a possuir nome, descrição, schema, tags e nível de risco.
- Schemas podem ser convertidos para formatos de function calling de OpenAI e Anthropic.
- Gemini passa a obter suas declarações diretamente do registro central.
- Dependências opcionais de pesquisa/voz deixam de impedir a importação do núcleo.

### Segurança
- Criado primeiro guardrail de entrada.
- Criada camada de políticas de risco para ferramentas.
- Ações de médio risco são marcadas para confirmação no registro, preparando um fluxo de aprovação mais completo.

### Qualidade
- Criados testes automatizados do novo núcleo.
- Validação com `pytest` e `compileall`.
- `.env` real não faz parte do pacote de distribuição.
- Atualizados exemplos de configuração e dependências.

## Versões anteriores

Consulte o histórico Git para detalhes das versões 0.1–0.4.
