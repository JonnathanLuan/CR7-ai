"""Painel desktop do ORION HOME. Execute com python home.py."""

import os
import queue
import threading
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

FUNDO = "#0b1119"
PAINEL = "#131e2b"
TEXTO = "#edf4fa"
SUAVE = "#a2b4c7"
VERDE = "#87ebbd"


class PainelHome:
    def __init__(self, janela, sessao, historico, provedor):
        self.janela = janela
        self.sessao = sessao
        self.ocupado = False
        self.eventos = queue.Queue()
        self.trabalhos = queue.Queue()
        self.fechado = False
        self.janela.title("ORION HOME · CR7 IA")
        self.janela.geometry("980x760")
        self.janela.minsize(720, 620)
        self.janela.configure(bg=FUNDO)
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar)
        self.janela.bind("<F11>", self.tela_cheia)
        self.janela.bind("<Escape>", lambda e: self.janela.attributes("-fullscreen", False))

        topo = tk.Frame(janela, bg=FUNDO)
        topo.pack(fill="x", padx=28, pady=(24, 14))
        marca = tk.Frame(topo, bg=FUNDO)
        marca.pack(side="left")
        self.rotulo(marca, "ORION HOME", 23, TEXTO, "bold").pack(anchor="w")
        self.rotulo(marca, "CR7 IA  /  ASSISTENTE PESSOAL", 10, VERDE).pack(anchor="w")
        self.relogio = self.rotulo(topo, "", 24, TEXTO)
        self.relogio.pack(side="right")

        faixa = tk.Frame(janela, bg=PAINEL, padx=18, pady=13)
        faixa.pack(fill="x", padx=28)
        self.estado = tk.Label(faixa, text="●  Pronto para conversar", bg=PAINEL,
                               fg=VERDE, font=("Segoe UI", 11, "bold"))
        self.estado.pack(side="left")
        tk.Label(faixa, text=f"Provedor configurado: {provedor}", bg=PAINEL,
                 fg=SUAVE, font=("Segoe UI", 10)).pack(side="right")

        self.rotulo(janela, "Em que posso ajudar hoje?", 19, TEXTO).pack(
            anchor="w", padx=28, pady=(20, 8))
        self.conversa = ScrolledText(
            janela, wrap="word", bg=PAINEL, fg=TEXTO, insertbackground=TEXTO,
            font=("Segoe UI", 12), relief="flat", padx=18, pady=16,
            height=10, state="disabled", borderwidth=0,
        )
        self.conversa.pack(fill="both", expand=True, padx=28)
        self.conversa.tag_configure("Você", foreground=SUAVE, font=("Segoe UI", 10, "bold"))
        self.conversa.tag_configure("CR7 IA", foreground=VERDE, font=("Segoe UI", 10, "bold"))
        self.conversa.tag_configure("Sistema", foreground="#f0c987", font=("Segoe UI", 10, "bold"))
        if historico:
            for troca in historico:
                self.mensagem("Você", troca["usuario"])
                self.mensagem("CR7 IA", troca["orion"])
        else:
            self.mensagem("CR7 IA", "Olá! Escreva uma mensagem ou escolha um dos atalhos abaixo.")

        atalhos = tk.Frame(janela, bg=FUNDO)
        atalhos.pack(fill="x", padx=28, pady=(12, 8))
        self.atalhos = []
        for titulo, comando in (("Minhas tarefas", "listar tarefas"),
                                ("Minha memória", "qual meu nome"),
                                ("Analisar código", "analise o codigo")):
            botao = self.botao(atalhos, titulo, lambda c=comando: self.preencher(c))
            botao.pack(side="left", padx=(0, 8))
            self.atalhos.append(botao)

        self.entrada = tk.Text(janela, height=3, wrap="word", bg=PAINEL,
                               fg=TEXTO, insertbackground=VERDE, relief="flat",
                               font=("Segoe UI", 12), padx=14, pady=10)
        self.entrada.pack(fill="x", padx=28)
        self.entrada.bind("<Return>", self.enter)
        self.entrada.bind("<Shift-Return>", lambda e: None)

        controles = tk.Frame(janela, bg=FUNDO)
        controles.pack(fill="x", padx=28, pady=(10, 8))
        self.microfone = self.botao(controles, "Usar microfone", self.escutar)
        self.microfone.pack(side="left")
        self.usar_voz = tk.BooleanVar(value=False)
        self.opcao_voz = tk.Checkbutton(
            controles, text="Ler respostas em voz alta", variable=self.usar_voz,
            bg=FUNDO, fg=SUAVE, selectcolor=PAINEL, activebackground=FUNDO,
            activeforeground=TEXTO, font=("Segoe UI", 10),
        )
        self.opcao_voz.pack(side="left", padx=12)
        self.enviar_botao = self.botao(controles, "Enviar  →", self.enviar, destaque=True)
        self.enviar_botao.pack(side="right")
        self.rotulo(janela, "Histórico salvo neste computador · Enter envia · Shift+Enter quebra linha · F11 amplia",
                    9, SUAVE).pack(anchor="w", padx=28, pady=(0, 18))
        self.entrada.focus_set()
        threading.Thread(target=self.executar_trabalhos, daemon=True).start()
        self.atualizar_relogio()
        self.janela.after(80, self.receber_eventos)

    @staticmethod
    def rotulo(pai, texto, tamanho, cor, peso="normal"):
        return tk.Label(pai, text=texto, bg=FUNDO, fg=cor, font=("Segoe UI", tamanho, peso))

    @staticmethod
    def botao(pai, texto, comando, destaque=False):
        return tk.Button(pai, text=texto, command=comando, relief="flat", borderwidth=0,
                         bg=VERDE if destaque else PAINEL, fg=FUNDO if destaque else TEXTO,
                         activebackground="#b2f5d6", activeforeground=FUNDO,
                         padx=16, pady=9, cursor="hand2", font=("Segoe UI", 10, "bold"))

    def mensagem(self, autor, texto):
        self.conversa.configure(state="normal")
        self.conversa.insert("end", f"{autor}\n", autor)
        self.conversa.insert("end", f"{texto}\n\n")
        self.conversa.configure(state="disabled")
        self.conversa.see("end")

    def preencher(self, texto):
        if not self.ocupado:
            self.entrada.delete("1.0", "end")
            self.entrada.insert("1.0", texto)
            self.entrada.focus_set()

    def enter(self, evento):
        self.enviar()
        return "break"

    def definir_ocupado(self, ocupado, texto="●  Pronto para conversar"):
        self.ocupado = ocupado
        estado = "disabled" if ocupado else "normal"
        for widget in [self.entrada, self.microfone, self.enviar_botao, self.opcao_voz, *self.atalhos]:
            widget.configure(state=estado)
        self.estado.configure(text=texto)
        if not ocupado:
            self.entrada.focus_set()

    def enviar(self):
        if self.ocupado:
            return
        # Mantém indentação de código colado.
        texto = self.entrada.get("1.0", "end-1c")
        if not texto.strip():
            return
        self.entrada.delete("1.0", "end")
        self.mensagem("Você", texto)
        self.definir_ocupado(True, "●  Preparando resposta…")
        self.trabalhos.put(("conversa", texto, self.usar_voz.get()))

    def escutar(self):
        if self.ocupado:
            return
        if not messagebox.askokcancel(
            "Microfone", "A fala será enviada ao Google para transcrição em português. "
            "Depois, você poderá revisar o texto antes de enviar ao ORION.\n\n"
            "Fale após confirmar. A captura dura no máximo cerca de 20 segundos.",
            parent=self.janela,
        ):
            return
        self.definir_ocupado(True, "●  Ouvindo… fale uma frase")
        self.trabalhos.put(("microfone", "", False))

    def executar_trabalhos(self):
        # Uma thread fixa serializa conversa e áudio; nenhum widget é acessado aqui.
        while True:
            trabalho = self.trabalhos.get()
            if trabalho is None:
                return
            tipo, texto, usar_voz = trabalho
            try:
                if tipo == "microfone":
                    from agentes.ferramentas.ouvido import ouvir
                    transcricao = ouvir()
                    self.eventos.put(("transcricao", transcricao))
                else:
                    resposta = self.sessao.responder(texto)
                    self.eventos.put(("resposta", resposta))
                    if usar_voz:
                        self.eventos.put(("estado", "●  Lendo resposta…"))
                        from agentes.ferramentas.voz import falar
                        if not falar(resposta):
                            self.eventos.put(("voz_falhou", "A voz não está disponível. A resposta está na tela."))
            except Exception as erro:
                from agentes.ferramentas.ouvido import ErroMicrofone
                if isinstance(erro, ErroMicrofone):
                    self.eventos.put(("aviso", str(erro)))
                else:
                    # Não mostra chaves, prompts ou detalhes de exceções de provedores.
                    self.eventos.put(("aviso", "Não consegui concluir esta operação. Verifique a configuração e tente novamente."))
            finally:
                self.eventos.put(("pronto", None))

    def receber_eventos(self):
        if self.fechado:
            return
        try:
            while True:
                tipo, valor = self.eventos.get_nowait()
                if tipo == "resposta":
                    self.mensagem("CR7 IA", valor)
                elif tipo == "transcricao":
                    if valor:
                        self.entrada.configure(state="normal")
                        # Preserva eventual rascunho já digitado.
                        if self.entrada.get("1.0", "end-1c").strip():
                            self.entrada.insert("end", "\n")
                        self.entrada.insert("end", valor)
                        self.mensagem("Sistema", "Fala transcrita. Revise o texto e clique em Enviar.")
                    else:
                        self.mensagem("Sistema", "Não entendi a fala. Tente novamente ou digite sua mensagem.")
                elif tipo in ("aviso", "voz_falhou"):
                    self.mensagem("Sistema", valor)
                    if tipo == "voz_falhou":
                        self.usar_voz.set(False)
                elif tipo == "estado":
                    self.estado.configure(text=valor)
                elif tipo == "pronto":
                    self.definir_ocupado(False)
        except queue.Empty:
            pass
        self.janela.after(80, self.receber_eventos)

    def atualizar_relogio(self):
        if not self.fechado:
            self.relogio.configure(text=datetime.now().strftime("%H:%M"))
            self.janela.after(1000, self.atualizar_relogio)

    def tela_cheia(self, evento=None):
        self.janela.attributes("-fullscreen", not self.janela.attributes("-fullscreen"))

    def fechar(self):
        if self.ocupado and not messagebox.askyesno(
            "Fechar ORION", "Há uma operação em andamento. Fechar pode interrompê-la. Deseja sair?",
            parent=self.janela,
        ):
            return
        self.fechado = True
        self.trabalhos.put(None)
        self.janela.destroy()


def main():
    # Os caminhos legados do núcleo são relativos à pasta do projeto.
    os.chdir(Path(__file__).resolve().parent)
    janela = tk.Tk()
    janela.withdraw()
    try:
        from config import PROVEDOR_LLM, USAR_LLM
        from core.banco import inicializar_banco
        from core.historico import carregar_historico
        from core.sessao_home import SessaoHome
        inicializar_banco()
        PainelHome(janela, SessaoHome(), carregar_historico(limite=20),
                   PROVEDOR_LLM if USAR_LLM else "desativado")
    except Exception:
        messagebox.showerror("ORION HOME", "Não foi possível iniciar o painel. "
                             "Confira as dependências e a configuração do projeto.", parent=janela)
        janela.destroy()
        raise
    janela.deiconify()
    janela.mainloop()


if __name__ == "__main__":
    main()
