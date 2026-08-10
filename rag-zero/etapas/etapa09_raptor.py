"""Etapa 9 — RAPTOR reduzido: pergunta global × pergunta factual (cap. 10).

    python3 etapas/etapa09_raptor.py

Constrói a árvore de resumos recursivos sobre o texto deste livro e compara,
na mesma pergunta, o que vem das **folhas** e o que vem dos **nós altos**.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_zero.ingestao import ingerir                    # noqa: E402
from rag_zero.portas import EmbedderHashing              # noqa: E402
from rag_zero.raptor import Raptor                       # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]

GLOBAL = "quais são os temas recorrentes deste livro"
FACTUAL = "qual o limiar de abstenção e onde ele é calibrado"


def main() -> None:
    docs, _ = ingerir(RAIZ)
    # Subconjunto: a árvore é O(n²) no agrupamento guloso, e o ponto aqui é
    # pedagógico, não de escala. Em corpus grande, o agrupamento precisa de
    # índice aproximado — que é a mesma troca recall/latência do cap. 06.
    docs = [d for d in docs if "capitulos/" in d.origem][:180]
    textos = [d.texto for d in docs]

    print(f"folhas: {len(textos)} blocos\nconstruindo a árvore...\n")
    arvore = Raptor(textos, EmbedderHashing(),
                    origens=[d.origem for d in docs], niveis=3)

    print(f"altura: {arvore.altura}")
    for nivel, quantos in arvore.por_nivel().items():
        rotulo = "folhas (texto original)" if nivel == 0 else f"resumos de nível {nivel}"
        corte = f"   corte={arvore.limiares[nivel - 1]:.3f}" if nivel else ""
        print(f"  nível {nivel}: {quantos:>4} nós   {rotulo}{corte}")
    print("\n  Os cortes foram DERIVADOS do corpus, não escolhidos. A primeira")
    print("  versão desta etapa usava limiar fixo de 0.35 — e a árvore degenerava")
    print("  (180 -> 141 nós, quase todos com um filho só), porque com este")
    print("  embedder a mediana de similaridade é 0.049 e o percentil 99 é 0.314.")
    print("  Similaridade não é comparável entre embedders: é a mesma regra do")
    print("  limiar de reranking (cap. 07) e do peso da fusão (cap. 06).")

    for pergunta, tipo in ((GLOBAL, "GLOBAL"), (FACTUAL, "FACTUAL")):
        print()
        print("=" * 72)
        print(f"pergunta {tipo}: \"{pergunta}\"")
        print("=" * 72)
        for rotulo, nivel in (("só folhas (nível 0)", 0), ("árvore inteira", None)):
            print(f"\n  {rotulo}:")
            for i in arvore.buscar(pergunta, k=2, nivel=nivel):
                no = arvore.nos[i]
                marca = f"nível {no.nivel}" + (f", {len(no.filhos)} filhos" if no.filhos else "")
                print(f"    [{marca}] {no.texto[:88]}...")

    print()
    print("=" * 72)
    print("A leitura — e uma ressalva honesta")
    print("=" * 72)
    print("  O resumidor aqui é EXTRATIVO: escolhe as frases mais centrais do")
    print("  grupo. Ele nunca produz uma frase que não estava lá — o que é bom")
    print("  para procedência e ruim para o que dá poder ao RAPTOR: a SÍNTESE.")
    print("  Um resumo que só recorta não condensa de verdade, e por isso o")
    print("  ganho na pergunta global aparece atenuado aqui.")
    print()
    print("  Trocar por uma chamada de LLM é uma linha — o LLMPort já existe.")
    print("  E aí aparece a conta do cap. 10: RAPTOR precisa de embeddings e")
    print("  agrupamento; grafo precisa EXTRAIR ENTIDADES, que é um modelo a")
    print("  mais, um erro a mais e um custo a mais.")
    print()
    print("  Grafo fica de fora desta trilha de propósito: o corpus deste livro")
    print("  não tem entidades recorrentes o bastante para justificá-lo, e")
    print("  fingir que tem seria ensinar o erro que o cap. 10 denuncia.")


if __name__ == "__main__":
    main()
