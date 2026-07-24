import pyttsx3


def falar(texto):
    """Transforma um texto em fala usando a voz do sistema."""

    motor = pyttsx3.init()

    motor.setProperty("rate", 180)
    motor.setProperty("volume", 1.0)

    motor.say(texto)
    motor.runAndWait()


if __name__ == "__main__":
    falar("Siiiiuuuuu! CR7 IA iniciado com sucesso!")