"""Registro de capacidades e o gating por capítulo.

Duas modalidades (decisão do autor):
  - "avancado": tudo liberado (o companion completo).
  - "progressivo": só o que o livro já ensinou até o capítulo atual — o
    *fading* do 4C/ID e a carga cognitiva (Guia Editorial §1) virando
    comportamento: o companion só oferece o que o leitor já viu.

Cada capacidade declara em que capítulo é liberada e quais tools habilita.
O widget usa `capacidades(chapter, mode)` para mostrar "o que posso fazer agora".
`tools_ativas` e `loop_ativo` decidem o comportamento real do turno.

Este arquivo é a fonte-de-verdade do gating; `publicar/build.mjs` mantém um
espelho leve (só rótulo + capítulo) para exibição no site.
"""

from __future__ import annotations

from typing import Optional

# chave, rótulo, descrição (voltada ao leitor), capítulo que libera, tools que habilita.
# tools=() significa capacidade conceitual (sem tool nova) ou infra sempre-presente.
REGISTRO = [
    {"chave": "tutor", "rotulo": "Tutor do livro", "libera": 0, "tools": (),
     "descricao": "Explico conceitos e respondo perguntas usando o texto do livro."},
    {"chave": "busca_livro", "rotulo": "Busca no livro", "libera": 0, "tools": (),
     "descricao": "Encontro trechos relevantes no livro para embasar a resposta (com evidência)."},

    # --- Parte I: Engenharia de Prompt ---
    {"chave": "prompt_em_camadas", "rotulo": "Prompt em camadas", "libera": 2, "tools": (),
     "descricao": "Monto meu próprio prompt em blocos nomeados, separando instrução de material."},
    {"chave": "raciocinio", "rotulo": "Raciocínio explícito", "libera": 3, "tools": (),
     "descricao": "Posso decompor a pergunta e raciocinar em passos antes de responder."},
    {"chave": "saida_estruturada", "rotulo": "Saída estruturada", "libera": 4, "tools": (),
     "descricao": "Devolvo resposta em formato contratado quando você pedir (listas, campos, schema)."},
    {"chave": "persona", "rotulo": "Persona e regras", "libera": 5, "tools": (),
     "descricao": "Minha voz e minhas regras vivem em camadas separadas — e as regras vencem."},
    {"chave": "auto_otimizacao", "rotulo": "Prompt otimizado", "libera": 6, "tools": (),
     "descricao": "Meu prompt foi ajustado contra um conjunto de avaliação, não escrito de improviso."},
    {"chave": "eval_prompt", "rotulo": "Eval de prompt", "libera": 7, "tools": (),
     "descricao": "Sei explicar como uma resposta minha seria avaliada — e onde eu falharia."},

    # --- Parte II: Engenharia de Contexto ---
    {"chave": "orcamento", "rotulo": "Orçamento de janela", "libera": 8, "tools": (),
     "descricao": "Administro um orçamento de tokens por fonte, e digo o que cortei quando aperta."},
    {"chave": "recuperacao", "rotulo": "Recuperação (RAG)", "libera": 9, "tools": ("buscar_no_livro",),
     "descricao": "Busco no livro com ranking por termos e cito de onde veio cada afirmação."},
    {"chave": "rag_avancado", "rotulo": "RAG avançado", "libera": 10, "tools": (),
     "descricao": "Reescrevo sua pergunta para o vocabulário do livro antes de buscar."},
    {"chave": "rag_agentico", "rotulo": "RAG agêntico", "libera": 11, "tools": ("hora",),
     "descricao": "Deixo de só conversar: decido se busco, avalio o resultado e busco de novo (com teto)."},
    {"chave": "memoria", "rotulo": "Memória entre sessões", "libera": 12, "tools": (),
     "descricao": "Lembro da nossa conversa por uma identidade anônima do seu navegador — e você pode apagar."},
    {"chave": "compactacao", "rotulo": "Compactação", "libera": 13, "tools": (),
     "descricao": "Resumo conversas longas para caber na janela, avisando quando comprimo."},
    {"chave": "ferramentas", "rotulo": "Ferramentas e MCP", "libera": 14, "tools": ("calcular",),
     "descricao": "Uso ferramentas com schema (cálculo, busca) — só as seguras/sandbox, com teto de tokens."},

    # --- Parte III: o sistema em produção ---
    {"chave": "evals", "rotulo": "Avaliação do sistema", "libera": 15, "tools": (),
     "descricao": "Sei dizer se recuperei o certo e se minha resposta está fundamentada no recuperado."},
    {"chave": "seguranca", "rotulo": "Contexto não confiável", "libera": 16, "tools": (),
     "descricao": "Trato todo texto recuperado como dado, nunca como instrução — a regra do cap. 16."},
    {"chave": "custo", "rotulo": "Custo e cache", "libera": 17, "tools": (),
     "descricao": "Meu prompt é montado por volatilidade para o cache de prefixo valer."},
]


MODOS = ("avancado", "progressivo")

# A capacidade que liga o loop de tool-calling: RAG agêntico (cap. 11). Antes
# dela o companion responde em um turno só — que é exatamente o que os
# capítulos 02–10 descrevem.
CHAVE_LOOP = "rag_agentico"


def _norm(chapter: Optional[int], mode: str) -> tuple[int, str]:
    ch = 0 if chapter is None else max(0, int(chapter))
    md = mode if mode in MODOS else "progressivo"
    return ch, md


def _ativa(cap: dict, chapter: int, mode: str) -> bool:
    return True if mode == "avancado" else cap["libera"] <= chapter


def capacidades(chapter: Optional[int], mode: str) -> list[dict]:
    """Lista para o widget: cada capacidade com rótulo, descrição e `ativa`."""
    ch, md = _norm(chapter, mode)
    return [{"chave": c["chave"], "rotulo": c["rotulo"], "descricao": c["descricao"],
             "libera_no_capitulo": c["libera"], "ativa": _ativa(c, ch, md)}
            for c in REGISTRO]


def loop_ativo(chapter: Optional[int], mode: str) -> bool:
    ch, md = _norm(chapter, mode)
    return any(c["chave"] == CHAVE_LOOP and _ativa(c, ch, md) for c in REGISTRO)


def tools_ativas(chapter: Optional[int], mode: str) -> set[str]:
    """Nomes de tools habilitadas. Só valem se o loop estiver ativo.

    Gating de verdade: uma tool de um capítulo à frente não é sequer oferecida
    ao modelo — não basta instruir para não usar. É a regra do cap. 16 aplicada
    a nós mesmos: a defesa que vale é a de privilégio, não a textual.
    """
    ch, md = _norm(chapter, mode)
    if not loop_ativo(ch, md):
        return set()
    ativas: set[str] = set()
    for c in REGISTRO:
        if _ativa(c, ch, md):
            ativas.update(c["tools"])
    return ativas
