"""Etapa 0 — o contador de tokens por bloco, e a montagem do contexto.

Este é **o instrumento do livro** (cap. 20). A maior parte dos sistemas em
produção não tem nada equivalente, e é exatamente por isso que degradam de forma
inexplicável: ninguém sabe dizer quanto do contexto foi para cada fonte.

Ele vem na etapa 0, antes de qualquer recuperação, porque todas as etapas
seguintes vão olhar para ele.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


def contar_tokens(texto: str) -> int:
    """Estimativa de tokens sem dependência externa.

    **Isto é uma aproximação, e o livro não finge o contrário.** A regra usada é
    a heurística comum de ~4 caracteres por token para texto latino, com piso na
    contagem de palavras.

    A pegadinha registrada no Apêndice A do cap. 20 vale aqui inteira: cada
    família de modelo tokeniza diferente, e um orçamento calibrado num
    tokenizador **não transfere** para outro. Para número de fatura, use o
    tokenizador do seu provedor atrás de uma porta — a estrutura deste módulo
    não muda.
    """
    palavras = len(re.findall(r"\S+", texto))
    return max(palavras, len(texto) // 4)


@dataclass
class Bloco:
    """Um pedaço nomeado do contexto, com sua procedência.

    O nome não é decoração: é ele que aparece no contador, e é o que permite
    responder "quem gastou o orçamento?" sem adivinhar.
    """

    nome: str
    conteudo: str
    fonte: str = ""          # de onde veio — o contrato de procedência do cap. 02
    confiavel: bool = True   # False = conteúdo externo, é DADO e nunca instrução

    @property
    def tokens(self) -> int:
        return contar_tokens(self.conteudo)


@dataclass
class Contexto:
    """O contexto montado, em blocos — com orçamento e política de corte.

    Duas regras do livro estão codificadas aqui, e não em comentário:

    - **Camadas por volatilidade** (cap. 14): a ordem de inserção é a ordem de
      montagem, e nada volátil deve entrar acima de algo estável, senão o cache
      por prefixo do cap. 23 é invalidado.
    - **Conteúdo recuperado é dado, nunca instrução** (constituição, Princípio V):
      blocos com `confiavel=False` são delimitados e rotulados na montagem.
    """

    blocos: list[Bloco] = field(default_factory=list)
    orcamento: int | None = None

    def adicionar(self, nome: str, conteudo: str, *, fonte: str = "",
                  confiavel: bool = True) -> "Contexto":
        self.blocos.append(Bloco(nome, conteudo, fonte, confiavel))
        return self

    @property
    def tokens(self) -> int:
        return sum(b.tokens for b in self.blocos)

    def composicao(self) -> list[tuple[str, int, float]]:
        """(nome, tokens, fração) por bloco — o painel que quase ninguém tem."""
        total = self.tokens or 1
        return [(b.nome, b.tokens, b.tokens / total) for b in self.blocos]

    def estourou(self) -> bool:
        return self.orcamento is not None and self.tokens > self.orcamento

    def montar(self) -> str:
        """Serializa o contexto. **Determinística** — e isso não é detalhe.

        A pegadinha do Apêndice A do cap. 23: um bloco serializado em ordem
        diferente quebra o cache por prefixo sem mudar uma palavra do conteúdo.
        É a causa nº 1 de cache que "não funciona".
        """
        partes: list[str] = []
        for b in self.blocos:
            if b.confiavel:
                partes.append(b.conteudo)
            else:
                # Delimitar e rotular: a separação entre ordem e material só
                # existe na medida em que a montagem a torna evidente (cap. 11).
                proc = f" fonte={b.fonte}" if b.fonte else ""
                partes.append(
                    f"<{b.nome}{proc}>\n{b.conteudo}\n</{b.nome}>"
                )
        return "\n\n".join(partes)

    def relatorio(self) -> str:
        """O contador impresso — a saída que fecha a etapa 0."""
        linhas = [f"{'bloco':<22} {'tokens':>8} {'%':>7}  procedência"]
        linhas.append("-" * 62)
        for b in self.blocos:
            frac = b.tokens / (self.tokens or 1)
            marca = "" if b.confiavel else "  [externo — dado, não instrução]"
            linhas.append(f"{b.nome:<22} {b.tokens:>8} {frac:>6.1%}  {b.fonte}{marca}")
        linhas.append("-" * 62)
        alvo = f" / orçamento {self.orcamento}" if self.orcamento else ""
        estouro = "  ESTOUROU" if self.estourou() else ""
        linhas.append(f"{'TOTAL':<22} {self.tokens:>8}{alvo}{estouro}")
        return "\n".join(linhas)
