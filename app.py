from agentes.ferramentas.programador import (
    MENSAGEM_SOLICITAR_CODIGO,
    analisar_codigo,
)
from core.banco import inicializar_banco
from core.interpretador import interpretar
from core.historico import registrar_conversa
from core.llm import usar_llm_disponivel
from config import NOME, VERSAO
from agentes.ferramentas.voz import falar

# ==========================
# INICIALIZAÇÃO
# ==========================

inicializar_banco()

# ==========================
# TELA INICIAL
# ==========================

print(
    f"""
 ██████╗██████╗ ███████╗
██╔════╝██╔══██╗╚════██║
██║     ██████╔╝    ██╔╝
██║     ██╔══██╗   ██╔╝
╚██████╗██║  ██║   ██║
 ╚═════╝╚═╝  ╚═╝   ╚═╝

        SIIIIUUUU!

      {NOME}
    Versão {VERSAO}

Sistema iniciado com sucesso!
"""
)

if usar_llm_disponivel():
    print("🧠 IA conversacional ATIVA — posso conversar sobre qualquer assunto.")
else:
    print(
        "⚠ IA conversacional INATIVA — configure uma chave de API no arquivo "
        ".env (veja .env.example) para liberar conversas livres. Por enquanto "
        "só respondo aos comandos conhecidos."
    )

print(
    'Digite "modo voz" para ativar o microfone, "modo texto" para voltar '
    'ao teclado, ou "sair" para encerrar.'
)

falar("Siiiiuuuuu! CR7 IA iniciado com sucesso!")

# ==========================
# ESTADO DA CONVERSA
# ==========================

aguardando_codigo = False
modo_voz = False


# ==========================
# RECEBER CÓDIGO
# ==========================

def receber_codigo():
    print()
    print("Cole o código abaixo.")
    print("Digite FIM em uma nova linha quando terminar.")
    print()

    linhas = []

    while True:
        linha = input()

        if linha.strip().upper() == "FIM":
            break

        linhas.append(linha)

    return "\n".join(linhas)


# ==========================
# CAPTURAR COMANDO (TEXTO OU VOZ)
# ==========================

def capturar_comando():
    if not modo_voz:
        return input("Você > ")

    from agentes.ferramentas.ouvido import ouvir

    texto = ouvir()

    if texto is None:
        print("(não entendi, tente novamente)")
        return ""

    print(f"Você (voz) > {texto}")
    return texto


# ==========================
# LOOP PRINCIPAL
# ==========================

while True:
    comando = capturar_comando()

    if not comando.strip():
        continue

    comando_normalizado = comando.lower().strip()

    if comando_normalizado == "sair":
        mensagem_encerramento = f"{NOME} encerrado."
        print(mensagem_encerramento)
        falar(mensagem_encerramento)
        break

    if comando_normalizado == "modo voz":
        modo_voz = True
        print("🎙 Modo voz ativado.")
        continue

    if comando_normalizado == "modo texto":
        modo_voz = False
        print("⌨ Modo texto ativado.")
        continue

    resposta = interpretar(comando)

    print(f"{NOME}:", resposta)
    falar(resposta)

    # Salva a conversa no histórico
    registrar_conversa(comando, resposta)

    if resposta == MENSAGEM_SOLICITAR_CODIGO:
        aguardando_codigo = True

    if aguardando_codigo:
        codigo = receber_codigo()

        if not codigo.strip():
            resposta_analise = "Nenhum código foi informado."
        else:
            resposta_analise = analisar_codigo(codigo)

        print()
        print(f"{NOME}: {resposta_analise}")
        falar(resposta_analise)

        registrar_conversa(
            "[Código enviado para análise]",
            resposta_analise,
        )

        aguardando_codigo = False
