"""Etapa 6 — reranking, a nota como limiar, e o caminho de "não encontrei".

    python3 etapas/etapa06_reranking.py

Duas coisas que o cap. 07 diz e quase nenhum tutorial faz:

1. **Usar a nota, não só a ordem.** O reranking é o único estágio que devolve um
   número calibrável. Jogar isso fora é deixar a abstenção sem instrumento.
2. **Instalar o caminho de abstenção.** Um retriever que sempre devolve K
   sempre devolve *algo*. Se o corpus não tem a resposta, esse algo é ruído — e
   o gerador, sem instrução contrária, vai usá-lo (cap. 15).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_zero.ingestao import ingerir                             # noqa: E402
from rag_zero.portas import EmbedderHashing, RerankerLexical      # noqa: E402
from rag_zero.recuperacao import RecuperadorHibrido               # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]

# A última é a que importa: o corpus deste livro não fala de fotossíntese.
PERGUNTAS = [
    "por que a busca híbrida vence a densa sozinha",
    "quando o grafo de entidades compensa",
    "o que é abstenção na geração fundamentada",
    "como fazer fotossíntese em plantas aquáticas de água salgada",
]


def main() -> None:
    docs, _ = ingerir(RAIZ)
    textos = [d.texto for d in docs]
    rec = RecuperadorHibrido(textos, EmbedderHashing(), RerankerLexical())

    for limiar in (0.0, 0.30):
        titulo = ("SEM limiar (limiar=0.0) — o comportamento padrão da maioria"
                  if limiar == 0.0 else
                  f"COM limiar={limiar:.2f} — e caminho de abstenção")
        print("=" * 72)
        print(titulo)
        print("=" * 72)
        vazias = 0
        for pergunta in PERGUNTAS:
            r = rec.buscar(pergunta, k=3, limiar=limiar)
            print(f'\n  "{pergunta[:58]}"')
            if r.abstem:
                vazias += 1
                print(f"    -> ABSTÉM ({r.motivo}); o gerador NÃO é chamado")
                continue
            for res in r.resultados:
                print(f"    nota={res.nota:.2f}  {docs[res.indice].origem:<38} "
                      f"{textos[res.indice][:44]}...")
        print(f"\n  taxa de resultado zero: {vazias}/{len(PERGUNTAS)} = "
              f"{vazias / len(PERGUNTAS):.0%}")
        print()

    print("=" * 72)
    print("A leitura")
    print("=" * 72)
    print("  Sem limiar, a última pergunta — cujo assunto não existe no corpus —")
    print("  recebe três trechos sobre outra coisa, com nota baixa. Se você os")
    print("  entregar ao gerador sem regra de ausência (cap. 15), a alucinação")
    print("  fundamentada em ruído é o comportamento PADRÃO, não o excepcional.")
    print()
    print("  Com limiar, ela abstém — e a taxa de resultado zero deixa de ser")
    print("  zero. Esse indicador é o sinal operacional mais barato do livro, e")
    print("  ele denuncia por AUSÊNCIA: se vive em zero, quase sempre significa")
    print("  que não existe limiar, e não que a recuperação é perfeita (cap. 21).")
    print()
    print("  O 0.30 daqui foi calibrado NESTE corpus e não transfere. Calibrá-lo")
    print("  no seu é o exercício de completude da etapa (regra 3 da construção).")


if __name__ == "__main__":
    main()
