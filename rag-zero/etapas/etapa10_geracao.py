"""Etapa 10 — o gerador fundamentado, e a verificação da citação (cap. 15).

    python3 etapas/etapa10_geracao.py

O "G" do RAG. Um sistema que recupera bem e gera mal erra **com fontes ao lado**
— o que é pior, porque parece confiável.

A etapa roda três geradores contra o mesmo contexto. Nenhum deles é um modelo
real: são adaptadores que encenam, de forma determinística, os três
comportamentos do capítulo. O que a etapa demonstra não é qualidade de redação —
é que **a verificação pega o defeito**.

Delta (ADR 0014) — vem da etapa 9; decide: a metade esquecida da sigla: citação verificável e abstenção, com a verificação pegando o defeito.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_zero.geracao import Trecho, gerar                                 # noqa: E402
from rag_zero.portas import LLMAlucinado, LLMDeMemoria, LLMFundamentado    # noqa: E402

TRECHOS = [
    Trecho("T1", "O prazo para solicitar reembolso é de 30 dias corridos a partir "
                 "da compra. O pedido é feito pelo portal.", "politicas/reembolso.md"),
    Trecho("T2", "Produtos em promoção seguem o mesmo prazo de reembolso.",
           "politicas/promocoes.md"),
]

GERADORES = [
    ("fundamentado", LLMFundamentado(), "usa só o material e cita"),
    ("alucinado", LLMAlucinado(), "cita [T7], que não existe no contexto"),
    ("de memória", LLMDeMemoria(), "responde sem citar — pode até acertar"),
]


def main() -> None:
    pergunta = "Qual o prazo para pedir reembolso?"
    print(f'pergunta: "{pergunta}"')
    print(f"contexto: {len(TRECHOS)} trechos ({', '.join(t.id for t in TRECHOS)})\n")

    for nome, llm, descricao in GERADORES:
        resposta, ctx = gerar(pergunta, TRECHOS, llm)
        print("=" * 72)
        print(f"{nome.upper()} — {descricao}")
        print("=" * 72)
        print(f"  resposta: {resposta.texto}")
        print(f"  fundamentada ...........: {resposta.fundamentada}")
        print(f"  citações ...............: {resposta.citacoes or '(nenhuma)'}")
        print(f"  citações INVÁLIDAS .....: {resposta.citacoes_invalidas or '(nenhuma)'}")
        print(f"  afirmações sem citação ..: {resposta.afirmacoes_sem_citacao}")
        print(f"  contexto enviado ........: {ctx.tokens} tokens\n")

    print("=" * 72)
    print("A abstenção, que é a metade esquecida do prompt de RAG")
    print("=" * 72)
    resposta, _ = gerar("O que é fotossíntese?", [], LLMFundamentado())
    print(f"  sem trechos -> resposta='{resposta.texto}'  abstem={resposta.abstem}")
    print("  O modelo NÃO é chamado. Chamar um gerador sem material e torcer")
    print("  para que ele recuse é pagar por uma alucinação provável.\n")

    print("=" * 72)
    print("A leitura")
    print("=" * 72)
    print("  Os três modos de falha são DIFERENTES, e o livro insiste nisso:")
    print()
    print("  · Citação inválida é o mais perigoso, porque a resposta PARECE")
    print("    verificável — tem colchete, tem número, tem cara de fonte. Só que")
    print("    a fonte não existe. Isso é pegável por código, e foi pego.")
    print("  · Afirmação sem citação não prova que o modelo inventou. Prova que")
    print("    NÃO DÁ PARA CONFERIR — que é motivo suficiente para recusar.")
    print("  · Abstenção não é falha: é a resposta certa quando falta base.")
    print("    Por isso ela conta como 'fundamentada' aqui.")
    print()
    print("  E note o que torna tudo isso possível: o identificador [T1] que")
    print("  atravessou documento -> chunk -> candidato -> contexto -> citação.")
    print("  É o quarto contrato do cap. 02. Sem ele, a citação verificável do")
    print("  cap. 15 não tem em que se apoiar — e o sistema só pode citar vago.")


if __name__ == "__main__":
    main()
