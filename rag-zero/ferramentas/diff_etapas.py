#!/usr/bin/env python3
"""Gera `DIFF.md` — a lição do diff entre etapas consecutivas, derivada da fonte.

    python3 ferramentas/diff_etapas.py            # grava DIFF.md
    python3 ferramentas/diff_etapas.py --conferir # falha se estiver desatualizado

**Por que isto existe** ([ADR 0014](../adr/0014-autocontencao-das-etapas.md)). O livro
irmão guarda um diretório completo por etapa, e ganha com isso um `git diff` que é
literalmente a lição do capítulo. Aqui há um núcleo único com 48 testes, porque cópia
divergente é a forma mais comum de apodrecimento — a cópia 3 se afasta da 11 e nenhum
teste percebe.

O que essa troca perdeu foi a **legibilidade do delta**, e é isso que este script
devolve. A observação que torna tudo mais simples: o delta não precisava da duplicação.
Ele é uma **função** do que cada etapa importa — e função se calcula. O que se calcula
pode ser conferido contra a fonte; o que se copia à mão, não.

O que é declarado à mão fica no cabeçalho de cada etapa (a **decisão** que ela
introduz — isso nenhuma máquina infere). O que é lido do código fica aqui. Nada é
declarado duas vezes: informação duplicada é informação que vai divergir.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ETAPAS = RAIZ / "etapas"
SAIDA = RAIZ / "DIFF.md"

DELTA_RE = re.compile(r"Delta \(ADR 0014\) — (.+?); decide: (.+?)\.\s*$", re.S)


def numero(p: Path) -> int:
    return int(re.search(r"etapa(\d+)", p.name).group(1))


def ler(p: Path) -> dict:
    """Símbolos do núcleo que a etapa usa, e a decisão que ela declara."""
    arvore = ast.parse(p.read_text(encoding="utf8"))
    modulos: dict[str, set[str]] = {}
    for no in ast.walk(arvore):
        if isinstance(no, ast.ImportFrom) and (no.module or "").startswith("rag_zero"):
            modulos.setdefault(no.module, set()).update(a.name for a in no.names)

    doc = ast.get_docstring(arvore) or ""
    m = DELTA_RE.search(doc)
    titulo = doc.splitlines()[0] if doc else p.name
    return {
        "arquivo": p,
        "n": numero(p),
        "titulo": titulo,
        "modulos": modulos,
        "vem": m.group(1) if m else None,
        "decide": " ".join(m.group(2).split()) if m else None,
    }


SECAO_RE = re.compile(r"^#\s*Etapas?\s+(\d+)(?:\s+e\s+(\d+))?\s*—", re.I)


def testes_por_etapa() -> dict[int, list[str]]:
    """Testes de cada etapa — a coluna 'Prova' do README, agora verificável.

    A fonte é a **seção** em que o teste está (`# Etapa N — ...`), não o nome dele.
    Essa escolha importa: mapear por nome convidaria a renomear teste para o portão
    ficar verde, que é a forma mais barata de mentir para um verificador. A seção
    já existia no arquivo, escrita por quem escreveu o teste — é registro, não
    adaptação ao instrumento.

    Seções transversais (Avaliação, Portas) não pertencem a etapa nenhuma e ficam
    de fora de propósito: inventar dono para elas seria estatística cosmética.
    """
    saida: dict[int, list[str]] = {}
    for arq in sorted((RAIZ / "tests").glob("test_*.py")):
        atual: list[int] = []
        for linha in arq.read_text(encoding="utf8").splitlines():
            m = SECAO_RE.match(linha.strip())
            if m:
                atual = [int(g) for g in m.groups() if g]
            elif linha.startswith("# ") and not linha.startswith("# ---"):
                atual = []          # seção transversal: sem dono
            elif linha.startswith("def test_"):
                nome = linha[4:linha.index("(")]
                for n in atual:
                    saida.setdefault(n, []).append(nome)
    return saida


def gerar() -> str:
    etapas = sorted((ler(p) for p in ETAPAS.glob("etapa*.py")), key=lambda e: e["n"])
    provas = testes_por_etapa()

    linhas = [
        "# DIFF — o que cada etapa acrescenta",
        "",
        "> **Gerado** por [`ferramentas/diff_etapas.py`](ferramentas/diff_etapas.py) a partir",
        "> do código. Não edite à mão: a próxima geração apaga. Decisão em",
        "> [ADR 0014](../adr/0014-autocontencao-das-etapas.md).",
        "",
        "No livro irmão, a lição de cada etapa está no `git diff` entre dois diretórios.",
        "Aqui o núcleo é único e testado, e o diff é **calculado**: para cada etapa, os",
        "módulos e símbolos do núcleo que ela passa a usar, mais a decisão que ela",
        "introduz — a única parte declarada à mão, porque nenhuma máquina a infere.",
        "",
        "| Etapa | Acrescenta | Decide | Prova |",
        "|:---:|---|---|---|",
    ]

    vistos: dict[str, set[str]] = {}
    detalhes = []
    for e in etapas:
        novos_mod, novos_sim = [], []
        for mod, simbolos in sorted(e["modulos"].items()):
            curto = mod.replace("rag_zero.", "")
            if mod not in vistos:
                novos_mod.append(curto)
                vistos[mod] = set()
            for s in sorted(simbolos - vistos[mod]):
                novos_sim.append(f"`{curto}.{s}`")
            vistos[mod] |= simbolos

        acrescenta = ", ".join(novos_sim) if novos_sim else "— (só recombina o que já existe)"
        prova = ", ".join(f"`{t}`" for t in sorted(provas.get(e["n"], []))) or "—"
        linhas.append(f"| **{e['n']:02d}** | {acrescenta} | {e['decide'] or '**não declarada**'} | {prova} |")

        detalhes.append(
            f"### Etapa {e['n']:02d} — {e['titulo']}\n\n"
            f"- **Vem de:** {e['vem'] or '—'}\n"
            f"- **Módulos novos:** {', '.join('`' + m + '`' for m in novos_mod) or '—'}\n"
            f"- **Rodar:** `python3 etapas/{e['arquivo'].name}`\n"
        )

    linhas += ["", "## Por etapa", ""] + detalhes
    return "\n".join(linhas).rstrip() + "\n"


def main() -> int:
    novo = gerar()
    if "--conferir" in sys.argv:
        atual = SAIDA.read_text(encoding="utf8") if SAIDA.exists() else ""
        if atual != novo:
            print("✗ DIFF.md está desatualizado — rode `python3 ferramentas/diff_etapas.py`")
            return 1
        print("✓ DIFF.md em dia")
        return 0
    SAIDA.write_text(novo, encoding="utf8")
    print(f"✓ {SAIDA.relative_to(RAIZ)} gerado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
