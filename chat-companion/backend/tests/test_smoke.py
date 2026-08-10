"""Smoke tests do companion — sem rede, sem banco (adapter echo + memória).

Cobrem o fluxo (chat, histórico, capacidades), o gating progressivo e o
rate limit. Rodar:  cd chat-companion/backend && python -m pytest
"""

import os
import sys

os.environ.setdefault("LLM_ADAPTER", "echo")   # sem rede
os.environ.pop("DATABASE_URL", None)           # força MemoryStore
os.environ["RATE_LIMIT_MSGS"] = "3"
os.environ["RATE_LIMIT_WINDOW_S"] = "60"
os.environ["RATE_LIMIT_IP_FACTOR"] = "100"  # guarda por IP fora do caminho nos testes

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient  # noqa: E402

import capabilities  # noqa: E402
import app as appmod  # noqa: E402

client = TestClient(appmod.app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["store"] == "memory"


def test_chat_and_history():
    sid = "s-chat"
    r = client.post("/chat", json={"session_id": sid, "message": "olá", "chapter": 1,
                                   "mode": "progressivo"})
    assert r.status_code == 200
    body = r.json()
    assert "echo" in body["reply"]
    assert any(c["chave"] == "tutor" for c in body["capabilities_ativas"])
    h = client.get("/history", params={"session_id": sid}).json()["messages"]
    assert h[0]["role"] == "user" and h[-1]["role"] == "assistant"


def test_gating_progressive_hides_future_tools():
    # cap. 17 progressivo: RAG agêntico (cap. 18) ainda não ligou o loop -> sem tools
    assert capabilities.tools_ativas(17, "progressivo") == set()
    # cap. 18: loop + 'hora' + a busca já liberada no cap. 06
    assert {"hora", "buscar_no_livro"} <= capabilities.tools_ativas(18, "progressivo")
    # 'calcular' só no cap. 21 (avaliação)
    assert "calcular" not in capabilities.tools_ativas(18, "progressivo")
    assert "calcular" in capabilities.tools_ativas(21, "progressivo")
    # avançado libera tudo mesmo no cap. 0
    assert {"hora", "calcular", "buscar_no_livro"} <= capabilities.tools_ativas(0, "avancado")


def test_capabilities_endpoint():
    r = client.get("/capabilities", params={"chapter": 0, "mode": "progressivo"})
    j = r.json()
    assert j["loop_ativo"] is False
    ativos = {c["chave"] for c in j["capabilities"] if c["ativa"]}
    assert "tutor" in ativos and "rag_agentico" not in ativos


def test_rate_limit_429():
    sid = "s-rate"
    for _ in range(3):
        assert client.post("/chat", json={"session_id": sid, "message": "hi"}).status_code == 200
    # 4ª na janela estoura
    assert client.post("/chat", json={"session_id": sid, "message": "hi"}).status_code == 429


def test_byok_bypasses_rate_limit():
    sid = "s-byok"
    for _ in range(3):
        client.post("/chat", json={"session_id": sid, "message": "hi"})
    r = client.post("/chat", json={"session_id": sid, "message": "hi", "byok_key": "nvapi-x"})
    # BYOK isenta do limite do projeto; echo ignora a chave, mas não deve dar 429
    assert r.status_code == 200


def test_delete_session():
    sid = "s-del"
    client.post("/chat", json={"session_id": sid, "message": "oi"})
    client.delete(f"/session/{sid}")
    assert client.get("/history", params={"session_id": sid}).json()["messages"] == []


def test_suggestion_persists_and_lists():
    sid = "s-sug"
    r = client.post("/suggestion", json={"session_id": sid, "texto": "ótimo livro, o cap. 5 podia ter mais exemplos", "pagina": "14-persona-e-regras.html"})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True and body["email_enviado"] is False  # sem SMTP no teste
    # sem ADMIN_TOKEN -> 403
    assert client.get("/suggestions", params={"token": "x"}).status_code == 403


def test_suggestion_empty_400():
    assert client.post("/suggestion", json={"session_id": "s", "texto": "  "}).status_code == 400


def test_chat_stream_echo():
    """spec 047: o stream emite deltas e um done com a resposta completa,
    idêntica à que fica persistida no histórico."""
    import json
    sid = "t-stream"
    with client.stream("POST", "/chat/stream",
                       json={"session_id": sid, "message": "olá streaming"}) as r:
        assert r.status_code == 200
        assert r.headers["content-type"].startswith("text/event-stream")
        eventos = []
        for linha in r.iter_lines():
            if linha.startswith("data: "):
                eventos.append(json.loads(linha[6:]))
    deltas = [e["delta"] for e in eventos if "delta" in e]
    done = [e for e in eventos if e.get("done")]
    assert len(deltas) > 1, "deveria vir em mais de um pedaço"
    assert len(done) == 1
    assert "".join(deltas) == done[0]["reply"]
    hist = client.get("/history", params={"session_id": sid}).json()["messages"]
    assert hist[-1]["role"] == "assistant" and hist[-1]["content"] == done[0]["reply"]


def test_rate_limit_sobrevive_a_restart():
    """spec 049: o 429 por sessão vem do STORE (mensagens persistidas), não do
    deque em memória — limpar o deque (simulando deploy) não zera o limite."""
    sid = "t-rl-persistente"
    for i in range(3):  # RATE_LIMIT_MSGS = 3 nos testes
        r = client.post("/chat", json={"session_id": sid, "message": f"m{i}"})
        assert r.status_code == 200
    appmod._hits.clear()  # "restart" da instância
    r = client.post("/chat", json={"session_id": sid, "message": "m-extra"})
    assert r.status_code == 429


def test_debug_bastidores():
    """spec 053: /chat e o done do stream expõem o bloco debug (transparência)."""
    import json
    r = client.post("/chat", json={"session_id": "t-debug", "message": "o que é busca híbrida?"})
    d = r.json()["debug"]
    assert d["tokens_estimados"] > 0 and d["janela_tokens"] > 0
    assert d["historico_msgs"] >= 1 and isinstance(d["trechos"], list)
    assert "Tutor do livro" in d["capacidades_ativas"]

    with client.stream("POST", "/chat/stream",
                       json={"session_id": "t-debug2", "message": "e o reranking?"}) as r:
        eventos = [json.loads(l[6:]) for l in r.iter_lines() if l.startswith("data: ")]
    done = [e for e in eventos if e.get("done")][0]
    assert done["debug"]["tokens_estimados"] > 0


def test_consent_telemetria_objetivo():
    """spec 054: aceite gravado; telemetria só com consentimento; objetivo
    persiste, aparece no GET e entra como camada do system prompt (debug)."""
    sid = "t-054"
    # telemetria ANTES do aceite: não grava
    r = client.post("/telemetry", json={"session_id": sid, "slug": "02-anatomia-do-sistema"})
    assert r.json()["ok"] is False
    # aceite
    r = client.post("/consent", json={"session_id": sid, "versao": "v1"})
    assert r.json()["ok"] is True
    # telemetria depois: grava
    r = client.post("/telemetry", json={"session_id": sid, "slug": "02-anatomia-do-sistema"})
    assert r.json()["ok"] is True
    # resumo exige token
    assert client.get("/telemetry").status_code == 403
    # objetivo
    r = client.post("/objetivo", json={"session_id": sid, "texto": "construir um RAG sobre a documentação do meu ERP"})
    assert r.json()["ok"] is True
    assert client.get("/objetivo", params={"session_id": sid}).json()["objetivo"].startswith("construir")
    # camada no prompt: via debug do /chat
    d = client.post("/chat", json={"session_id": sid, "message": "por onde começo?"}).json()["debug"]
    assert d["objetivo"].startswith("construir")
    # e o system prompt de fato contém a camada
    assert "Objetivo declarado do leitor" in appmod._system_prompt(6, "progressivo", [], "x")


def test_telemetry_publico_agregado():
    """spec 055: projeção pública só tem agregados — nada de sessões/timestamps."""
    sid = "t-055"
    client.post("/consent", json={"session_id": sid, "versao": "v1"})
    for slug in ("02-anatomia-do-sistema", "02-anatomia-do-sistema", "glossario"):
        client.post("/telemetry", json={"session_id": sid, "slug": slug})
    d = client.get("/telemetry/publico").json()
    assert d["total"] >= 3 and d["paginas_distintas"] >= 2
    assert d["por_pagina"].get("02-anatomia-do-sistema", 0) >= 2
    assert set(d.keys()) == {"total", "paginas_distintas", "por_pagina"}  # nada além do agregado


def test_bm25_paridade_com_rag_zero():
    """O companion reimplementa o BM25 do `rag-zero` — e isso vira contrato.

    O livro afirma que este serviço usa "o mesmo BM25 (*Best Matching 25*) Okapi
    da etapa 5". Até a edição 0.4 a afirmação era falsa e ninguém percebeu,
    porque nada a verificava (ADR 0010). Este teste é o portão: se a
    reimplementação divergir da canônica, ele quebra — e obriga ou a corrigir o
    código, ou a enfraquecer a frase.
    """
    import sys
    from pathlib import Path

    raiz = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(raiz / "rag-zero"))
    from rag_zero.bm25 import BM25
    from ragindex import BookIndex, _norm

    corpus = [
        "O código de erro ERR_4021 indica falha de autenticação no gateway.",
        "Automóveis elétricos reduzem emissão em áreas urbanas densas.",
        "O prazo de garantia do produto XR-4400-B é de 24 meses.",
        "Veículos de passeio movidos a bateria exigem recarga frequente.",
        "A autenticação do gateway usa token de curta duração.",
    ]

    indice = BookIndex.__new__(BookIndex)          # sem tocar em disco
    indice.blocos = [{"fonte": f"f{i}.md", "titulo": "t", "texto": t,
                      "termos": _norm(t)} for i, t in enumerate(corpus)]
    indice._indexar()

    canonico = BM25(corpus)
    for consulta in ("autenticação gateway", "veículos elétricos bateria",
                     "ERR_4021", "prazo de garantia"):
        esperado = [r.indice for r in canonico.buscar(consulta, 3)]
        obtido = [int(r["fonte"][1:-3]) for r in indice.buscar(consulta, 3)]
        assert obtido == esperado, (
            f"divergência em '{consulta}': companion={obtido} rag-zero={esperado}")
