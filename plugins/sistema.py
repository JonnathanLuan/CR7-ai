import subprocess
import webbrowser


PROGRAMAS = {
    "bloco de notas": "notepad",
    "notepad": "notepad",

    "calculadora": "calc",

    "paint": "mspaint",

    "explorador de arquivos": "explorer",
    "explorador": "explorer",
    "arquivos": "explorer",

    "prompt de comando": "cmd",
    "cmd": "cmd",

    "powershell": "powershell",

    "edge": "msedge",
    "microsoft edge": "msedge",

    "chrome": "chrome",
    "google chrome": "chrome",

    "visual studio code": "code",
    "vs code": "code",
    "vscode": "code",
}


SITES = {
    "youtube": "https://www.youtube.com",
    "netflix": "https://www.netflix.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
    "gmail": "https://mail.google.com",
}


def abrir_programa(nome):
    nome = nome.lower().strip()

    # ==========================================
    # SITES
    # ==========================================

    if nome in SITES:
        try:
            webbrowser.open(SITES[nome])
            return True
        except Exception:
            return False

    # ==========================================
    # PROGRAMAS
    # ==========================================

    comando = PROGRAMAS.get(nome)

    if not comando:
        return False

    try:
        subprocess.Popen(
            comando,
            shell=True,
        )

        return True

    except Exception:
        return False