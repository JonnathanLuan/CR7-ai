"""Saída de voz do ORION com falha segura quando o TTS não está disponível."""

from importlib import import_module
from types import SimpleNamespace


_estado = SimpleNamespace(motor=None)


def _biblioteca():
    """Carrega pyttsx3 somente quando a saída de voz é solicitada."""
    try:
        return import_module("pyttsx3")
    except (ImportError, ModuleNotFoundError):
        return None


def configurar_motor():
    """Cria e configura o motor de voz do ORION."""
    if _estado.motor is not None:
        return _estado.motor

    pyttsx3 = _biblioteca()
    if pyttsx3 is None:
        return None

    try:
        motor = pyttsx3.init()
        vozes = motor.getProperty("voices") or []

        for voz_disponivel in vozes:
            nome = str(getattr(voz_disponivel, "name", "")).upper()
            identificador = str(getattr(voz_disponivel, "id", "")).upper()
            idiomas = str(getattr(voz_disponivel, "languages", "")).upper()
            descricao = f"{nome} {identificador} {idiomas}"
            if any(marcador in descricao for marcador in ("PT-BR", "PORTUGUESE", "BRAZIL")):
                motor.setProperty("voice", voz_disponivel.id)
                break

        motor.setProperty("rate", 180)
        motor.setProperty("volume", 1.0)
        _estado.motor = motor
        return motor
    except Exception:
        _estado.motor = None
        return None


def falar(texto):
    """Lê o texto em voz alta e retorna False se o TTS estiver indisponível."""
    try:
        motor = configurar_motor()
        if motor is None:
            return False
        motor.say(str(texto))
        motor.runAndWait()
        return True
    except Exception:
        _estado.motor = None
        return False


def listar_vozes():
    """Mostra as vozes instaladas e devolve a lista encontrada."""
    motor = configurar_motor()
    if motor is None:
        print("Nenhuma voz está disponível.")
        return []

    vozes = motor.getProperty("voices") or []
    print("\nVozes disponíveis:\n")
    for indice, voz_disponivel in enumerate(vozes):
        print(f"Índice: {indice}")
        print(f"Nome: {voz_disponivel.name}")
        print(f"ID: {voz_disponivel.id}")
        print("-" * 40)
    return vozes


if __name__ == "__main__":
    falar("Olá! Eu sou o ORION e agora estou usando uma voz em português do Brasil.")
