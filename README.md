# 🤖 CR7 AI

> **Uma plataforma de Inteligência Artificial modular desenvolvida em Python para atuar como assistente pessoal, programador, pesquisador e executor de tarefas.**

![Status](https://img.shields.io/badge/status-Em%20Desenvolvimento-orange)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Version](https://img.shields.io/badge/version-0.4%20Alpha-green)

---

# 📖 Sobre

O **CR7 AI** é um projeto de Inteligência Artificial criado para evoluir continuamente através de uma arquitetura modular baseada em **Core**, **Agentes**, **Ferramentas** e **Plugins**.

Mais do que um chatbot, o objetivo do CR7 AI é tornar-se uma plataforma completa capaz de auxiliar pessoas em programação, organização pessoal, estudos, pesquisas e automação de tarefas.

Todo o projeto está sendo desenvolvido com foco em organização, escalabilidade e aprendizado contínuo.

---

# ✨ Objetivos

O CR7 AI está sendo desenvolvido para ser capaz de:

- 🧠 Aprender continuamente
- 💬 Conversar naturalmente
- 👤 Atuar como assistente pessoal
- 👨‍💻 Auxiliar no desenvolvimento de software
- 📚 Pesquisar informações
- 🌐 Utilizar serviços online
- 🎙 Conversar por voz
- 👁 Interpretar imagens e documentos
- 🖥 Automatizar tarefas do computador
- 🔌 Trabalhar através de plugins
- 🤖 Utilizar agentes especializados

---

# 🏗 Arquitetura

```
CR7 AI
│
├── Core
│   ├── IA
│   ├── Memória
│   ├── NLP
│   └── Configuração
│
├── Agentes
│   ├── Programador
│   ├── Pesquisador
│   ├── Escritor
│   ├── Planejador
│   └── ...
│
├── Ferramentas
│   ├── AST
│   ├── Arquivos
│   ├── Git
│   ├── Terminal
│   └── ...
│
├── Plugins
│
├── Dados
│
├── Documentação
│
└── Testes
```

---

# 📁 Estrutura

```
CR7-AI/
│
├── app.py
├── config.py
├── requirements.txt
│
├── core/
├── agentes/
├── plugins/
├── dados/
├── docs/
├── testes/
└── logs/
```

---

# 🚀 Funcionalidades atuais

## 🧠 Núcleo

- ✅ Memória permanente (SQLite)
- ✅ Histórico de conversas (SQLite)
- ✅ Personalidade
- ✅ Migração automática dos dados antigos em JSON

---

## 🤖 Inteligência conversacional (LLM)

- ✅ Conversa livre com um LLM externo (OpenAI ou Anthropic) quando o comando não é reconhecido pelo sistema de regras
- ✅ Function calling: o LLM aciona as ferramentas reais da ORION (tarefas, abrir programas, memória, pesquisa na internet)
- ✅ Contexto de memória e histórico enviado automaticamente

---

## 🌐 Pesquisa na internet

- ✅ Busca na internet (sem precisar de chave de API — usa DuckDuckGo)
- ✅ Leitura do conteúdo de uma página específica para aprofundar num assunto
- ✅ O LLM decide sozinho quando pesquisar: tutoriais, "como fazer X", psicologia, notícias, qualquer assunto que exija informação atual ou específica

---

## 💬 NLP

- ✅ Normalizador
- ✅ Detector de intenções
- ✅ Extrator de informações
- ✅ Executor de intenções
- ✅ Aprendizado de informações

---

## ✅ Tarefas

- ✅ Adicionar, listar, concluir e remover tarefas por comando de texto ou voz

---

## 🎙 Voz

- ✅ Síntese de voz (a ORION fala as respostas)
- ✅ Reconhecimento de fala (modo voz — a ORION ouve pelo microfone)

---

## 👨‍💻 Agente Programador

- ✅ Leitura de arquivos Python
- ✅ Análise utilizando AST
- ✅ Contagem de funções
- ✅ Contagem de classes
- ✅ Contagem de importações
- ✅ Sistema de sugestões
- ✅ Arquitetura modular

---

# ⚙️ Configuração rápida

```bash
pip install -r requirements.txt
cp .env.example .env
# edite o .env e cole sua chave da OpenAI ou da Anthropic
python app.py
```

Sem chave de API configurada, a ORION continua funcionando normalmente,
só que apenas com os comandos fixos do sistema de regras (sem conversa livre).

---

# 🚧 Em desenvolvimento

- Explicação inteligente de funções
- Relatórios de código
- Melhorias automáticas
- Documentação automática
- Refatoração assistida

---

# 🔮 Funcionalidades planejadas

## 🎙 Assistente de Voz

- Reconhecimento de fala
- Síntese de voz
- Palavra de ativação
- Conversação contínua

### 👤 Assistente Pessoal

- Agenda
- Calendário
- Lista de tarefas
- Lembretes
- Organização diária
- Rotinas inteligentes

### 🌐 Inteligência Online

- Pesquisa na internet
- Notícias
- Clima
- APIs
- Busca em documentação

### 👁 Visão Computacional

- OCR
- Leitura de imagens
- Leitura de PDFs
- Captura de tela
- Interpretação de gráficos

### 🖥 Automação

- Controle do Windows
- VS Code
- Terminal
- Navegador
- Gerenciamento de arquivos

### 🧠 Inteligência

- Memória de longo prazo
- Contexto entre conversas
- Aprendizado supervisionado
- Perfis de usuários
- Personalidades configuráveis

### 🤖 Sistema de Agentes

- Agente Programador
- Agente Pesquisador
- Agente Escritor
- Agente Professor
- Agente Planejador
- Agente Analista
- Agente Financeiro

### 🔌 Plugins

- Instalação dinâmica
- Atualização automática
- Plugins oficiais
- Plugins da comunidade

### 📱 Plataformas

- Desktop
- Web
- Android
- iOS
- API REST

---

# 📚 Documentação

A documentação do projeto está organizada nos seguintes arquivos:

| Documento | Descrição |
|-----------|-----------|
| README.md | Visão geral do projeto |
| CHANGELOG.md | Histórico das versões |
| ROADMAP.md | Planejamento das próximas versões |

Documentação em desenvolvimento:

- VISION.md
- ARCHITECTURE.md
- AGENTS.md
- DEVLOG.md

---

# 🛠 Tecnologias

Atualmente

- Python
- JSON
- Git
- GitHub

Planejado

- SQLite
- FastAPI
- Ollama
- OpenAI API
- Speech Recognition
- Text-to-Speech

---

# 🎯 Objetivo Final

Construir uma plataforma completa de Inteligência Artificial capaz de atuar como:

- Assistente Pessoal
- Programador
- Pesquisador
- Professor
- Organizador
- Executor de tarefas

Tudo isso através de uma arquitetura modular baseada em **Core**, **Agentes** e **Plugins**.

---

# 👨‍💻 Autor

**Jonnathan Luan**

Projeto desenvolvido em Python.

Arquitetura e desenvolvimento com apoio do ChatGPT.

---

# 📄 Licença

Este projeto encontra-se em desenvolvimento e ainda não possui uma licença definitiva.