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