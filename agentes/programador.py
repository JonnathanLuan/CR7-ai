def executar(intencao, dados=None):

    if intencao == "analisar_codigo":
        return (
            "Posso analisar seu código, encontrar problemas, "
            "sugerir melhorias e explicar cada parte."
        )

    return (
        "Sou o agente Programador, mas ainda não sei executar "
        "essa solicitação."
    )