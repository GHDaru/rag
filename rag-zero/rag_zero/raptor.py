"""Etapa 9 — RAPTOR reduzido: a árvore de resumos recursivos (cap. 10).

A pergunta que nenhum `top_k` sobre texto responde é a **global**: *"quais são os
temas recorrentes nestes 800 chamados?"*. A resposta é propriedade do
**conjunto**, não de nenhuma parte dele — e aumentar `top_k` não aproxima, piora.

O RAPTOR ([arXiv 2401.18059](https://arxiv.org/abs/2401.18059)) resolve com três
verbos, e o paper os nomeia assim: *"recursively **embedding**, **clustering**,
and **summarizing** chunks of text, constructing a tree with differing levels of
summarization from the bottom up"*. A recuperação passa a acontecer **em
qualquer nível**.

Aqui ele cabe em ~80 linhas, sem dependência externa.

**Grafo fica de fora, e a etapa explica por quê:** o corpus deste livro não tem
entidades recorrentes o bastante para justificar a extração, e fingir que tem
seria ensinar exatamente o erro que o cap. 10 denuncia.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

from .portas import EmbedderPort, cosseno, normalizar


def limiar_por_percentil(vetores: list[list[float]], percentil: float = 97.0,
                         *, amostra: int = 120) -> float:
    """Deriva o limiar de agrupamento **do próprio corpus**, não de um chute.

    Esta função nasceu de um defeito real, e vale contar porque a lição é do
    livro. A primeira versão desta etapa usava `limiar=0.35` fixo. Medindo a
    distribuição de similaridade no corpus deste livro com o embedder de
    *hashing*, a mediana é **0,049** e o percentil 99 é **0,314** — ou seja, o
    limiar fixo agrupava quase nada, e a árvore degenerava: 180 folhas viravam
    141 nós, quase todos com um filho só. Um RAPTOR que não condensa não é
    RAPTOR; é a mesma lista com passos extras.

    A causa é a de sempre nesta trilha: **similaridade não é comparável entre
    embedders**. Um valor calibrado num modelo não transfere para outro — é a
    mesma regra do limiar de reranking (cap. 07) e do peso da fusão (cap. 06).

    Derivar do corpus resolve para qualquer adaptador que você plugue.
    """
    passo = max(1, len(vetores) // amostra)
    reduzido = vetores[::passo]
    sims = sorted(cosseno(reduzido[i], reduzido[j])
                  for i in range(len(reduzido))
                  for j in range(i + 1, len(reduzido)))
    if not sims:
        return 0.0
    return sims[min(len(sims) - 1, int(len(sims) * percentil / 100))]


@dataclass
class No:
    """Um nó da árvore. Folha = texto original; acima = resumo de um grupo."""

    texto: str
    nivel: int
    filhos: list[int] = field(default_factory=list)
    origem: str = ""


def agrupar(vetores: list[list[float]], *, limiar: float = 0.35,
            maximo: int = 6) -> list[list[int]]:
    """Agrupamento aglomerativo guloso por similaridade de cosseno.

    Guloso e determinístico de propósito: o RAPTOR original usa mistura de
    gaussianas com redução de dimensionalidade, que é melhor **e** traz
    dependências, aleatoriedade e hiperparâmetros. Aqui o que interessa é ver a
    árvore nascer.

    `limiar` e `maximo` são os dois hiperparâmetros que decidem a forma da
    árvore — e são exatamente os que o cap. 10 §4 aponta como problema em aberto:
    não há padrão consagrado para eles.
    """
    restantes = set(range(len(vetores)))
    grupos: list[list[int]] = []
    while restantes:
        semente = min(restantes)
        restantes.discard(semente)
        grupo = [semente]
        vizinhos = sorted(
            ((cosseno(vetores[semente], vetores[j]), j) for j in restantes),
            reverse=True,
        )
        for sim, j in vizinhos:
            if sim < limiar or len(grupo) >= maximo:
                break
            grupo.append(j)
            restantes.discard(j)
        grupos.append(grupo)
    return grupos


def resumir_extrativo(textos: list[str], *, frases: int = 2) -> str:
    """Resumo **extrativo**: escolhe as frases mais centrais do grupo.

    O RAPTOR original resume com LLM. Este resumidor pontua cada frase pela
    frequência dos termos do grupo e devolve as mais representativas.

    **A diferença importa e está declarada:** um resumo extrativo nunca produz
    uma frase que não estava lá. Ele perde a síntese — que é justamente o que dá
    ao RAPTOR o poder de responder pergunta global. Trocar por uma chamada de
    LLM é uma linha (o `LLMPort` já existe), e a etapa mede o que muda.
    """
    todas: list[str] = []
    for t in textos:
        todas.extend(f.strip() for f in re.split(r"(?<=[.!?])\s+", t) if f.strip())
    if not todas:
        return ""
    frequencia = Counter(t for texto in textos for t in normalizar(texto))
    def peso(frase: str) -> float:
        termos = normalizar(frase)
        if not termos:
            return 0.0
        # média, não soma: senão a frase mais longa ganha sempre (o mesmo
        # problema que o `b` do BM25 corrige na etapa 5).
        return sum(frequencia[t] for t in termos) / len(termos)
    melhores = sorted(todas, key=peso, reverse=True)[:frases]
    # devolve na ordem original, para o resumo continuar legível
    return " ".join(sorted(melhores, key=todas.index))


class Raptor:
    """A árvore inteira: folhas embaixo, conjunto condensado no topo."""

    def __init__(self, textos: list[str], embedder: EmbedderPort, *,
                 origens: list[str] | None = None, niveis: int = 3,
                 limiar: float | None = None, percentil: float = 90.0) -> None:
        """`limiar=None` deriva o corte do corpus (ver `limiar_por_percentil`).

        Passar um `limiar` fixo é permitido, e é o que quase todo tutorial faz —
        mas então ele é seu, e não transfere se você trocar de embedder.
        """
        self.embedder = embedder
        self.nos: list[No] = [
            No(t, nivel=0, origem=(origens[i] if origens else ""))
            for i, t in enumerate(textos)
        ]
        self.limiares: list[float] = []   # o corte usado em cada nível
        atual = list(range(len(self.nos)))

        for nivel in range(1, niveis + 1):
            if len(atual) <= 1:
                break
            vetores = [embedder.embutir(self.nos[i].texto) for i in atual]
            corte = limiar if limiar is not None else limiar_por_percentil(
                vetores, percentil)
            self.limiares.append(corte)
            grupos = agrupar(vetores, limiar=corte)
            if len(grupos) >= len(atual):
                break          # não condensou nada; parar evita árvore infinita
            proximo: list[int] = []
            for grupo in grupos:
                filhos = [atual[j] for j in grupo]
                resumo = resumir_extrativo([self.nos[f].texto for f in filhos])
                self.nos.append(No(resumo, nivel=nivel, filhos=filhos))
                proximo.append(len(self.nos) - 1)
            atual = proximo

        self.vetores = [embedder.embutir(n.texto) for n in self.nos]

    @property
    def altura(self) -> int:
        return max(n.nivel for n in self.nos)

    def por_nivel(self) -> dict[int, int]:
        return dict(sorted(Counter(n.nivel for n in self.nos).items()))

    def buscar(self, consulta: str, k: int = 5, *, nivel: int | None = None) -> list[int]:
        """Recupera **em qualquer nível** — que é o ponto do RAPTOR.

        `nivel=0` busca só nas folhas (pergunta factual). `nivel=None` busca na
        árvore inteira, deixando resumos e folhas competirem pelo mesmo `top_k`.

        Escolher o nível certo **por pergunta** é o problema em aberto do cap. 10:
        hoje se resolve por heurística, e a desta etapa é deliberadamente
        simples — é o exercício de completude.
        """
        v = self.embedder.embutir(consulta)
        candidatos = [i for i, n in enumerate(self.nos)
                      if nivel is None or n.nivel == nivel]
        notas = [(i, cosseno(v, self.vetores[i])) for i in candidatos]
        notas = [(i, s) for i, s in notas if s > 0]
        notas.sort(key=lambda kv: (-kv[1], kv[0]))
        return [i for i, _ in notas[:k]]
