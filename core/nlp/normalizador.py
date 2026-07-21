import re
import unicodedata


def remover_acentos(texto):
    texto_normalizado = unicodedata.normalize("NFD", texto)

    return "".join(
        caractere
        for caractere in texto_normalizado
        if unicodedata.category(caractere) != "Mn"
    )


def normalizar(texto):
    """
    Normaliza um texto para facilitar o entendimento da ORION.
    """

    if not isinstance(texto, str):
        return ""

    texto = texto.lower()
    texto = remover_acentos(texto)
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    texto = texto.strip()

    return texto