"""
Reconhecimento de fala da ORION (entrada por voz).

Usa a biblioteca SpeechRecognition com o motor gratuito do
Google para transcrever fala em português do Brasil.

Requer um microfone e a lib `PyAudio` instalada no sistema
(no Windows, `pip install pyaudio` costuma bastar; no
Linux, pode ser necessário instalar o pacote `portaudio19-dev`
antes com o gerenciador de pacotes do sistema).
"""

import speech_recognition as sr

RECONHECEDOR = sr.Recognizer()


def ouvir(timeout=5, frase_maxima=15):
    """
    Ativa o microfone, escuta o usuário e devolve o texto
    transcrito em português. Retorna None se não entender
    nada ou se o tempo limite expirar.
    """

    try:
        with sr.Microphone() as fonte:
            print("🎙 Ouvindo... pode falar.")
            RECONHECEDOR.adjust_for_ambient_noise(fonte, duration=0.5)
            audio = RECONHECEDOR.listen(
                fonte, timeout=timeout, phrase_time_limit=frase_maxima
            )

    except sr.WaitTimeoutError:
        return None
    except OSError:
        # Nenhum microfone disponível no sistema
        return None

    try:
        return RECONHECEDOR.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None
