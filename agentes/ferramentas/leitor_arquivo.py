from pathlib import Path


def ler_arquivo(caminho):
    """
    Lê um arquivo de texto e retorna seu conteúdo.
    """

    caminho = Path(caminho)

    if not caminho.exists():
        return None

    if not caminho.is_file():
        return None

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return arquivo.read()

    except Exception:
        return None 