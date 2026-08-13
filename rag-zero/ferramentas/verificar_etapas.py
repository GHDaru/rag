#!/usr/bin/env python3
"""Portão da restrição 4 da constituição — o que o ADR 0014 promete, conferido.

    python3 ferramentas/verificar_etapas.py

A constituição dizia "etapas autocontidas" e o código fazia outra coisa. A emenda
3.1.0 separou as duas propriedades que a palavra escondia; este script confere a que
importa — **executabilidade isolada** — e a que foi recuperada — **o delta legível**.

Nenhuma destas checagens pode ser satisfeita mentindo, e isso é requisito, não
elogio: a lição mais cara do ciclo 001 foi uma checagem que **só passava se o texto
falsificasse um fato**. Aqui, cada uma tem uma saída honesta — declarar, remover,
regenerar — além de "ficar verde".
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ETAPAS = RAIZ / "etapas"

falhas: list[str] = []
avisos: list[str] = []

# O bloqueio de rede é o núcleo da checagem 1: "sem rede" tem de ser propriedade
# testada, não promessa do README. Um sitecustomize temporário derruba socket antes
# de qualquer import da etapa.
SITECUSTOMIZE = '''
import socket
class _SemRede(socket.socket):
    def __init__(self, *a, **k):
        raise OSError("etapa tentou usar a rede — a construção roda offline (restrição 4)")
socket.socket = _SemRede
socket.create_connection = lambda *a, **k: (_ for _ in ()).throw(
    OSError("etapa tentou usar a rede — a construção roda offline (restrição 4)"))
'''


def scripts() -> list[Path]:
    return sorted(ETAPAS.glob("etapa*.py"))


def c1_executavel_isoladamente() -> None:
    """Cada etapa roda sozinha: um comando, sem rede, sem credencial, e de qualquer
    diretório — sem ter executado a anterior."""
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "sitecustomize.py").write_text(SITECUSTOMIZE, encoding="utf8")
        for p in scripts():
            amb = {
                "PATH": os.environ.get("PATH", ""),
                "HOME": tmp,
                "PYTHONPATH": tmp,          # só o bloqueio de rede; nada do sistema
                "PYTHONDONTWRITEBYTECODE": "1",
            }
            r = subprocess.run([sys.executable, str(p)], cwd=tmp, env=amb,
                               capture_output=True, text=True, timeout=300)
            if r.returncode != 0:
                cauda = (r.stderr or r.stdout).strip().splitlines()[-3:]
                falhas.append(f"C1: {p.name} não roda isolada — {' / '.join(cauda)}")


def c2_independencia() -> None:
    """Nenhuma etapa importa outra etapa, e nada de fora da stdlib + `rag_zero`.

    Prova as duas coisas de uma vez: independência entre etapas e a promessa de
    zero dependência externa, que é o que mantém a trilha a custo zero (Princípio VI).
    """
    permitidos = {"rag_zero"}
    for p in scripts():
        arvore = ast.parse(p.read_text(encoding="utf8"))
        for no in ast.walk(arvore):
            nomes = []
            if isinstance(no, ast.Import):
                nomes = [a.name for a in no.names]
            elif isinstance(no, ast.ImportFrom) and no.level == 0:
                nomes = [no.module or ""]
            for nome in nomes:
                topo = nome.split(".")[0]
                if topo.startswith("etapa"):
                    falhas.append(f"C2: {p.name} importa outra etapa ({nome})")
                elif topo not in permitidos and topo not in sys.stdlib_module_names:
                    falhas.append(f"C2: {p.name} importa dependência externa ({nome})")


def c3_delta_declarado() -> None:
    """Toda etapa declara, no cabeçalho, a decisão que introduz.

    É a única parte do delta escrita à mão — o resto é lido do código. A saída
    honesta aqui é escrever a linha, e escrevê-la exige saber o que a etapa decide.
    """
    padrao = re.compile(r"Delta \(ADR 0014\) — .+?; decide: .+?\.", re.S)
    for p in scripts():
        doc = ast.get_docstring(ast.parse(p.read_text(encoding="utf8"))) or ""
        if not padrao.search(doc):
            falhas.append(f"C3: {p.name} sem a linha `Delta (ADR 0014) — ...; decide: ...`")


def c4_diff_em_dia() -> None:
    """`DIFF.md` regenerado bate com o do repositório. Diff velho não finge ser atual."""
    r = subprocess.run([sys.executable, str(RAIZ / "ferramentas/diff_etapas.py"), "--conferir"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        falhas.append("C4: DIFF.md desatualizado — rode `python3 ferramentas/diff_etapas.py`")


def c5_prova_por_etapa() -> None:
    """Etapa marcada ✅ no README tem teste, e a contagem publicada bate com a real.

    A parte da contagem é **falha**: número errado no README é afirmação falsa, e o
    conserto é trocar o número. A parte da prova é **aviso**: nem toda etapa tem hoje
    um teste próprio, e o remédio é escrever o teste — não renomear os que existem
    para o portão calar.
    """
    sys.path.insert(0, str(RAIZ / "ferramentas"))
    from diff_etapas import testes_por_etapa  # noqa: E402

    provas = testes_por_etapa()
    readme = (RAIZ / "README.md").read_text(encoding="utf8")

    reais = sum(len(re.findall(r"^def test_", t.read_text(encoding="utf8"), re.M))
                for t in sorted((RAIZ / "tests").glob("test_*.py")))
    for m in re.finditer(r"(\d+)\s+testes", readme):
        if int(m.group(1)) != reais:
            falhas.append(f"C5: README diz {m.group(1)} testes; são {reais}")

    concluidas = {int(m.group(1))
                  for m in re.finditer(r"^\|\s*(\d+)\s*\|.*\|\s*✅\s*\|", readme, re.M)}
    sem_prova = sorted(n for n in concluidas if not provas.get(n))
    if sem_prova:
        avisos.append(f"C5: etapas ✅ sem teste que as nomeie: {sem_prova} — "
                      f"escreva o teste; não renomeie os existentes")


def main() -> int:
    for checagem in (c1_executavel_isoladamente, c2_independencia, c3_delta_declarado,
                     c4_diff_em_dia, c5_prova_por_etapa):
        checagem()

    if avisos:
        print(f"⚠ {len(avisos)} aviso(s):")
        for a in avisos:
            print(f"  · {a}")

    if falhas:
        print(f"\n✗ {len(falhas)} falha(s) na restrição 4 (ADR 0014):\n")
        for f in falhas:
            print(f"  · {f}")
        return 1

    print(f"\n✓ {len(scripts())} etapas: executáveis isoladamente, independentes, "
          f"com delta declarado e DIFF.md em dia")
    return 0


if __name__ == "__main__":
    sys.exit(main())
