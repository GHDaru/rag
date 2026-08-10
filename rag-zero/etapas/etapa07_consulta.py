"""Etapa 7 — o lado da pergunta, medido contra a linha de base (cap. 08).

    python3 etapas/etapa07_consulta.py

Os caps. 06 e 07 otimizam **como se busca**. Este otimiza **o que se busca**. E a
regra econômica que atravessa tudo aqui: isto é **custo de consulta**, pago para
sempre — ao contrário do cap. 09, onde se paga uma vez na indexação.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_zero.consulta import (Consulta, entender, precisa_resolver,  # noqa: E402
                               rotear)
from rag_zero.portas import LLMEco                                    # noqa: E402


class LLMReescritor:
    """Reescritor determinístico — encena o estágio sem gastar token.

    Ele não entende nada: cola a última menção do histórico na pergunta. O que a
    etapa demonstra é **o portão** (`precisa_resolver`), não a qualidade da
    reescrita.
    """

    def gerar(self, prompt: str, *, max_tokens: int = 512) -> str:
        conversa = prompt.split("<conversa>")[-1].split("</conversa>")[0]
        pergunta = prompt.rsplit("pergunta:", 1)[-1].strip()
        assunto = conversa.strip().splitlines()[0][:60] if conversa.strip() else ""
        return f"{pergunta} (sobre: {assunto})" if assunto else pergunta


def main() -> None:
    print("=" * 72)
    print("1. ROTEAMENTO — determinístico, auditável, custo zero")
    print("=" * 72)
    for p in ("quantos contratos vencem este mês",
              "quais são os temas recorrentes deste corpus",
              "o que é fusão por posição"):
        print(f"  {rotear(p):<12} <- \"{p}\"")
    print("\n  Roteador por palavra-chave, não por modelo — e isso é decisão, não")
    print("  preguiça: falha de forma previsível e custa zero. Um classificador")
    print("  por LLM acerta mais e custa uma chamada por pergunta, PARA SEMPRE.")
    print("  Comece pelo barato e meça se o caro paga.")

    print()
    print("=" * 72)
    print("2. RESOLUÇÃO DE REFERÊNCIA — o portão é metade do valor")
    print("=" * 72)
    historico = ["usuário: como funciona a busca híbrida?",
                 "assistente: ela funde os rankings esparso e denso por posição."]
    for pergunta in ("e o outro?", "qual o limiar de abstenção recomendado"):
        precisa = precisa_resolver(pergunta, historico)
        print(f'\n  "{pergunta}"')
        print(f"    precisa resolver? {precisa}")
        if precisa:
            resolvida = entender(pergunta, LLMReescritor(), historico=historico)
            print(f"    reescrita -> {resolvida.original}")
        else:
            print("    -> vai direto ao índice; nenhuma chamada de modelo gasta")
    print("\n  Sem o portão, você paga uma chamada por turno para descobrir que")
    print("  não precisava de nenhuma. Com ele, paga só quando importa.")

    print()
    print("=" * 72)
    print("3. A CONTA — por que os padrões vêm desligados")
    print("=" * 72)
    eco = LLMEco()
    c = entender("o que é abstenção", eco, usar_hyde=True, expandir=True)
    print(f"  com HyDE + expansão ligados: {len(c.todas)} consultas, "
          f"{len(eco.chamadas)} chamadas de modelo — POR PERGUNTA")
    eco2 = LLMEco()
    c2 = entender("o que é abstenção", eco2)
    print(f"  com os padrões conservadores: {len(c2.todas)} consulta, "
          f"{len(eco2.chamadas)} chamadas")
    print("\n  Ligar um estágio sem medir contra a linha de base (etapa 2) é")
    print("  exatamente o que a regra de sequência do cap. 09 proíbe.")


if __name__ == "__main__":
    main()
