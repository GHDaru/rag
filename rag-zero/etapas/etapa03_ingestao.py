"""Etapa 3 — ingestão e governança (cap. 04).

    python3 etapas/etapa03_ingestao.py

O teste que fecha a etapa, e que dá nome ao capítulo: **um documento marcado
como `revogado` não aparece em nenhuma recuperação, mesmo sendo o mais similar
à consulta.** Um índice que não sabe disso não é um índice — é uma pilha de
texto, e nenhuma técnica dos capítulos seguintes conserta.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_zero.bm25 import BM25                                        # noqa: E402
from rag_zero.ingestao import Documento, enriquecer, filtrar_indexaveis, ingerir  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]


def demonstrar_revogado() -> None:
    """Dois documentos quase idênticos; um revogado. Qual o índice devolve?"""
    docs = [
        Documento(
            origem="politicas/reembolso-2023.md",
            texto="Política de reembolso: o prazo para solicitar reembolso é de "
                  "90 dias corridos a partir da compra. Esta política foi revogada "
                  "e substituída pela versão de 2026.",
            data=date(2023, 1, 1), status="revogado",
        ),
        Documento(
            origem="politicas/reembolso-2026.md",
            texto="Política de reembolso: o prazo para solicitar reembolso é de "
                  "30 dias corridos a partir da compra.",
            data=date(2026, 1, 1), status="vigente",
        ),
    ]
    docs = [enriquecer(d) for d in docs]
    consulta = "qual o prazo para solicitar reembolso"

    print("=" * 64)
    print("SEM governança — o índice não sabe o que é verdade, sabe o que é parecido")
    print("=" * 64)
    todos = BM25([d.texto for d in docs])
    for r in todos.buscar(consulta, k=2):
        d = docs[r.indice]
        print(f"  nota={r.nota:5.2f}  status={d.status:<9} {d.origem}")
    print("\n  ^ o revogado ranqueia — e ranqueia BEM, porque é mais longo e "
          "repete os termos.\n    Um documento revogado embedda exatamente igual "
          "a um vigente.")

    print()
    print("=" * 64)
    print("COM governança — filtro por metadado ANTES da busca")
    print("=" * 64)
    indexaveis = filtrar_indexaveis(docs)
    filtrado = BM25([d.texto for d in indexaveis])
    for r in filtrado.buscar(consulta, k=2):
        d = indexaveis[r.indice]
        print(f"  nota={r.nota:5.2f}  status={d.status:<9} {d.origem}")

    print("\n  O filtro acontece na CONSTRUÇÃO do índice e na consulta — nunca")
    print("  sobre o resultado. Filtrar depois desperdiça o top_k, falseia a")
    print("  métrica e, dependendo de log e cache, vaza (cap. 22).")

    print()
    print("O que o extrator GEROU, e por que ele não filtra:")
    for d in docs:
        valor, conf = d.gerado["status_extraido"]
        print(f"  {d.origem:<34} status_extraido={valor:<9} confiança={conf:.1f}")
    print("\n  Repare: o gerado bateu com o herdado neste caso. Mesmo assim ele")
    print("  NÃO é usado para excluir candidato — só o herdado e o derivado")
    print("  filtram de forma dura. Metadado gerado errado faz o documento certo")
    print("  sumir ANTES da busca, sem deixar rastro no log (cap. 04 §4).")


def demonstrar_corpus_real() -> None:
    """A ingestão do texto deste livro, com o relatório que quase ninguém coleta."""
    docs, rel = ingerir(RAIZ)
    print()
    print("=" * 64)
    print("Ingestão do corpus real (o texto deste livro)")
    print("=" * 64)
    for chave, valor in rel.items():
        print(f"  {chave:<38} {valor}")
    print("\n  'duplicados_removidos' é o número que a maioria dos pipelines não")
    print("  coleta — e cada duplicata ocupa um lugar do top_k, deslocando o")
    print("  trecho que faltava.")


if __name__ == "__main__":
    demonstrar_revogado()
    demonstrar_corpus_real()
