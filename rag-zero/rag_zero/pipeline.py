"""Etapas 1 e 2 — os dois caminhos, os quatro contratos, e o Naive RAG (caps. 02, 03).

Esta é a etapa que o livro inteiro pressupõe e que faltava: **a linha de base**.
Sem ela, toda tabela de ganho compara com nada.

O cap. 02 diz que um sistema de RAG (*Retrieval-Augmented Generation*) tem **dois
caminhos** que quase nunca rodam juntos:

- **indexação** — offline, cara, paga uma vez: aquisição → extração → chunking →
  índice;
- **consulta** — online, barata por execução, paga sempre: pergunta → candidatos
  → contexto → resposta.

E **quatro contratos** entre eles. A propriedade que os une, e que este módulo
existe para tornar verificável: **todos carregam procedência adiante**.

| # | Contrato | O que atravessa |
|:-:|---|---|
| 1 | documento → chunk | origem, seção, status, permissão |
| 2 | chunk → índice | o identificador estável do chunk |
| 3 | índice → candidato | o identificador **e** a nota |
| 4 | candidato → citação | o identificador que o leitor consegue resolver |

O `NaiveRAG` abaixo é o primeiro paradigma da taxonomia de Gao
([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)): *indexar, buscar por
similaridade, concatenar, gerar*. É a linha de base honesta — e a arquitetura da
maioria dos sistemas que se dizem avançados.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .bm25 import BM25
from .contexto import Contexto
from .geracao import Trecho, gerar
from .ingestao import Documento, filtrar_indexaveis, ingerir
from .portas import LLMPort


# --------------------------------------------------------------------------- #
# Etapa 1 — o caminho de indexação, com os contratos explícitos
# --------------------------------------------------------------------------- #

@dataclass
class Indexado:
    """Uma unidade indexada com **identificador estável** — o contrato nº 2.

    O `id` é derivado de origem + posição, não de um contador global. Isso o
    torna estável entre execuções: reindexar não renumera o corpus, e uma
    citação emitida ontem continua resolvendo hoje. Um identificador que muda a
    cada build quebra o contrato nº 4 sem que nada falhe de forma visível.
    """

    id: str
    texto: str
    origem: str
    secao: str
    status: str
    permissao: str

    @classmethod
    def de_documento(cls, doc: Documento, posicao: int) -> "Indexado":
        base = doc.origem.rsplit("/", 1)[-1].replace(".md", "")
        return cls(id=f"{base}#{posicao:04d}", texto=doc.texto, origem=doc.origem,
                   secao=doc.secao, status=doc.status, permissao=doc.permissao)


class CaminhoDeIndexacao:
    """O caminho offline: do arquivo ao índice. Pago **uma vez**.

    Separá-lo em classe própria não é cerimônia: é o que torna visível que a
    consulta **não pode** chamar nada daqui. Quando os dois caminhos se misturam
    no mesmo objeto, a primeira consequência é reindexar por requisição sem
    ninguém perceber.
    """

    def __init__(self, raiz: Path, *, subpasta: str = "livro",
                 permissao: str = "publico") -> None:
        docs, self.relatorio = ingerir(raiz, subpasta)
        # Contrato nº 1 já foi honrado pela ingestão: cada documento carrega
        # origem, seção, status e permissão. O filtro duro usa só herdado.
        docs = filtrar_indexaveis(docs, permissao=permissao)
        self.unidades = [Indexado.de_documento(d, i) for i, d in enumerate(docs)]
        self.indice = BM25([u.texto for u in self.unidades])
        self.relatorio["indexados"] = len(self.unidades)


# --------------------------------------------------------------------------- #
# Etapa 2 — o Naive RAG inteiro
# --------------------------------------------------------------------------- #

@dataclass
class Execucao:
    """O resultado de uma consulta, com tudo que é preciso para auditá-la.

    Devolver o `contexto` junto não é conveniência: é a única forma de responder
    *o que foi realmente enviado ao modelo?* (cap. 20). Um sistema que não
    consegue responder isso não consegue ser depurado.
    """

    pergunta: str
    candidatos: list[tuple[str, float]]      # (id, nota) — contrato nº 3
    contexto: Contexto
    resposta: object                         # rag_zero.geracao.Resposta


class NaiveRAG:
    """O primeiro paradigma: indexar, buscar, concatenar, gerar.

    **A linha de base do livro.** Toda técnica dos caps. 05 a 10 precisa provar
    que bate isto aqui — e o cap. 09 é explícito: aplique uma por vez, meça dos
    dois lados, e **remova o que não pagou**.

    O que ele deliberadamente **não** faz, e que os capítulos seguintes
    acrescentam: fusão com busca densa (06), reranking (07), entendimento da
    consulta (08), indexação refinada (09) e estrutura (10). O laço agêntico do
    cap. 18 também não existe: aqui o caminho é sempre o mesmo, mesmo quando a
    pergunta não pede busca nenhuma.
    """

    def __init__(self, caminho: CaminhoDeIndexacao, llm: LLMPort, *,
                 k: int = 4, orcamento: int | None = None) -> None:
        self.caminho = caminho
        self.llm = llm
        self.k = k
        self.orcamento = orcamento

    def responder(self, pergunta: str) -> Execucao:
        resultados = self.caminho.indice.buscar(pergunta, self.k)

        # Contrato nº 3: o candidato carrega o identificador E a nota. Perder a
        # nota aqui é o que impede o limiar do cap. 06 e a abstenção do cap. 15.
        candidatos = [(self.caminho.unidades[r.indice].id, r.nota) for r in resultados]

        # Contrato nº 4: o identificador chega ao gerador, e é ele que a citação
        # vai apontar. Sem isso, o cap. 15 só consegue citar de forma vaga.
        trechos = [
            Trecho(id=self.caminho.unidades[r.indice].id,
                   texto=self.caminho.unidades[r.indice].texto,
                   fonte=self.caminho.unidades[r.indice].origem)
            for r in resultados
        ]

        resposta, contexto = gerar(pergunta, trechos, self.llm,
                                   orcamento=self.orcamento)
        return Execucao(pergunta, candidatos, contexto, resposta)


def procedencia_sobreviveu(execucao: Execucao) -> bool:
    """O teste que fecha a etapa 1: **a procedência atravessou os quatro contratos?**

    Verifica que todo identificador citado na resposta existe entre os
    candidatos recuperados — ou seja, que o fio documento → chunk → índice →
    candidato → citação não arrebentou em nenhum ponto.

    Abstenção conta como sucesso: não citar nada é diferente de citar errado.
    """
    if execucao.resposta.abstem:
        return True
    ids = {i for i, _ in execucao.candidatos}
    return all(c in ids for c in execucao.resposta.citacoes)
