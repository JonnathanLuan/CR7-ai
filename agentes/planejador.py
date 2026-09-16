"""
Agente Planejador do ORION.

Planejamentos comuns são feitos localmente
para manter a resposta rápida.
"""

import re


def _normalizar(texto):
    return " ".join(
        str(texto).lower().strip().split()
    )


def _plano_python():
    return (
        "Plano de Python para esta semana. "
        "Segunda: variáveis, tipos de dados e operadores. "
        "Terça: condições com if, elif e else. "
        "Quarta: laços for e while. "
        "Quinta: funções e exercícios práticos. "
        "Sexta: crie um pequeno programa usando o que estudou."
    )


def _plano_flutter():
    return (
        "Plano de Flutter para esta semana. "
        "Segunda: estrutura de um projeto Flutter e widgets básicos. "
        "Terça: Row, Column, Container e organização de layout. "
        "Quarta: botões, campos e interação com o usuário. "
        "Quinta: navegação entre telas e gerenciamento de estado básico. "
        "Sexta: crie uma pequena interface completa para praticar."
    )


def _plano_estudo_generico(assunto):
    return (
        f"Plano de estudos de {assunto}. "
        "Dia 1: revise os fundamentos do assunto. "
        "Dia 2: estude os principais conceitos e faça anotações. "
        "Dia 3: resolva exercícios práticos. "
        "Dia 4: revise os pontos em que teve dificuldade. "
        "Dia 5: faça uma atividade ou pequeno projeto para aplicar o conteúdo."
    )


def _extrair_assunto(pedido):
    padroes = [
        r"estudos? de (.+?)(?: para| nesta| essa| durante|$)",
        r"estudar (.+?)(?: para| nesta| essa| durante|$)",
        r"aprender (.+?)(?: para| nesta| essa| durante|$)",
    ]

    for padrao in padroes:
        resultado = re.search(
            padrao,
            pedido,
            re.IGNORECASE,
        )

        if resultado:
            return resultado.group(1).strip()

    return None


def executar(intencao, dados=None):
    """
    Executa planejamentos rápidos sem consultar IA.
    """

    dados = dados or {}

    if intencao != "planejar":
        return "Não reconheci essa solicitação de planejamento."

    pedido = dados.get("pedido", "").strip()

    if not pedido:
        return "O que você gostaria que eu planejasse?"

    texto = _normalizar(pedido)

    # ------------------------------------------
    # ESTUDOS DE PYTHON
    # ------------------------------------------

    if "python" in texto:
        return _plano_python()

    # ------------------------------------------
    # ESTUDOS DE FLUTTER
    # ------------------------------------------

    if "flutter" in texto:
        return _plano_flutter()

    # ------------------------------------------
    # OUTROS ESTUDOS
    # ------------------------------------------

    if (
        "estudo" in texto
        or "estudar" in texto
        or "aprender" in texto
    ):
        assunto = _extrair_assunto(pedido)

        if assunto:
            return _plano_estudo_generico(assunto)

        return (
            "Posso organizar seus estudos. "
            "Diga apenas qual assunto você quer estudar."
        )

    # ------------------------------------------
    # ROTINA
    # ------------------------------------------

    if "rotina" in texto:
        return (
            "Sugestão de rotina. "
            "Primeiro, organize as tarefas mais importantes. "
            "Depois, reserve um período de foco sem interrupções. "
            "Faça uma pausa curta. "
            "Em seguida, conclua as tarefas menores. "
            "No fim do dia, revise o que foi realizado."
        )

    # ------------------------------------------
    # PLANO GENÉRICO
    # ------------------------------------------

    return (
        "Posso montar esse planejamento rapidamente. "
        "Diga o objetivo principal e o período disponível."
    )