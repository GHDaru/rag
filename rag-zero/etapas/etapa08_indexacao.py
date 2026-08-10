"""Etapa 8 — indexação refinada: as duas curas lado a lado (cap. 09).

    python3 etapas/etapa08_indexacao.py

A falha: **o chunk perdeu o contexto de onde veio**. Duas curas, com contas de
ordem de grandeza diferente — e, como a rodada 2 mostrou, com **troca de
qualidade**, não só de preço.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_zero.avaliacao import Caso, avaliar                           # noqa: E402
from rag_zero.indexacao import (ChunkIndexado, IndiceDenso,            # noqa: E402
                                contexto_estrutural, custo_estimado)
from rag_zero.ingestao import ingerir                                  # noqa: E402
from rag_zero.portas import EmbedderHashing                            # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
K = 5


def main() -> None:
    docs, _ = ingerir(RAIZ)
    docs = [d for d in docs if "capitulos/" in d.origem]
    chunks = [contexto_estrutural(d.texto, d.origem, d.secao) for d in docs]
    n_docs = len({c.origem for c in chunks})
    print(f"corpus: {len(chunks)} chunks de {n_docs} documentos\n")

    alvos = {
        "o que faz a busca esparsa achar identificador": "06-busca",
        "quando o grafo de entidades compensa": "10-recuperacao-estruturada",
        "o que o metadado de status evita": "04-corpus",
        "o que é abstenção na geração": "15-geracao-fundamentada",
        "por que o reranker usa a nota e não a ordem": "07-reranking",
    }
    casos = [Caso(q, {i for i, c in enumerate(chunks) if alvo in c.origem})
             for q, alvo in alvos.items()]
    casos = [c for c in casos if c.relevantes]

    emb = EmbedderHashing()
    indices = {
        "simples (linha de base)": IndiceDenso(chunks, emb, estrategia="simples"),
        "contextual (prefixo)":    IndiceDenso(chunks, emb, estrategia="contextual"),
        "late (vizinhança)":       IndiceDenso(chunks, emb, estrategia="late"),
    }

    print("as três indexações, mesmas perguntas, mesmo k")
    print("-" * 72)
    for nome, idx in indices.items():
        m = avaliar(nome, casos, lambda q, i=idx: i.buscar(q, K))
        print(f"  {m}")
    print("-" * 72)

    print("\na conta — chamadas estruturais, não preço (que expira)")
    print("-" * 72)
    for chave in ("simples", "contextual", "late"):
        c = custo_estimado(len(chunks), n_docs, chave)
        print(f"  {c['estrategia']:<12} chamadas de LLM: {c['chamadas_llm']:>5}   "
              f"embeddings: {c['embeddings']:>5}")
    print("-" * 72)

    print("\nA leitura, com as duas ressalvas que a trilha não esconde:")
    print("  · O 'contextual' aqui prefixa o CAMINHO HIERÁRQUICO, não um resumo")
    print("    gerado — é a versão de custo zero da mesma ideia. Por isso a coluna")
    print("    'chamadas de LLM' mostra 0 onde a técnica original mostraria N.")
    print("  · O 'late' mistura uma fração do vetor do documento ao do chunk. É o")
    print("    análogo pobre do pooling tardio, e reproduz a propriedade que")
    print("    importa: nenhuma chamada de LLM.")
    print()
    print("  E a correção que a rodada 2 trouxe (arXiv 2504.19754): a escolha")
    print("  entre as duas NÃO é só de preço. O contextual preserva mais coerência")
    print("  semântica e custa mais; o late é eficiente e sacrifica relevância e")
    print("  completude. Dois eixos, não um.")


if __name__ == "__main__":
    main()
