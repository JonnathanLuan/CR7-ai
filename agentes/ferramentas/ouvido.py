"""Entrada por voz do ORION.

A importação é feita somente quando o microfone é usado. Assim, o restante do
assistente continua funcionando mesmo sem SpeechRecognition ou PyAudio.
"""

from importlib import import_module


class ErroMicrofone(RuntimeError):
    """Erro recuperável de configuração ou acesso ao reconhecimento de voz."""


def _biblioteca():
    """Carrega SpeechRecognition ou orienta o uso do teclado."""
    try:
        return import_module("speech_recognition")
    except (ImportError, ModuleNotFoundError) as erro:
        raise ErroMicrofone(
            "O reconhecimento de voz não está instalado. Continue usando o teclado."
        ) from erro


def _erro_dispositivo(erro):
    """Converte falhas técnicas do dispositivo em uma mensagem compreensível."""
    if "pyaudio" in str(erro).lower():
        return ErroMicrofone(
            "O PyAudio não está instalado ou não pôde acessar o microfone. "
            "Continue usando o teclado."
        )
    return ErroMicrofone(
        "Não foi possível acessar o microfone. Verifique o dispositivo "
        "ou continue usando o teclado."
    )


def verificar_microfone():
    """Confirma se a biblioteca e o dispositivo de entrada estão disponíveis."""
    sr = _biblioteca()
    try:
        with sr.Microphone():
            pass
    except (AttributeError, OSError) as erro:
        raise _erro_dispositivo(erro) from erro
    return True


def ouvir(timeout=5, frase_maxima=15):
    """Escuta uma frase e devolve sua transcrição em português do Brasil.

    Silêncio ou fala incompreensível retornam None. Problemas de instalação,
    dispositivo ou internet geram ErroMicrofone para a interface informar o
    usuário sem encerrar o ORION.
    """
    sr = _biblioteca()
    reconhecedor = sr.Recognizer()
    reconhecedor.operation_timeout = 10

    try:
        with sr.Microphone() as fonte:
            print("🎙 Ouvindo... pode falar.")
            reconhecedor.adjust_for_ambient_noise(fonte, duration=0.5)
            audio = reconhecedor.listen(
                fonte,
                timeout=timeout,
                phrase_time_limit=frase_maxima,
            )
    except sr.WaitTimeoutError:
        return None
    except (AttributeError, OSError) as erro:
        raise _erro_dispositivo(erro) from erro

    try:
        return reconhecedor.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        return None
    except sr.RequestError as erro:
        raise ErroMicrofone(
            "Não foi possível acessar o reconhecimento de voz pela internet. "
            "Verifique sua conexão ou continue usando o teclado."
        ) from erro
