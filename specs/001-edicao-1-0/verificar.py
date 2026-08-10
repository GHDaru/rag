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

SIGLAS_DEF = json.loads((RAIZ / "publicar" / "siglas.json").read_text(encoding="utf-8"))


def _limpar(texto: str) -> str:
    """Remove o que não conta como ocorrência de sigla no corpo.

    É aqui que moram os falsos positivos, e cada remoção tem motivo:

    - **blockquote de datação** — o build o APAGA da página; sigla introduzida
      ali é invisível para quem lê o site;
    - **código** (cercado e inline) — `top_k` e `ERR_4021` não são siglas;
    - **alvos de link e URLs** — `arXiv 2401.18059` não é sigla;
    - **nomes de arquivo em caixa alta** — ROADMAP, HISTORICO, CLAUDE.
    """
    texto = re.sub(r"^> \*\*Estado da arte.*?(?=\n\n)", "", texto, flags=re.S | re.M)
    texto = re.sub(r"```.*?```", "", texto, flags=re.S)
    texto = re.sub(r"`[^`]*`", "", texto)
    texto = re.sub(r"\]\([^)]*\)", "]", texto)
    texto = re.sub(r"https?://\S+", "", texto)
    texto = re.sub(r"\b(ROADMAP|HISTORICO|CLAUDE|GUIA|README|ADR|NAO_ENCONTRADO)\b", "", texto)
    return texto


def _primeiro_paragrafo_com(texto: str, sigla: str) -> str | None:
    """O parágrafo da primeira ocorrência — a unidade que o leitor percebe."""
    for par in re.split(r"\n\s*\n", texto):
        if re.search(rf"\b{re.escape(sigla)}\b", par):
            return par
    return None


def r5_siglas() -> None:
    """A política do ADR 0011 — quatro classes, uma regra cada."""
    publicados = capitulos() + [LIVRO / "apendice-tecnicas.md",
                                LIVRO / "apendice-ecossistema.md"]
    for p in publicados:
        texto = _limpar(p.read_text(encoding="utf-8"))
        rel = p.relative_to(RAIZ).as_posix()
        for sigla, d in SIGLAS_DEF.items():
            par = _primeiro_paragrafo_com(texto, sigla)
            if par is None:
                continue
            classe = d["classe"]

            # S2 — técnica: a expansão vem junto, no mesmo parágrafo.
            if classe == "tecnica" and d.get("expansao"):
                if d["expansao"].lower() not in par.lower():
                    falhas.append(f"R5/S2: {rel} usa '{sigla}' (técnica) sem a "
                                  f"expansão no mesmo parágrafo")
                elif len(re.findall(rf"\b{re.escape(sigla)}\b", texto)) == 1:
                    avisos.append(f"R5/S6: {rel} usa '{sigla}' UMA vez — "
                                  f"escreva o termo em vez da sigla")

            # S5 — núcleo expandida fora das portas canônicas é redundância.
            if classe == "nucleo" and d.get("expansao"):
                canonicos = d.get("canonicos", [])
                tem = d["expansao"].lower() in texto.lower()
                if tem and rel not in canonicos:
                    falhas.append(f"R5/S5: {rel} expande '{sigla}' fora das portas "
                                  f"canônicas — o motor já faz isso por página")
                if not tem and rel in canonicos:
                    falhas.append(f"R5/S5: {rel} é porta canônica de '{sigla}' e "
                                  f"não traz a expansão")


def r5_glossario() -> None:
    """S4 — toda sigla catalogada tem verbete. Vale para as quatro classes."""
    glossario = (LIVRO / "glossario.md").read_text(encoding="utf-8")
    usadas = set()
    for p in capitulos():
        texto = _limpar(p.read_text(encoding="utf-8"))
        for sigla in SIGLAS_DEF:
            if re.search(rf"\b{re.escape(sigla)}\b", texto):
                usadas.add(sigla)
    for sigla in sorted(usadas):
        # Sigla franca não entra no glossário: ela vive no dicionário (o motor dá
        # o tooltip), e um verbete "JSON — JavaScript Object Notation" num livro
        # de RAG é o empilhamento que o ADR 0011 combate. O glossário é para o
        # que carrega sentido NESTE livro.
        if SIGLAS_DEF[sigla]["classe"] == "franca":
            continue
        if not re.search(rf"^\*\*{re.escape(sigla)}\b", glossario, re.M) and \
           not re.search(rf"\*\*{re.escape(sigla)} ?\(", glossario):
            falhas.append(f"R5/S4: '{sigla}' é usada no livro e não tem verbete "
                          f"no glossário")


def r5_fonte_unica() -> None:
    """S7 — o motor e o verificador leem o MESMO dicionário.

    Antes do ADR 0011 havia duas listas divergentes: a de `build.mjs` (herdada do
    livro irmão, com ACP, A2A, LSP, MAST — nada disso é deste livro) e a do
    verificador. Fonte única é o que impede a divergência de voltar.
    """
    build = (RAIZ / "publicar" / "build.mjs").read_text(encoding="utf-8")
    if "siglas.json" not in build:
        falhas.append("R5/S7: build.mjs não lê publicar/siglas.json — as duas "
                      "listas voltaram a divergir")


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
                     r5_glossario, r5_fonte_unica, r6_mao_na_massa,
                     r6_sumario, r8_etapas_honestas):
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
