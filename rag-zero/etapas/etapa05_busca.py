"""Etapa 5 — esparso, denso e a fusão, medidos com o mesmo conjunto (cap. 06).

    python3 etapas/etapa05_busca.py

Esta é a etapa central da trilha. Ela constrói os três recuperadores sobre o
texto deste livro e mede os três com as **mesmas** perguntas, imprimindo o ganho
por estágio. O objetivo pedagógico é ver o ranking acontecer — e ver o ponto
cego de cada família aparecer numa pergunta concreta.

Um aviso que faz parte da lição: o embedder daqui é de *hashing*, sem semântica
(ver `rag_zero.portas.EmbedderHashing`). Ele reproduz a **mecânica** da busca
densa, não a **qualidade**. A saída mostra exatamente onde isso quebra — e é
esse o erro didático deliberado da etapa.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_zero.avaliacao import Caso, avaliar                      # noqa: E402
from rag_zero.bm25 import BM25                                    # noqa: E402
from rag_zero.ingestao import ingerir                             # noqa: E402
from rag_zero.portas import EmbedderHashing, RerankerLexical      # noqa: E402
from rag_zero.recuperacao import BuscaDensa, fundir, rerankear    # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
K = 5


def construir_casos(docs) -> list[Caso]:
    """Conjunto sintético a partir do próprio corpus.

    A ressalva do cap. 21 vale e está aqui por escrito: conjunto sintético
    derivado do corpus **superestima o recall**, porque a pergunta é escrita a
    partir do documento que a responde. Serve para comparar estágios entre si
    (que é o uso desta etapa), não para reportar qualidade absoluta.
    """
    alvos = {
        "o que faz a busca esparsa achar identificador e código":
            "06-busca",
        "por que fundir por posição dispensa calibrar as notas":
            "06-busca",
        "quando o grafo de entidades compensa e quando não compensa":
            "10-recuperacao-estruturada",
        "como a árvore de resumos recursivos responde pergunta global":
            "10-recuperacao-estruturada",
        "o que o metadado de status evita no corpus":
            "04-corpus",
        "qual a diferença entre contextual retrieval e late chunking":
            "09-recuperacao-avancada",
        "o que é abstenção e quando o gerador não deve ser chamado":
            "15-geracao-fundamentada",
        "por que o reranker usa a nota e não só a ordem":
            "07-reranking",
    }
    casos = []
    for pergunta, alvo in alvos.items():
        relevantes = {i for i, d in enumerate(docs) if alvo in d.origem}
        if relevantes:
            casos.append(Caso(pergunta, relevantes))
    return casos


def main() -> None:
    docs, _ = ingerir(RAIZ)
    textos = [d.texto for d in docs]
    print(f"corpus: {len(textos)} blocos de {len({d.origem for d in docs})} arquivos\n")

    esparso = BM25(textos)
    denso = BuscaDensa(textos, EmbedderHashing())
    reranker = RerankerLexical()
    casos = construir_casos(docs)

    def so_esparso(q):
        return [r.indice for r in esparso.buscar(q, K)]

    def so_denso(q):
        return [r.indice for r in denso.buscar(q, K)]

    def hibrido(q):
        return [r.indice for r in fundir(
            [esparso.buscar(q, 30), denso.buscar(q, 30)], k=K)]

    def hibrido_com_reranker(q):
        cand = fundir([esparso.buscar(q, 30), denso.buscar(q, 30)], k=30)
        rec = rerankear(q, cand, textos, reranker, k=K, limiar=0.15)
        return [r.indice for r in rec.resultados]

    print(f"{len(casos)} perguntas · k={K}\n")
    print("ganho por estágio — cada linha acrescenta UM estágio ao anterior")
    print("-" * 72)
    medicoes = [
        avaliar("1. só esparso (BM25)", casos, so_esparso),
        avaliar("2. só denso (hashing)", casos, so_denso),
        avaliar("3. híbrido (fusão RRF)", casos, hibrido),
        avaliar("4. híbrido + reranking", casos, hibrido_com_reranker),
    ]
    for m in medicoes:
        print(f"  {m}")
    print("-" * 72)

    print("\nPor que a coluna que importa é 'acerto', e não 'recall@k':")
    print("  O gabarito marca TODOS os blocos do capítulo-alvo como relevantes —")
    print("  dezenas deles. Com k=5, o recall tem teto matemático em ~0,12, e o")
    print("  número pareceria péssimo por construção, não por defeito da busca.")
    print("  É o erro de medição mais fácil de cometer e mais difícil de ver.")
    print("  A pergunta real aqui é 'o pipeline acha o lugar certo do livro?' —")
    print("  e a métrica que responde isso é taxa de acerto (cap. 21).")
    print("\nComo ler esta tabela:")
    print("  · A linha 2 é o erro didático deliberado. O embedder de hashing não")
    print("    tem semântica: ele erra onde a esparsa erra, e custa mais. Trocar")
    print("    o adaptador por um modelo de verdade é UMA linha — e é aí que a")
    print("    linha 3 passa a ganhar de verdade (cap. 06).")
    print("  · Se a linha 3 não superar a 1 no SEU corpus, o problema é o")
    print("    embedder, não a fusão. Medir separa as duas hipóteses; opinar não.")
    print("  · A linha 4 troca recall por precisão. É o comportamento esperado")
    print("    do reranking, e é por isso que ele vem depois, sobre N candidatos.")

    print("\nO ponto cego, numa pergunta concreta:")
    demonstrar_ponto_cego(esparso, denso, textos)


def demonstrar_ponto_cego(esparso, denso, textos) -> None:
    """A pergunta que separa as duas famílias — e o que ela revela aqui."""
    consulta = "arXiv 2401.18059"
    print(f'  consulta literal: "{consulta}"  (o identificador do RAPTOR)')
    for nome, motor in (("esparso", esparso), ("denso  ", denso)):
        r = motor.buscar(consulta, 1)
        if not r:
            print(f"    {nome}: NADA")
            continue
        trecho = textos[r[0].indice]
        veredito = "CERTO" if "2401.18059" in trecho else "ERRADO"
        print(f"    {nome}: {veredito:<6} -> {trecho[:62]}...")
    print("\n  Identificador é o território da busca esparsa. É o sintoma mais")
    print("  comum de RAG sem BM25: 'o sistema não encontra o óbvio' — e o óbvio")
    print("  quase sempre é um código, uma sigla ou um nome próprio.")


if __name__ == "__main__":
    main()
