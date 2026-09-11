from core.ferramentas.registro import registro
from tools.builtin import registrar_ferramentas_nativas
registrar_ferramentas_nativas()
from core.router import router
from core.runtime import ContextoExecucao, ResultadoExecucao
from core.security import validar_mensagem
from core.decisor import decidir


def test_contexto_execucao_tem_ids():
    contexto = ContextoExecucao("teste")
    assert contexto.sessao_id
    assert contexto.execucao_id
    assert contexto.mensagem == "teste"


def test_resultado_padronizado():
    resultado = ResultadoExecucao.ok("ok", dados={"x": 1})
    assert resultado.sucesso is True
    assert resultado.dados["x"] == 1


def test_registro_tem_ferramentas_nativas():
    nomes = {f.nome for f in registro.listar()}
    assert {"adicionar_tarefa", "buscar_na_internet", "analisar_codigo"}.issubset(nomes)


def test_router_preserva_decisao_de_regras():
    rota = router.rotear("qual meu nome")
    assert rota.tipo == "memoria"
    assert rota.confianca > 0.9


def test_decisor_vazio():
    assert decidir("").tipo == "vazio"


def test_guardrail():
    assert validar_mensagem("").sucesso is False
    assert validar_mensagem("oi").sucesso is True


def test_llm_manager_seleciona_provedor():
    from core.llm.manager import LLMManager
    from core.llm.providers import LLMProvider

    class Falso(LLMProvider):
        nome = "falso"
        def disponivel(self):
            return True
        def gerar(self, comando):
            return "ok"

    gerente = LLMManager()
    gerente.registrar(Falso())
    assert gerente.obter("falso").gerar("oi") == "ok"
