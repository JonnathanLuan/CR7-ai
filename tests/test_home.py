"""Regressões: conversa real com SQLite temporário e falhas de áudio simuladas."""

import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from agentes.ferramentas import ouvido, voz


@pytest.fixture
def sessao(tmp_path, monkeypatch):
    import config
    from core import banco
    from core.sessao_home import SessaoHome
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(banco, "CAMINHO_BANCO", tmp_path / "teste.db")
    monkeypatch.setattr(config, "USAR_LLM", False)
    banco.inicializar_banco()
    return SessaoHome()


def test_conversa_memoria_e_historico(sessao):
    from core.historico import carregar_historico
    sessao.responder("meu nome e Teste")
    assert "Teste" in sessao.responder("qual meu nome")
    historico = carregar_historico()
    assert len(historico) == 2
    assert historico[0]["usuario"] == "meu nome e Teste"


def test_codigo_multilinha_preserva_fluxo(sessao):
    assert "Enviar" in sessao.responder("analise o codigo")
    resposta = sessao.responder("def dobro(x):\n    return x * 2")
    assert "Análise concluída" in resposta
    assert "dobro" in resposta
    assert not sessao.aguardando_codigo


def test_cancelar_codigo_e_mensagem_vazia(sessao):
    from core.historico import carregar_historico
    sessao.responder("   ")
    assert carregar_historico() == []
    sessao.responder("analise o codigo")
    assert "cancelada" in sessao.responder("cancelar")
    assert not sessao.aguardando_codigo


def test_sem_biblioteca_microfone(monkeypatch):
    monkeypatch.setitem(sys.modules, "speech_recognition", None)
    with pytest.raises(ouvido.ErroMicrofone, match="teclado"):
        ouvido.ouvir()


def biblioteca_falsa():
    return SimpleNamespace(
        Recognizer=Mock(), Microphone=Mock(),
        WaitTimeoutError=type("WaitTimeoutError", (Exception,), {}),
        UnknownValueError=type("UnknownValueError", (Exception,), {}),
        RequestError=type("RequestError", (Exception,), {}),
    )


def test_pyaudio_ausente_nao_vira_erro_fatal(monkeypatch):
    sr = biblioteca_falsa()
    sr.Microphone.side_effect = AttributeError("Could not find PyAudio")
    monkeypatch.setattr(ouvido, "_biblioteca", lambda: sr)
    for funcao in (ouvido.verificar_microfone, ouvido.ouvir):
        with pytest.raises(ouvido.ErroMicrofone, match="[Pp]yAudio"):
            funcao()


def test_silencio_e_falha_de_rede_sao_diferentes(monkeypatch):
    sr = biblioteca_falsa()
    sr.Microphone.return_value = Mock(__enter__=Mock(), __exit__=Mock(return_value=False))
    monkeypatch.setattr(ouvido, "_biblioteca", lambda: sr)
    sr.Recognizer.return_value.listen.side_effect = sr.WaitTimeoutError
    assert ouvido.ouvir() is None
    sr.Recognizer.return_value.listen.side_effect = None
    sr.Recognizer.return_value.recognize_google.side_effect = sr.RequestError
    with pytest.raises(ouvido.ErroMicrofone, match="internet"):
        ouvido.ouvir()


def test_transcricao_portugues(monkeypatch):
    sr = biblioteca_falsa()
    sr.Microphone.return_value = Mock(__enter__=Mock(), __exit__=Mock(return_value=False))
    sr.Recognizer.return_value.recognize_google.return_value = "bom dia"
    monkeypatch.setattr(ouvido, "_biblioteca", lambda: sr)
    assert ouvido.ouvir() == "bom dia"
    assert sr.Recognizer.return_value.operation_timeout == 10
    assert sr.Recognizer.return_value.recognize_google.call_args.kwargs["language"] == "pt-BR"


def test_tts_ausente_ou_quebrado_nao_encerra_programa(monkeypatch):
    monkeypatch.setattr(voz._estado, "motor", None, raising=False)
    monkeypatch.setitem(sys.modules, "pyttsx3", None)
    assert voz.falar("oi") is False
    motor = Mock()
    motor.runAndWait.side_effect = RuntimeError("motor indisponível")
    monkeypatch.setattr(voz, "configurar_motor", lambda: motor)
    assert voz.falar("oi") is False
