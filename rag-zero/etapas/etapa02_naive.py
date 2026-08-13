"""Etapas 1 e 2 — os contratos e o Naive RAG: **a linha de base** (caps. 02, 03).

    python3 etapas/etapa02_naive.py

Esta é a etapa que o livro inteiro pressupunha e que faltava. Sem linha de base,
toda tabela de ganho dos capítulos seguintes compara com nada — e a regra do
cap. 09 ("meça primeiro, uma técnica por vez, remova o que não pagou") não tem
de onde partir.

Ela mostra duas coisas:

1. **Os dois caminhos separados** — indexação (paga uma vez) e consulta (paga
   sempre). A separação não é cerimônia: quando os dois se misturam no mesmo
   objeto, a primeira consequência é reindexar por requisição sem ninguém ver.
2. **Os quatro contratos honrados** — a procedência atravessa documento → chunk
   → índice → candidato → citação. É o que torna a citação do cap. 15 possível.

Delta (ADR 0014) — vem da etapa 0; decide: fechar o circuito inteiro na forma mais burra possível — a linha de base contra a qual todo ganho posterior é medido.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_zero.pipeline import CaminhoDeIndexacao, NaiveRAG, procedencia_sobreviveu  # noqa: E402
from rag_zero.portas import LLMFundamentado                                          # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]

PERGUNTAS = [
    "por que a busca híbrida vence a densa sozinha",
    "o que o metadado de status evita no corpus",
    "como fazer fotossíntese em plantas aquáticas",   # fora do corpus
]


def main() -> None:
    print("=" * 72)
    print("CAMINHO DE INDEXAÇÃO — offline, caro, pago UMA vez")
    print("=" * 72)
    caminho = CaminhoDeIndexacao(RAIZ)
    for chave, valor in caminho.relatorio.items():
        print(f"  {chave:<34} {valor}")
    print(f"\n  exemplo de identificador estável: {caminho.unidades[0].id}")
    print("  Ele é derivado de origem + posição, não de um contador global — por")
    print("  isso sobrevive a uma reindexação. Identificador que muda a cada build")
    print("  quebra o contrato nº 4 sem que nada falhe de forma visível.")

    print()
    print("=" * 72)
    print("CAMINHO DE CONSULTA — online, barato por execução, pago SEMPRE")
    print("=" * 72)
    rag = NaiveRAG(caminho, LLMFundamentado(), k=3)

    for pergunta in PERGUNTAS:
        ex = rag.responder(pergunta)
        print(f'\n  "{pergunta}"')
        print(f"    candidatos (contrato nº 3 — id E nota):")
        for ident, nota in ex.candidatos:
            print(f"      {nota:6.2f}  {ident}")
        if not ex.candidatos:
            print("      (nenhum)")
        print(f"    contexto: {ex.contexto.tokens} tokens em "
              f"{len(ex.contexto.blocos)} blocos")
        print(f"    resposta: {ex.resposta.texto[:88]}")
        print(f"    procedência sobreviveu aos 4 contratos: "
              f"{procedencia_sobreviveu(ex)}")

    print()
    print("=" * 72)
    print("O que esta linha de base NÃO faz — e é essa a lista do resto do livro")
    print("=" * 72)
    print("  · fusão com busca densa .............. cap. 06, etapa 5")
    print("  · reranking e limiar ................. cap. 07, etapa 6")
    print("  · entendimento da consulta ........... cap. 08, etapa 7")
    print("  · indexação refinada ................. cap. 09, etapa 8")
    print("  · recuperação estruturada ............ cap. 10, etapa 9")
    print("  · laço agêntico ...................... cap. 18, etapa 11")
    print()
    print("  Cada uma delas precisa PROVAR que bate esta linha. É a regra de")
    print("  sequência do cap. 09 — e é por isso que a etapa 2 vem antes de todas.")


if __name__ == "__main__":
    main()
