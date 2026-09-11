# 🏗️ Arquitetura do ORION 0.5

A versão 0.5 organiza o projeto em camadas, mantendo os módulos antigos funcionando enquanto cria uma base para evolução.

```text
Interface
   ↓
Interpretador
   ↓
Router
   ↓
Runtime / Contexto
   ↓
Agente ou LLM
   ↓
Registro de Ferramentas
   ↓
Ferramentas / Plugins
   ↓
Memória + Persistência
```

## 1. Runtime

`core/runtime/contexto.py` guarda o estado transitório de uma execução. Cada solicitação recebe `sessao_id` e `execucao_id`.

`core/runtime/resultado.py` padroniza resultados com `sucesso`, `mensagem`, `codigo`, `dados` e metadados.

## 2. Router

`core/router/router.py` cria uma camada explícita de roteamento. O decisor legado continua disponível para compatibilidade.

## 3. Ferramentas

`core/ferramentas/registro.py` centraliza ferramentas. Cada ferramenta possui schema e classificação de risco. Isso permite que diferentes provedores de LLM recebam as mesmas capacidades do ORION.

## 4. LLM

`core/llm/` substitui o arquivo monolítico por um pacote. A API pública continua simples:

```python
from core import llm
resposta = llm.gerar_resposta("Olá")
```

O provedor é selecionado por `PROVEDOR_LLM`.

## 5. Segurança

`core/security/` é a primeira camada de políticas. A intenção é que ferramentas capazes de alterar o sistema passem por aprovação antes de uma execução automática.

## 6. Próxima evolução

A próxima grande mudança será transformar a memória atual em uma memória por sessão + memória de longo prazo recuperável. Depois, agentes poderão compartilhar contexto por meio do Runtime.
