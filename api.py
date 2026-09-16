from fastapi import FastAPI
from pydantic import BaseModel

from config import NOME, VERSAO
from core.banco import inicializar_banco
from core.historico import registrar_conversa
from core.interpretador import interpretar


app = FastAPI(
    title="ORION API",
    version=VERSAO,
)


class MensagemRequest(BaseModel):
    mensagem: str


class MensagemResponse(BaseModel):
    resposta: str


inicializar_banco()


@app.get("/")
def inicio():
    return {
        "sistema": "ORION",
        "nome": NOME,
        "versao": VERSAO,
        "status": "online",
    }


@app.get("/status")
def status():
    return {
        "status": "online",
        "orion": NOME,
        "versao": VERSAO,
    }


@app.post("/mensagem", response_model=MensagemResponse)
def mensagem(dados: MensagemRequest):
    texto = dados.mensagem.strip()

    if not texto:
        return MensagemResponse(
            resposta="Nenhuma mensagem foi recebida."
        )

    resposta = interpretar(texto)

    registrar_conversa(
        texto,
        resposta,
    )

    return MensagemResponse(
        resposta=resposta
    )