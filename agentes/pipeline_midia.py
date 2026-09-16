"""
Pipeline de mídia do ORION.

Fluxo rápido:
Transcrição -> Observador -> Editor rápido

Perfis iniciais:
- eafc27
- gta6
"""

from agentes.observador import analisar_segmentos
from agentes.editor import preparar_cortes


PERFIS_SUPORTADOS = (
    "eafc27",
    "gta6",
)


def analisar_e_preparar(
    segmentos,
    perfil="eafc27",
):
    """
    Analisa uma transcrição e prepara
    os melhores cortes rapidamente.
    """

    if perfil not in PERFIS_SUPORTADOS:
        return {
            "status": "perfil_invalido",
            "perfil": perfil,
            "destaques": [],
            "cortes": [],
        }

    if not segmentos:
        return {
            "status": "sem_conteudo",
            "perfil": perfil,
            "destaques": [],
            "cortes": [],
        }

    destaques = analisar_segmentos(
        segmentos,
        perfil=perfil,
    )

    if not destaques:
        return {
            "status": "sem_destaques",
            "perfil": perfil,
            "destaques": [],
            "cortes": [],
        }

    cortes = preparar_cortes(
        destaques
    )

    cortes_validos = [
        corte
        for corte in cortes
        if corte.get("status")
        == "pronto_para_corte"
    ]

    return {
        "status": "pronto",
        "perfil": perfil,
        "editor": "rapido",
        "quantidade_destaques": len(
            destaques
        ),
        "quantidade_cortes": len(
            cortes_validos
        ),
        "destaques": destaques,
        "cortes": cortes_validos,
    }