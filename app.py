from agentes.ferramentas.programador import (
    MENSAGEM_SOLICITAR_CODIGO,
    analisar_codigo,
)
from core.interpretador import interpretar
from core.historico import registrar_conversa
from config import NOME, VERSAO


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


# ==========================
# ESTADO DA CONVERSA
# ==========================

aguardando_codigo = False


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
# LOOP PRINCIPAL
# ==========================

while True:
    comando = input("Você > ")

    if comando.lower().strip() == "sair":
        print(f"{NOME} encerrado.")
        break

    resposta = interpretar(comando)

    print(f"{NOME}:", resposta)

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

        registrar_conversa(
            "[Código enviado para análise]",
            resposta_analise,
        )

        aguardando_codigo = False