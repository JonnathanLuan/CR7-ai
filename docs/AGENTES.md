# 🤖 Agentes ORION

## Princípio

Agentes não devem conhecer detalhes do banco, do provedor de LLM ou da interface. Eles recebem contexto e usam ferramentas por meio de contratos definidos pelo núcleo.

## Agente base

`agentes/base.py` define `AgenteBase` com:

- `nome`
- `descricao`
- `executar(contexto)`

## Agentes atuais

- Assistente
- Programador

O Gerente mantém compatibilidade com `executar_agente(intencao, dados)` enquanto a nova arquitetura é adotada gradualmente.

## Futuro

O objetivo é permitir que um agente gerente encaminhe uma tarefa para especialistas, compartilhando o mesmo contexto de execução.
