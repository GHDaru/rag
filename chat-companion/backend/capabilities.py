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
    {"chave": "arquitetura", "rotulo": "Mapa dos componentes", "libera": 2, "tools": (),
     "descricao": "Sei situar qualquer técnica no componente do sistema que ela aprofunda."},
    {"chave": "topologia", "rotulo": "Arquiteturas de referência", "libera": 3, "tools": (),
     "descricao": "Reconheço em que degrau um sistema está — naive, advanced, modular ou agêntico."},
    {"chave": "corpus", "rotulo": "Corpus curado", "libera": 4, "tools": (),
     "descricao": "Meu índice sabe de onde veio cada trecho e em que seção — procedência, não só similaridade."},
    {"chave": "chunking", "rotulo": "Corte e representação", "libera": 5, "tools": (),
     "descricao": "A unidade que busco não é necessariamente a que entrego."},
    {"chave": "busca", "rotulo": "Busca híbrida", "libera": 6, "tools": ("buscar_no_livro",),
     "descricao": "Combino busca por termo e por similaridade — e cito de onde veio cada afirmação."},
    {"chave": "reranking", "rotulo": "Reranking", "libera": 7, "tools": (),
     "descricao": "Reordeno os candidatos e uso a nota para decidir quantos valem o contexto."},
    {"chave": "consulta", "rotulo": "Entendimento da consulta", "libera": 8, "tools": (),
     "descricao": "Reescrevo sua pergunta para o vocabulário do livro antes de buscar."},
    {"chave": "avancada", "rotulo": "Recuperação avançada", "libera": 9, "tools": (),
     "descricao": "Cada trecho do índice carrega o contexto de onde foi tirado."},
    {"chave": "estruturada", "rotulo": "Pergunta global", "libera": 10, "tools": (),
     "descricao": "Respondo perguntas sobre o conjunto do livro, não só sobre trechos."},
    {"chave": "fundamentacao", "rotulo": "Geração fundamentada", "libera": 15, "tools": (),
     "descricao": "Respondo só com base no que recuperei — e digo quando não encontrei."},
    {"chave": "rag_agentico", "rotulo": "RAG agêntico", "libera": 18, "tools": ("hora",),
     "descricao": "Decido se busco, avalio o resultado e busco de novo — com teto de iterações."},
    {"chave": "conversacional", "rotulo": "RAG conversacional", "libera": 19, "tools": (),
     "descricao": "Resolvo referências entre turnos e evito repetir trechos que já mostrei."},
    {"chave": "orcamento", "rotulo": "Orçamento de janela", "libera": 20, "tools": (),
     "descricao": "Administro quanto do contexto vale gastar com trechos recuperados."},
    {"chave": "evals", "rotulo": "Avaliação do sistema", "libera": 21, "tools": ("calcular",),
     "descricao": "Sei dizer se recuperei o certo e se minha resposta está fundamentada nele."},
    {"chave": "seguranca", "rotulo": "Corpus não confiável", "libera": 22, "tools": (),
     "descricao": "Trato todo texto recuperado como dado, nunca como instrução — a regra do cap. 22."},
    {"chave": "custo", "rotulo": "Custo e cache", "libera": 23, "tools": (),
     "descricao": "Meu prompt é montado por volatilidade para o cache de prefixo valer."},
]


MODOS = ("avancado", "progressivo")

# A capacidade que liga o loop de tool-calling: RAG agêntico (cap. 18). Antes
# dela o companion responde em um turno só — que é o pipeline fixo dos caps.
# 02–17.
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
    ao modelo — não basta instruir para não usar. É a regra do cap. 22 aplicada
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
