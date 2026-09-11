import re
import unicodedata
from datetime import datetime, timedelta


def _sem_acentos(texto):
    return "".join(
        caractere
        for caractere in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caractere) != "Mn"
    )


def extrair_lembrete(frase):
    """
    Entende lembretes simples em linguagem natural.

    Exemplos:
        CR7, me lembre hoje às 19h de estudar Python.
        Me lembre amanhã às 08:30 de ligar para João.
        Me lembre de estudar Python hoje às 19h.
    """

    agora = datetime.now()

    texto = _sem_acentos(frase.lower())
    texto = re.sub(r"[,.!?;]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    if "me lembre" not in texto and "me lembra" not in texto:
        return None

    # -------------------------
    # DIA
    # -------------------------

    if re.search(r"\bamanha\b", texto):
        dia = (agora + timedelta(days=1)).date()

    elif re.search(r"\bhoje\b", texto):
        dia = agora.date()

    else:
        return None

    # -------------------------
    # HORÁRIO
    # -------------------------

    resultado_hora = re.search(
        r"\b(?:as\s+)?(\d{1,2})(?:(?:h|:)\s*(\d{1,2})?)?\b",
        texto,
    )

    if not resultado_hora:
        return None

    hora = int(resultado_hora.group(1))
    minuto = int(resultado_hora.group(2) or 0)

    if not (0 <= hora <= 23 and 0 <= minuto <= 59):
        return None

    # -------------------------
    # DESCRIÇÃO
    # -------------------------

    restante = texto[resultado_hora.end():].strip()

    resultado_descricao = re.search(
        r"^de\s+(.+)$",
        restante,
    )

    if resultado_descricao:
        descricao = resultado_descricao.group(1)

    else:
        # Exemplo:
        # me lembre de estudar python hoje as 19h

        alternativo = re.search(
            r"me lembr[ea]\s+de\s+(.+?)\s+"
            r"(?:hoje|amanha)\s+"
            r"(?:as\s+)?\d{1,2}"
            r"(?:(?:h|:)\s*\d{0,2})?$",
            texto,
        )

        if not alternativo:
            return None

        descricao = alternativo.group(1)

    descricao = descricao.strip(" .!?")

    if not descricao:
        return None

    lembrar_em = datetime.combine(
        dia,
        datetime.min.time(),
    ).replace(
        hour=hora,
        minute=minuto,
    )

    return {
        "descricao": descricao,
        "lembrar_em": lembrar_em.strftime("%Y-%m-%d %H:%M:%S"),
    }