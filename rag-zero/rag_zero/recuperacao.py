"""Etapas 5 e 6 — denso, fusão por posição, reranking e o caminho de abstenção.

Cobre os caps. 06 e 07. Três coisas acontecem aqui, nesta ordem:

1. **Busca densa** (`BuscaDensa`) — o outro lado do par esparso/denso.
2. **Fusão por posição** (`fundir`) — porque as notas são incomparáveis.
3. **Reranking com a nota usada como limiar** (`rerankear`) — e o caminho de
   "não encontrei", que é o que impede a alucinação fundamentada em ruído.
"""

from __future__ import annotations

from dataclasses import dataclass

from .bm25 import BM25, Resultado
from .portas import EmbedderPort, RerankerPort, cosseno


# --------------------------------------------------------------------------- #
# Denso
# --------------------------------------------------------------------------- #

class BuscaDensa:
    """Busca por similaridade de vetores. Varredura linear, de propósito.

    Um banco vetorial usaria índice aproximado. Aqui a varredura é completa —
    o que é lento e **exato**. A pegadinha do Apêndice A do cap. 06 é
    justamente o contrário disso: em produção, o índice aproximado troca
    **recall** por latência, e um recall que cai sem explicação costuma ser o
    parâmetro de busca do índice, não o modelo de embedding.

    Fazendo exato aqui, você tem uma linha de base contra a qual medir essa
    perda quando trocar por um banco de verdade.
    """

    def __init__(self, documentos: list[str], embedder: EmbedderPort) -> None:
        self.embedder = embedder
        self.vetores = [embedder.embutir(d) for d in documentos]

    def buscar(self, consulta: str, k: int = 10) -> list[Resultado]:
        v = self.embedder.embutir(consulta)
        notas = [(i, cosseno(v, vd)) for i, vd in enumerate(self.vetores)]
        notas = [(i, s) for i, s in notas if s > 0]
        notas.sort(key=lambda kv: (-kv[1], kv[0]))
        return [Resultado(i, s) for i, s in notas[:k]]


# --------------------------------------------------------------------------- #
# Fusão
# --------------------------------------------------------------------------- #

def fundir(listas: list[list[Resultado]], *, k_rrf: int = 60, k: int = 10) -> list[Resultado]:
    """Fusão recíproca de ranking — combina por **posição**, não por nota.

    O problema que ela resolve: similaridade de cosseno e pontuação BM25 vivem
    em escalas diferentes, e normalizá-las é frágil. Fundindo por posição, um
    documento bem colocado nas duas listas sobe mais que um excelente em uma só
    e ausente na outra — sem calibrar nada.

    `k_rrf` é o amortecimento. É a pegadinha registrada no Apêndice A do
    cap. 06: **o padrão 60 raramente é discutido**, e ele decide quanto peso a
    cauda recebe. Valor baixo concentra nos primeiros; valor alto achata.

    Este é um dos pontos de *completion problem* da trilha (regra 3): o
    esqueleto vem pronto, e calibrar `k_rrf` no seu corpus é seu.
    """
    acumulado: dict[int, float] = {}
    for lista in listas:
        for posicao, r in enumerate(lista, start=1):
            acumulado[r.indice] = acumulado.get(r.indice, 0.0) + 1.0 / (k_rrf + posicao)
    ordenados = sorted(acumulado.items(), key=lambda kv: (-kv[1], kv[0]))
    return [Resultado(i, nota) for i, nota in ordenados[:k]]


# --------------------------------------------------------------------------- #
# Reranking e abstenção
# --------------------------------------------------------------------------- #

@dataclass
class Recuperacao:
    """O que sai do estágio de recuperação — com o caminho de abstenção junto.

    `abstem=True` significa: nada passou do limiar, e o gerador **não deve ser
    chamado**. É o contrato do cap. 06 §4 com o cap. 15: sem ele, um corpus que
    não tem a resposta produz alucinação fundamentada em ruído, por padrão.
    """

    resultados: list[Resultado]
    abstem: bool
    motivo: str = ""


def rerankear(
    consulta: str,
    candidatos: list[Resultado],
    documentos: list[str],
    reranker: RerankerPort,
    *,
    k: int = 5,
    limiar: float = 0.15,
) -> Recuperacao:
    """Reordena os candidatos e **usa a nota** como corte, não só a ordem.

    Esta função é onde as duas metades do cap. 07 se encontram:

    - *recuperar barato, reordenar caro* — o custo é **linear em N**, e é por
      isso que o reranker vê `candidatos`, não o corpus;
    - *a nota, não só a ordem* — é o único estágio que devolve um número
      calibrável, e desperdiçá-lo é deixar a abstenção sem instrumento.

    `limiar` não tem valor universal. O padrão daqui foi calibrado no corpus
    deste livro e **não transfere** — é o segundo *completion problem* da
    trilha.
    """
    pontuados = [
        Resultado(c.indice, reranker.pontuar(consulta, documentos[c.indice]))
        for c in candidatos
    ]
    pontuados.sort(key=lambda r: (-r.nota, r.indice))
    acima = [r for r in pontuados if r.nota >= limiar][:k]

    if not acima:
        return Recuperacao([], abstem=True,
                           motivo=f"nada acima do limiar {limiar:.2f}")
    return Recuperacao(acima, abstem=False)


# --------------------------------------------------------------------------- #
# O pipeline híbrido, montado
# --------------------------------------------------------------------------- #

class RecuperadorHibrido:
    """Esparso + denso + fusão + reranking, com abstenção. Etapas 5–6 juntas.

    É o pipeline que o cap. 03 chama de **Advanced RAG**: continua linear, com
    otimizações antes e depois da busca.
    """

    def __init__(self, documentos: list[str], embedder: EmbedderPort,
                 reranker: RerankerPort) -> None:
        self.documentos = documentos
        self.esparso = BM25(documentos)
        self.denso = BuscaDensa(documentos, embedder)
        self.reranker = reranker

    def buscar(self, consulta: str, *, n_candidatos: int = 30, k: int = 5,
               limiar: float = 0.15) -> Recuperacao:
        candidatos = fundir(
            [self.esparso.buscar(consulta, n_candidatos),
             self.denso.buscar(consulta, n_candidatos)],
            k=n_candidatos,
        )
        if not candidatos:
            return Recuperacao([], abstem=True, motivo="nenhum candidato")
        return rerankear(consulta, candidatos, self.documentos, self.reranker,
                         k=k, limiar=limiar)
