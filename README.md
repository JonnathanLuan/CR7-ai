# 🤖 ORION — CR7 IA

> Plataforma modular de Inteligência Artificial desenvolvida em Python.

**Versão:** 0.5 Alpha — Núcleo Inteligente  
**Autor:** Jonnathan Luan

## Visão

O ORION está sendo construído como uma plataforma de assistente de IA, e não apenas como um chatbot. A arquitetura combina Core, Runtime, Router, Agentes, Ferramentas, Memória, Plugins e provedores de LLM.

## O que mudou no 0.5

- Runtime com contexto de execução.
- Resultado padronizado para operações internas.
- Router central.
- Registro único de ferramentas.
- Schemas reutilizáveis para function calling.
- Base de agentes.
- Camada inicial de segurança.
- Suporte arquitetural a Ollama, Gemini, OpenAI e Anthropic.
- Testes automatizados do núcleo.

## Estrutura

```text
ORION/
├── app.py
├── config.py
├── core/
│   ├── runtime/
│   ├── router/
│   ├── llm/
│   ├── security/
│   ├── ferramentas/
│   ├── conhecimento/
│   ├── nlp/
│   ├── memoria.py
│   └── banco.py
├── agentes/
├── tools/
├── plugins/
├── tests/
├── docs/
└── database/
```

## Configuração

1. Crie um ambiente virtual.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Copie `.env.example` para `.env` e configure o provedor.
4. Para Ollama, deixe o serviço local ativo e configure `MODELO_OLLAMA`.
5. Para Gemini/OpenAI/Anthropic, informe a chave no `.env`.

> O arquivo `.env` real nunca deve ser enviado ao GitHub.

## Execução

```bash
python app.py
```

## Testes

```bash
python -m pytest -q
```

## Documentação

- `docs/ARQUITETURA.md` — arquitetura do núcleo.
- `docs/AGENTES.md` — modelo de agentes.
- `ROADMAP.md` — próximas versões.
- `CHANGELOG.md` — histórico.

## Próxima etapa

**0.6 — Memória Inteligente:** separar memória de sessão, memória permanente e recuperação de informações relevantes.
