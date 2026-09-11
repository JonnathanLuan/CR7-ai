# ORION HOME — primeiro painel no computador

Esta atualização permite continuar o ORION enquanto o Redmi aguarda o
desbloqueio. A janela roda no Windows e conversa com o núcleo Python existente.
Ainda não é um aplicativo Android e não conecta o telefone pela rede.

## Aplicar a atualização

1. Feche o ORION, caso esteja aberto.
2. Faça uma cópia da sua pasta atual `ORION-v0.5-nucleo` como backup.
3. Extraia o ZIP atualizado em uma pasta temporária.
4. Copie **o conteúdo** da pasta extraída `ORION-v0.5-nucleo` para dentro da
   sua pasta original `C:\Users\jonna\Desktop\ORION-v0.5-nucleo`.
5. Substitua os arquivos de código quando o Windows perguntar.
6. Na pasta original, dê dois cliques em `INICIAR_ORION_HOME.bat`.

O pacote não inclui `.env`, ambientes virtuais, banco de dados ou logs.
Mantenha os seus arquivos locais: eles guardam configurações, dependências e
histórico. Não apague sua pasta antiga nem execute apenas a pasta temporária.
Nenhuma dependência nova é necessária para o painel se seu Python tem Tkinter
e as dependências do núcleo já estavam instaladas.

## Primeiro teste

1. Digite `oi` e clique em **Enviar**.
2. Use **Minha memória** e depois **Enviar**, para conferir a memória existente.
3. Digite uma pergunta livre para testar o provedor configurado no seu `.env`.
4. Se quiser ouvir a resposta, marque **Ler respostas em voz alta** e envie
   outra mensagem. Se houver falha, a resposta permanece na tela.
5. Experimente **Usar microfone**. Confirme o aviso e fale uma frase. Revise o
   texto reconhecido antes de clicar em **Enviar**.

O rótulo de provedor indica a configuração, não um teste de conexão nem qual
provedor respondeu após fallback. Gemini e Ollama continuam com a configuração
existente. Nenhuma chave é exibida na interface.

## Microfone e voz

- Entrada de voz exige SpeechRecognition, PyAudio, microfone e permissão do
  Windows. A transcrição atual usa o Google e precisa de internet.
- A falha de instalação do PyAudio ainda precisa ser resolvida no computador:
  esta versão trata a ausência dele, mas não o substitui por outro capturador.
- A leitura usa pyttsx3 e as vozes do sistema; a existência de voz em português
  depende da instalação local.
- O microfone só é acionado pelo botão. Não há escuta contínua ou palavra de
  ativação nesta versão.

## Atalhos

- Enter envia a mensagem; Shift+Enter quebra a linha.
- F11 alterna tela cheia; Esc sai da tela cheia.
- Para analisar código, use o atalho, envie o pedido e depois cole o código
  completo na caixa. Não é necessário digitar FIM no painel.
- Digite `cancelar` para sair do pedido de código.
- As conversas continuam salvas no banco local do projeto, como no terminal.
- Para usar o terminal antigo, execute `python app.py`.

## Se não abrir

Envie uma captura do erro que aparecer na janela do terminal. O atalho procura
primeiro `.venv`, depois `venv` e depois o Python disponível no computador.
Para verificar se esse Python tem interface gráfica, execute `python -m tkinter`
no mesmo ambiente. Não é necessário instalar ROM ou desbloquear o Redmi para
testar este painel.

## Validação desta entrega

- Testes do núcleo e novos testes de sessão/áudio passaram em ambiente isolado.
- Memória e histórico foram testados com banco temporário; nenhum provedor
  externo foi chamado durante os testes.
- Sintaxe dos módulos alterados verificada.
- Janela, permissões e áudio reais no Windows ainda precisam ser testados.
- Próxima etapa: validar esta base no seu computador e preparar a interface
  do Redmi e sua conexão ao núcleo pela rede.
