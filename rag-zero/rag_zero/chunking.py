"""Etapa 4 — chunking e o padrão que unifica o capítulo (cap. 05).

As estratégias parecem muitas, mas quase todas são a mesma ideia:

    **desacoplar a unidade de busca da unidade de entrega.**

Indexa-se pequeno (preciso de achar) e entrega-se grande (preciso de contexto).
`sentence_window` abaixo é a materialização mais direta disso.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Chunk:
    """O que é indexado — e o que é entregue. Nem sempre a mesma coisa.

    `texto_busca` alimenta o índice; `texto_entrega` vai para o gerador. Quando
    os dois divergem, **a métrica muda de significado**: `context_precision`
    passa a medir a relevância do que foi pontuado, não do que foi enviado
    (cap. 21). Vale saber disso antes de comparar números.
    """

    texto_busca: str
    texto_entrega: str
    origem: str = ""
    secao: str = ""


def fixo(texto: str, *, tamanho: int = 400, sobreposicao: int = 80,
         origem: str = "", secao: str = "") -> list[Chunk]:
    """Corte por número de caracteres, com sobreposição. A linha de base honesta.

    Pegadinha do Apêndice A do cap. 05: em bibliotecas reais o tamanho é contado
    em **tokens do tokenizador que você passar** — trocar de modelo muda o corte
    sem ninguém perceber. Aqui é caractere, e é explícito.
    """
    passo = max(1, tamanho - sobreposicao)
    return [Chunk(texto[i:i + tamanho], texto[i:i + tamanho], origem, secao)
            for i in range(0, max(1, len(texto)), passo)
            if texto[i:i + tamanho].strip()]


def sentence_window(texto: str, *, janela: int = 2, origem: str = "",
                    secao: str = "") -> list[Chunk]:
    """Indexa a **frase**; entrega a **janela** de frases em volta dela.

    É o padrão central do capítulo em ~10 linhas: a precisão da busca vem da
    unidade pequena, e o contexto da resposta vem da unidade grande. Você não
    escolhe entre as duas — desacopla.
    """
    frases = [f.strip() for f in re.split(r"(?<=[.!?])\s+", texto) if f.strip()]
    chunks: list[Chunk] = []
    for i, frase in enumerate(frases):
        ini, fim = max(0, i - janela), min(len(frases), i + janela + 1)
        chunks.append(Chunk(frase, " ".join(frases[ini:fim]), origem, secao))
    return chunks
