from plugins import sistema


PLUGINS = {
    "sistema": sistema,
}


def executar_plugin(plugin, funcao, *args):
    """
    Executa uma função de um plugin.
    """

    if plugin not in PLUGINS:
        return None

    modulo = PLUGINS[plugin]

    if not hasattr(modulo, funcao):
        return None

    metodo = getattr(modulo, funcao)

    return metodo(*args)