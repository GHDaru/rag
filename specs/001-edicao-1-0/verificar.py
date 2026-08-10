#!/usr/bin/env python3
"""Verificador dos critérios de aceite da spec 001 — a edição 1.0.

Princípio IV do método operacional: *prove, não afirme*. Cada critério da spec
vira aqui um `pass/fail` que um agente produz e um portão confere — em vez de
uma opinião sobre estar pronto.

    python3 specs/001-edicao-1-0/verificar.py

Saída: um relatório por requisito e código de saída 0 (tudo verde) ou 1.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
LIVRO = RAIZ / "livro"
EDICAO_VIGENTE = "1.0"

falhas: list[str] = []
avisos: list[str] = []


def capitulos() -> list[Path]:
    return sorted(LIVRO.glob("capitulos/*.md")) + [
        LIVRO / "00-introducao.md", LIVRO / "01-fundamentos.md",
        LIVRO / "24-convergencias.md",
    ]


# --------------------------------------------------------------------------- #
# R2 — estado coerente
# --------------------------------------------------------------------------- #

def r2_datacao() -> None:
    padrao = re.compile(r"edição (\d+\.\d+)", re.I)
    for p in capitulos():
        for m in padrao.finditer(p.read_text(encoding="utf-8")):
            if m.group(1) != EDICAO_VIGENTE:
                falhas.append(f"R2 datação: {p.relative_to(RAIZ)} declara edição "
                              f"{m.group(1)}, vigente é {EDICAO_VIGENTE}")

    readme = (RAIZ / "README.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Edição (\d+\.\d+)\*\*", readme)
    if not m or m.group(1) != EDICAO_VIGENTE:
        falhas.append(f"R2 datação: README.md declara "
                      f"{m.group(1) if m else '(nada)'}, vigente é {EDICAO_VIGENTE}")

    # A contradição que o parecer de processo encontrou: duas afirmações
    # mutuamente exclusivas sobre os Apêndices A, a 15 linhas de distância.
    if "Apêndices A" in readme:
        preenchidos = "Apêndices A estão preenchidos" in readme
        enfileirados = re.search(r"Apêndices A.{0,60}(enfileirados|não escritos)",
                                 readme, re.S)
        if preenchidos and enfileirados:
            falhas.append("R2 coerência: README.md afirma que os Apêndices A estão "
                          "preenchidos E enfileirados")


# --------------------------------------------------------------------------- #
# R3 — metadado de citação
# --------------------------------------------------------------------------- #

def r3_citacao() -> None:
    revogado = "técnica central da engenharia de contexto"
    for nome in ("CITATION.cff", ".zenodo.json"):
        p = RAIZ / nome
        if not p.exists():
            falhas.append(f"R3: {nome} não existe")
            continue
        texto = p.read_text(encoding="utf-8")
        if revogado in texto:
            falhas.append(f"R3: {nome} descreve o objeto da constituição 2.0.0 "
                          f"(revogada pelo Princípio VIII da 3.0.0)")
        if "0.1.0" in texto:
            falhas.append(f"R3: {nome} ainda declara versão 0.1.0")


# --------------------------------------------------------------------------- #
# R4 — remissões
# --------------------------------------------------------------------------- #

# O dono de cada assunto, para pegar remissão que manda ao capítulo errado.
# Só assuntos com dono inequívoco entram — a checagem precisa ser precisa, não ampla.
DONO = {
    "fundamentação": 15, "fundamentacao": 15, "abstenção": 15,
    "chunking": 5, "reranking": 7, "reranker": 7,
    "ingestão": 4, "ingestao": 4, "corpus": 4,
}


def r4_remissoes() -> None:
    # 4a — capítulo fora de faixa
    for p in capitulos() + [LIVRO / "glossario.md", LIVRO / "apendice-tecnicas.md",
                            LIVRO / "apendice-ecossistema.md"]:
        for m in re.finditer(r"caps?\. (\d{2})", p.read_text(encoding="utf-8")):
            if not (0 <= int(m.group(1)) <= 24):
                falhas.append(f"R4: {p.relative_to(RAIZ)} cita cap. {m.group(1)} "
                              f"(fora de 00–24)")

    # 4b — assunto mandado ao capítulo errado, na mesma frase
    for p in capitulos():
        for linha in p.read_text(encoding="utf-8").splitlines():
            for m in re.finditer(r"([\wçãáéíóúâêô-]+)[^.|]{0,60}?\(caps?\. (\d{2})\)",
                                 linha, re.I):
                assunto, alvo = m.group(1).lower(), int(m.group(2))
                if assunto in DONO and DONO[assunto] != alvo:
                    falhas.append(
                        f"R4: {p.relative_to(RAIZ)} manda '{assunto}' para o cap. "
                        f"{alvo:02d}; o dono é o cap. {DONO[assunto]:02d}")

    # 4c — etapa do rag-zero citada com número divergente do README da trilha
    readme = (RAIZ / "rag-zero" / "README.md").read_text(encoding="utf-8")
    mapa: dict[int, set[int]] = {}     # etapa -> capítulos que ela atende
    for m in re.finditer(r"^\| (\d+) \| (\d+)(?:–(\d+))? \|", readme, re.M):
        ini = int(m.group(2))
        fim = int(m.group(3)) if m.group(3) else ini
        mapa[int(m.group(1))] = set(range(ini, fim + 1))
    for p in capitulos():
        texto = p.read_text(encoding="utf-8")
        numero = re.match(r"(\d{2})", p.stem)
        if not numero:
            continue
        cap = int(numero.group(1))
        for m in re.finditer(r"rag-zero, etapa (\d+)", texto):
            etapa = int(m.group(1))
            if etapa in mapa and cap not in mapa[etapa]:
                donos = ", ".join(f"{c:02d}" for c in sorted(mapa[etapa]))
                falhas.append(f"R4: cap. {cap:02d} declara etapa {etapa}, que o "
                              f"README da trilha atribui ao(s) cap. {donos}")


# --------------------------------------------------------------------------- #
# R5 — siglas
# --------------------------------------------------------------------------- #

SIGLAS = {
    "RAG": "Retrieval-Augmented Generation",
    "LLM": "Large Language Model",
    "IR": "Information Retrieval",
    "OWASP": "Open Worldwide Application Security Project",
    "BM25": "Best Matching 25",
    "RRF": "Reciprocal Rank Fusion",
    "DoD": "Definition of Done",
}


def r5_siglas() -> None:
    """Lei de Ferro: a primeira ocorrência do capítulo expande a sigla.

    Verifica só a **primeira** ocorrência por arquivo — o leitor não tem
    obrigação de ter lido o capítulo anterior.
    """
    for p in capitulos():
        texto = p.read_text(encoding="utf-8")
        for sigla, extenso in SIGLAS.items():
            m = re.search(rf"\b{re.escape(sigla)}\b", texto)
            if not m:
                continue
            # A expansão precisa aparecer até o fim do parágrafo da 1ª ocorrência.
            janela = texto[:m.end() + 400]
            if extenso.lower() not in janela.lower():
                falhas.append(f"R5 sigla órfã: {p.relative_to(RAIZ)} usa '{sigla}' "
                              f"sem expandir na primeira ocorrência")


def r5_glossario() -> None:
    glossario = (LIVRO / "glossario.md").read_text(encoding="utf-8")
    for sigla in SIGLAS:
        if not re.search(rf"^\*\*{re.escape(sigla)}\b", glossario, re.M) and \
           not re.search(rf"\*\*{re.escape(sigla)} ?\(", glossario):
            avisos.append(f"R5: '{sigla}' não tem verbete próprio no glossário")


# --------------------------------------------------------------------------- #
# R6 — escada de execução visível
# --------------------------------------------------------------------------- #

def r6_mao_na_massa() -> None:
    for p in sorted(LIVRO.glob("capitulos/*.md")):
        texto = p.read_text(encoding="utf-8")
        m = re.search(r"^## Mão na massa.*?(?=^## |\Z)", texto, re.M | re.S)
        if not m:
            falhas.append(f"R6: {p.relative_to(RAIZ)} não tem seção 'Mão na massa'")
            continue
        secao = m.group(0)
        if "```" not in secao:
            falhas.append(f"R6: 'Mão na massa' de {p.relative_to(RAIZ)} não tem "
                          f"comando para rodar")
        if "rag-zero/" not in secao and "rag_zero/" not in secao:
            falhas.append(f"R6: 'Mão na massa' de {p.relative_to(RAIZ)} não aponta "
                          f"caminho de arquivo da trilha")


def r6_sumario() -> None:
    sumario = json.loads((RAIZ / "publicar" / "sumario.json").read_text(encoding="utf-8"))
    arquivos = [i["arquivo"] for parte in sumario["partes"] for i in parte["itens"]]
    if not any("rag-zero" in a for a in arquivos):
        falhas.append("R6: `rag-zero` não está em sumario.json — a espinha 4C/ID "
                      "não existe para quem lê o site")


# --------------------------------------------------------------------------- #
# R8 — nenhuma etapa não construída descrita no presente
# --------------------------------------------------------------------------- #

def r8_etapas_honestas() -> None:
    readme = (RAIZ / "rag-zero" / "README.md").read_text(encoding="utf-8")
    nao_construidas = {int(m.group(1))
                       for m in re.finditer(r"^\| (\d+) \|.*\| 🔜 \|", readme, re.M)}
    for p in sorted(LIVRO.glob("capitulos/*.md")):
        texto = p.read_text(encoding="utf-8")
        m = re.search(r"^## Mão na massa.*?(?=^## |\Z)", texto, re.M | re.S)
        if not m:
            continue
        secao = m.group(0)
        for etapa in re.findall(r"etapa (\d+)", secao):
            if int(etapa) in nao_construidas and "ainda não construída" not in secao:
                falhas.append(f"R8: {p.relative_to(RAIZ)} descreve a etapa {etapa} "
                              f"(não construída) sem declarar isso")


# --------------------------------------------------------------------------- #

def main() -> int:
    for checagem in (r2_datacao, r3_citacao, r4_remissoes, r5_siglas,
                     r5_glossario, r6_mao_na_massa, r6_sumario, r8_etapas_honestas):
        checagem()

    if avisos:
        print(f"\n⚠ {len(avisos)} aviso(s):")
        for a in avisos:
            print(f"  · {a}")

    if falhas:
        print(f"\n✗ {len(falhas)} falha(s) nos critérios de aceite:\n")
        for f in falhas:
            print(f"  · {f}")
        return 1

    print("\n✓ todos os critérios verificáveis da spec 001 passam")
    return 0


if __name__ == "__main__":
    sys.exit(main())
