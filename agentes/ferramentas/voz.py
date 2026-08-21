import pyttsx3


def configurar_motor():
    """Cria e configura o motor de voz do CR7."""

    motor = pyttsx3.init()
    vozes = motor.getProperty("voices")

    for voz in vozes:
        if "PT-BR" in voz.id.upper() or "PORTUGUESE" in voz.name.upper():
            motor.setProperty("voice", voz.id)
            break

    motor.setProperty("rate", 180)
    motor.setProperty("volume", 1.0)

    return motor


def falar(texto):
    """Transforma um texto em fala usando uma voz em português."""

    motor = configurar_motor()
    motor.say(str(texto))
    motor.runAndWait()


def listar_vozes():
    """Mostra as vozes instaladas no computador."""

    motor = pyttsx3.init()
    vozes = motor.getProperty("voices")

    print("\nVozes disponíveis:\n")

    for indice, voz in enumerate(vozes):
        print(f"Índice: {indice}")
        print(f"Nome: {voz.name}")
        print(f"ID: {voz.id}")
        print("-" * 40)


if __name__ == "__main__":
    falar("Siiiiuuuuu! Agora estou usando uma voz em português do Brasil.")