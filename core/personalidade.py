import random


RESP_APRENDEU = [
    "Entendido. Vou lembrar disso.",
    "Informação registrada.",
    "Aprendi mais uma coisa sobre você.",
    "Perfeito. Isso ficará na minha memória.",
    "Agora sei disso.",
    "Certo! Informação salva."
]


RESP_NAO_SEI = [
    "Ainda não sei responder isso.",
    "Essa informação ainda não faz parte da minha memória.",
    "Ainda estou aprendendo sobre esse assunto.",
    "Não encontrei essa informação.",
    "Posso aprender isso no futuro."
]


RESP_SAUDACAO = [
    "Olá!",
    "Oi!",
    "Olá! Como posso ajudar?",
    "É bom falar com você novamente.",
    "Estou pronta para ajudar."
]


def resposta_aprendeu():
    return random.choice(RESP_APRENDEU)


def resposta_nao_sei():
    return random.choice(RESP_NAO_SEI)


def resposta_saudacao():
    return random.choice(RESP_SAUDACAO)