import subprocess


PROGRAMAS = {
    "bloco de notas": "notepad",
    "notepad": "notepad",
    "calculadora": "calc",
    "paint": "mspaint",
}


def abrir_programa(nome):
    nome = nome.lower().strip()

    if nome not in PROGRAMAS:
        return False

    try:
        subprocess.Popen(PROGRAMAS[nome])
        return True
    except Exception:
        return False