"""Etapa 5 — BM25 na mão, antes de qualquer biblioteca (cap. 06).

Regra 1 da construção: **do zero antes da biblioteca.** O objetivo é você ver o
mecanismo funcionar antes de delegá-lo — e descobrir que ele cabe em ~40 linhas.

Por que BM25 e não contagem de termos: a contagem crua trata todos os termos
como iguais. BM25 acrescenta as duas correções que a fazem funcionar:

1. **IDF** — termo raro vale mais que termo comum. Sem isso, "sistema" pesa o
   mesmo que "RAPTOR", e a busca vira sorteio entre documentos longos.
2. **Saturação e normalização por comprimento** — a décima ocorrência de um
   termo vale menos que a segunda (`k1`), e documento longo não ganha só por
   ser longo (`b`).

O BEIR ([arXiv 2104.08663](https://arxiv.org/abs/2104.08663)) mede o resultado
disso em 18 datasets e conclui: *"BM25 is a robust baseline"*. **Se o seu
sistema não bate isto aqui, ele não está pronto.**
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass

from .portas import normalizar


@dataclass
class Resultado:
    indice: int
    nota: float


class BM25:
    """BM25 Okapi. Índice invertido em memória, sem dependência externa.

    Os padrões `k1=1.5` e `b=0.75` são os da literatura — e são exatamente o
    tipo de constante que se copia sem pensar. A pegadinha do Apêndice A do
    cap. 06 vale aqui: em produção, o **analisador** (o que `normalizar()` faz)
    muda o resultado tanto quanto `k1` e `b`, e quase ninguém o audita.
    """

    def __init__(self, documentos: list[str], *, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1, self.b = k1, b
        self.docs: list[list[str]] = [normalizar(d) for d in documentos]
        self.n = len(self.docs)
        self.tamanhos = [len(d) for d in self.docs]
        self.tamanho_medio = (sum(self.tamanhos) / self.n) if self.n else 0.0

        # Índice invertido: termo -> {doc: frequência}. É a estrutura que torna
        # a busca sublinear — sem ela, toda consulta varre o corpus inteiro.
        self.invertido: dict[str, dict[int, int]] = {}
        for i, doc in enumerate(self.docs):
            for termo, freq in Counter(doc).items():
                self.invertido.setdefault(termo, {})[i] = freq

        # IDF pré-computado, na forma com suavização (evita negativo em termo
        # presente em mais da metade do corpus).
        self.idf: dict[str, float] = {
            termo: math.log(1 + (self.n - len(postings) + 0.5) / (len(postings) + 0.5))
            for termo, postings in self.invertido.items()
        }

    def buscar(self, consulta: str, k: int = 10) -> list[Resultado]:
        notas: dict[int, float] = {}
        for termo in normalizar(consulta):
            postings = self.invertido.get(termo)
            if not postings:
                continue
            idf = self.idf[termo]
            for i, freq in postings.items():
                norma = 1 - self.b + self.b * (self.tamanhos[i] / self.tamanho_medio)
                notas[i] = notas.get(i, 0.0) + idf * (freq * (self.k1 + 1)) / (
                    freq + self.k1 * norma
                )
        ordenados = sorted(notas.items(), key=lambda kv: (-kv[1], kv[0]))
        return [Resultado(i, nota) for i, nota in ordenados[:k]]
