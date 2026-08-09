"""Etapa 14 (antecipada) — as métricas mínimas, para medir as etapas anteriores.

O cap. 09 tem uma regra que vale mais que todas as técnicas dele: **meça
primeiro qual falha você tem**. Cumprir essa regra exige que a medição exista
antes da otimização — e é por isso que este módulo aparece cedo, mesmo que o
capítulo correspondente venha depois.

O que está aqui é o subconjunto que roda **sem juiz e sem chave**: as métricas
de recuperação. `faithfulness` e `answer relevance` exigem LLM-as-judge e ficam
para a etapa 14 completa.

Sobre a atribuição, que a rodada 2 corrigiu: o paper do RAGAS propõe três
aspectos — *faithfulness*, *answer relevance* e *context relevance*. O par
`context_precision` / `context_recall` é da **biblioteca**, que desdobrou o
terceiro em dois porque as duas metades diagnosticam falhas diferentes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Caso:
    """Uma pergunta com os documentos que **deveriam** ser recuperados."""

    pergunta: str
    relevantes: set[int]


def context_recall(recuperados: list[int], relevantes: set[int]) -> float:
    """Dos trechos necessários, quantos vieram. Baixo = problema de achar."""
    if not relevantes:
        return 1.0
    return len(set(recuperados) & relevantes) / len(relevantes)


def context_precision(recuperados: list[int], relevantes: set[int]) -> float:
    """Dos trechos recuperados, quantos eram relevantes. Baixo = ruído pago."""
    if not recuperados:
        return 0.0
    return len(set(recuperados) & relevantes) / len(recuperados)


def taxa_resultado_zero(recuperacoes: list[list[int]]) -> float:
    """Proporção de consultas que voltaram vazias.

    O sinal operacional mais barato da recuperação — e o que **denuncia por
    ausência**: se ele vive em zero, provavelmente não existe limiar nem
    caminho de abstenção no sistema, e não que a recuperação seja perfeita.
    """
    if not recuperacoes:
        return 0.0
    return sum(1 for r in recuperacoes if not r) / len(recuperacoes)


def acerto(recuperados: list[int], relevantes: set[int]) -> float:
    """1.0 se **algum** trecho relevante apareceu no top-k; 0.0 caso contrário.

    Esta métrica existe por uma razão que vale mais que ela: quando o gabarito
    marca dezenas de trechos como relevantes (por exemplo, "tudo do cap. 06") e
    você mede `context_recall` em `k=5`, o teto matemático é `5/40 = 0,125`.
    **O número parece péssimo por construção**, e não por defeito da busca.

    É o erro de medição mais fácil de cometer e mais difícil de perceber — e é
    a razão de o cap. 21 insistir que a métrica precisa casar com a pergunta que
    você está fazendo. Aqui a pergunta é "o pipeline encontra o lugar certo do
    livro?", e a resposta certa é taxa de acerto, não recall.
    """
    return 1.0 if set(recuperados) & relevantes else 0.0


@dataclass
class Medicao:
    nome: str
    acerto: float
    recall: float
    precisao: float
    zero: float

    def __str__(self) -> str:
        return (f"{self.nome:<26} acerto={self.acerto:.0%}  "
                f"precisão={self.precisao:.3f}  recall@k={self.recall:.3f}  "
                f"zero={self.zero:.0%}")


def avaliar(nome: str, casos: list[Caso], buscar) -> Medicao:
    """Roda um conjunto de casos contra uma função de busca.

    `buscar` recebe a pergunta e devolve uma lista de índices. Qualquer estágio
    do pipeline serve — é isso que permite a tabela "ganho por estágio" da
    etapa 5, que é o exercício central da trilha.
    """
    acertos, recalls, precisoes, saidas = [], [], [], []
    for caso in casos:
        obtidos = buscar(caso.pergunta)
        saidas.append(obtidos)
        acertos.append(acerto(obtidos, caso.relevantes))
        recalls.append(context_recall(obtidos, caso.relevantes))
        precisoes.append(context_precision(obtidos, caso.relevantes))
    n = len(casos) or 1
    return Medicao(nome, sum(acertos) / n, sum(recalls) / n,
                   sum(precisoes) / n, taxa_resultado_zero(saidas))
