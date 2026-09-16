"""
Fontes de live do ORION.

Plataformas iniciais:
- Twitch
- Kick
"""


def detectar_plataforma(url):
    url = str(url).lower().strip()

    if "twitch.tv" in url:
        return "twitch"

    if "kick.com" in url:
        return "kick"

    return None


def normalizar_perfil(jogo):
    jogo = str(jogo).lower().strip()

    aliases = {
        "ea fc 27": "eafc27",
        "fc 27": "eafc27",
        "eafc27": "eafc27",

        "gta 6": "gta6",
        "gta vi": "gta6",
        "gta6": "gta6",
    }

    return aliases.get(jogo)


def preparar_live(url, jogo):
    plataforma = detectar_plataforma(url)
    perfil = normalizar_perfil(jogo)

    if plataforma is None:
        return {
            "status": "plataforma_nao_suportada",
        }

    if perfil is None:
        return {
            "status": "jogo_nao_suportado",
            "plataforma": plataforma,
        }

    return {
        "status": "pronto",
        "plataforma": plataforma,
        "perfil": perfil,
        "url": url.strip(),
    }