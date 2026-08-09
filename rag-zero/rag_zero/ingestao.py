"""Etapa 3 — ingestão e governança do corpus (cap. 04).

A etapa que vem **antes** de qualquer busca, porque é ela que define o teto de
tudo que vem depois: você só recupera o que está no índice, do jeito que foi
colocado lá.

O que este módulo implementa, na ordem do pipeline do capítulo:

    aquisição → extração → normalização → deduplicação → enriquecimento

E o que ele **prova**, no teste que fecha a etapa: um documento marcado como
`revogado` não é recuperado, mesmo sendo o mais similar à consulta. Um índice
que não sabe disso não é índice — é uma pilha de texto.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable, Literal

Status = Literal["vigente", "revogado", "rascunho"]
Procedencia = Literal["herdado", "derivado", "gerado"]


@dataclass
class Documento:
    """Um documento com o metadado mínimo do cap. 04.

    Cada campo existe porque **habilita uma decisão**. Se não habilita decisão
    nenhuma, não é metadado — é peso morto, e não deveria estar aqui.
    """

    origem: str                       # citar a fonte; invalidar em bloco
    texto: str
    data: date | None = None          # filtrar por vigência; ordenar versões
    status: Status = "vigente"        # NÃO recuperar o revogado
    secao: str = ""                   # reconstruir o contexto do trecho
    permissao: str = "publico"        # filtrar ANTES de buscar (cap. 22)
    # Metadado gerado por modelo vive separado, com a confiança ao lado.
    # A regra do cap. 04: o gerado **impulsiona, nunca filtra de forma dura**.
    gerado: dict[str, tuple[str, float]] = field(default_factory=dict)

    @property
    def hash(self) -> str:
        """Derivado: deduplicar, e detectar mudança sem reprocessar."""
        return hashlib.sha256(self.texto.encode("utf-8")).hexdigest()[:16]


# --------------------------------------------------------------------------- #
# Extração e normalização
# --------------------------------------------------------------------------- #

def extrair_markdown(caminho: Path, raiz: Path) -> list[Documento]:
    """Extrai um Markdown em documentos por seção (cabeçalho).

    A etapa mais subestimada do pipeline é justamente esta. Aqui ela é fácil
    porque a fonte é Markdown — estruturado, previsível, nosso. Com PDF, a
    extração é onde a informação morre em silêncio, e **nenhuma métrica do
    cap. 21 detecta isso**: `context recall` mede se o chunk certo veio, não se
    o chunk certo faz sentido.

    Por isso a verificação de maior retorno do capítulo não é automatizável:
    ler uma amostra do extraído, com olhos humanos.
    """
    try:
        bruto = caminho.read_text(encoding="utf-8")
    except OSError:
        return []

    rel = caminho.relative_to(raiz).as_posix()
    docs: list[Documento] = []
    secao = caminho.stem
    buffer: list[str] = []

    def fechar() -> None:
        corpo = normalizar_texto(" ".join(buffer))
        if len(corpo) > 40:
            docs.append(Documento(origem=rel, texto=corpo, secao=secao))

    for linha in bruto.splitlines():
        if linha.startswith("#"):
            fechar()
            buffer = []
            secao = linha.lstrip("#").strip()
        elif linha.strip():
            buffer.append(linha.strip())
        else:
            fechar()
            buffer = []
    fechar()
    return docs


def normalizar_texto(texto: str) -> str:
    """Limpeza conservadora: espaço em excesso e ruído de marcação.

    "Conservadora" é decisão, não preguiça. Normalizar de menos deixa ruído em
    todo chunk; normalizar de mais **apaga a estrutura** que a etapa 4 vai usar
    para cortar. Na dúvida, tire menos.
    """
    texto = re.sub(r"`{1,3}", "", texto)
    texto = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", texto)   # link -> só o rótulo
    texto = re.sub(r"[*_>|]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


# --------------------------------------------------------------------------- #
# Deduplicação
# --------------------------------------------------------------------------- #

def deduplicar(docs: Iterable[Documento]) -> tuple[list[Documento], int]:
    """Remove idênticos por hash. Devolve (mantidos, removidos).

    **A pegadinha do Apêndice A, implementada como comentário porque é onde ela
    morde:** o quase-idêntico costuma ser *versão diferente*, não duplicata.
    Deduplicar por similaridade sem olhar `data` e `status` apaga a atualização
    e mantém a revogada — que é o pior resultado possível deste módulo.

    Por isso aqui a deduplicação é **só por hash exato**. O quase-idêntico é
    problema de política de versão (abaixo), não de limpeza.
    """
    vistos: set[str] = set()
    mantidos: list[Documento] = []
    removidos = 0
    for d in docs:
        if d.hash in vistos:
            removidos += 1
            continue
        vistos.add(d.hash)
        mantidos.append(d)
    return mantidos, removidos


# --------------------------------------------------------------------------- #
# Enriquecimento — a camada cara e rendosa
# --------------------------------------------------------------------------- #

_PADROES_REVOGACAO = (
    re.compile(r"\brevogad[oa]\b", re.I),
    re.compile(r"\bsubstitu[ií](?:da|do|\s+pela?)\b", re.I),
    re.compile(r"\bsem\s+efeito\b", re.I),
)


def extrair_vigencia(doc: Documento) -> tuple[Status, float]:
    """Lê o status da **prosa** — metadado gerado, com confiança ao lado.

    É o campo que evita o incidente nº 1 do cap. 04 (responder com política
    revogada), e frequentemente ele só existe no texto corrido.

    Note o tipo de retorno: `(valor, confiança)`. Um campo sem a confiança do
    extrator é uma afirmação sem procedência — exatamente o que o cap. 02 diz
    para não fazer nas fronteiras.
    """
    for padrao in _PADROES_REVOGACAO:
        if padrao.search(doc.texto):
            return "revogado", 0.8
    return "vigente", 0.3   # confiança baixa: ausência de sinal não é prova


def enriquecer(doc: Documento) -> Documento:
    """Aplica os geradores disponíveis, **sem sobrescrever o herdado**.

    A ordem importa e é a do capítulo: herdado e derivado mandam; o gerado
    entra só onde não havia nada, e sempre com a confiança registrada.
    """
    status, confianca = extrair_vigencia(doc)
    doc.gerado["status_extraido"] = (status, confianca)
    return doc


# --------------------------------------------------------------------------- #
# O filtro — e a razão de ele existir
# --------------------------------------------------------------------------- #

def filtrar_indexaveis(docs: Iterable[Documento], *, permissao: str = "publico") -> list[Documento]:
    """O que pode ser recuperado. **Filtro duro só com herdado e derivado.**

    Esta função é a materialização da regra mais importante do cap. 04:

        Metadado **ausente** faz o sistema recuperar demais — e você percebe.
        Metadado **errado** faz o documento certo sumir **antes** da busca,
        sem deixar rastro no log.

    Por isso `doc.gerado` **não** é consultado aqui. O `status_extraido` que o
    `enriquecer()` produziu serve para ordenar e impulsionar, ou para entrar
    numa fila de revisão humana — nunca para excluir candidato.
    """
    return [d for d in docs
            if d.status == "vigente" and d.permissao == permissao]


def ingerir(raiz: Path, subpasta: str = "livro") -> tuple[list[Documento], dict]:
    """O pipeline inteiro, com o relatório que quase ninguém coleta.

    Os quatro números do relatório são os do cap. 04 §7 — os que costumam não
    ter painel nenhum. Coletá-los custa quase nada e revela o que a ingestão
    está perdendo em silêncio.
    """
    base = Path(raiz) / subpasta
    docs: list[Documento] = []
    for arquivo in sorted(base.rglob("*.md")):
        docs.extend(extrair_markdown(arquivo, Path(raiz)))

    docs, duplicados = deduplicar(docs)
    docs = [enriquecer(d) for d in docs]

    relatorio = {
        "documentos": len(docs),
        "duplicados_removidos": duplicados,
        "fontes": len({d.origem for d in docs}),
        "marcados_revogados_pelo_extrator": sum(
            1 for d in docs if d.gerado.get("status_extraido", ("", 0))[0] == "revogado"
        ),
    }
    return docs, relatorio
