"""Índice de busca no texto do livro — sem dependências, sem rede.

O tutor responde do livro (Princípio I: evidência). Este módulo carrega os
Markdown de `livro/`, quebra em blocos por cabeçalho/parágrafo e ranqueia com
**BM25 Okapi** — o mesmo da etapa 5 do `rag-zero`, reimplementado aqui porque o
companion precisa ser deployável sozinho, sem o repositório completo.

**Correção registrada (rodada 3).** Até a edição 0.4 este módulo pontuava por
**sobreposição crua de termos** e se descrevia como "o BM25 do rag-zero". Não
era: faltavam as três correções que fazem BM25 funcionar — IDF (termo raro vale
mais), saturação de frequência e normalização por comprimento. Sem elas, o
ranking favorecia bloco longo e tratava "sistema" como igual a "RAPTOR".

**Correção da afirmação (ADR 0010).** O livro atribuía a este serviço uma
condição que ele não tinha, em dois sentidos: nenhum módulo daqui importa
`rag_zero` — o que existe é uma **reimplementação** do mesmo BM25 — e não há
instância pública. A paridade com `rag_zero/bm25.py` passou a ser fixada por
**teste**, não por promessa: ver `test_bm25_paridade_com_rag_zero`.

A versão canônica, comentada etapa a etapa, está em `rag-zero/rag_zero/bm25.py`.
Fusão com busca densa e reranking entram nas etapas 5–6 desta mesma rodada.
"""

from __future__ import annotations

import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Optional

_STOP = set("de da do das dos a o e que em para com sem por no na nos nas um uma os as "
            "se ao à é são como mais ou seu sua the of to and in is a an".split())


def _norm(txt: str) -> list[str]:
    txt = unicodedata.normalize("NFD", txt.lower())
    txt = "".join(c for c in txt if unicodedata.category(c) != "Mn")
    return [t for t in re.findall(r"[a-z0-9]+", txt) if t not in _STOP and len(t) > 2]


class BookIndex:
    K1 = 1.5
    B = 0.75

    def __init__(self, repo_root: Path, corpus_path: Optional[Path] = None) -> None:
        """Carrega do `corpus.json` empacotado se existir (caso do container
        isolado); senão varre `livro/` ao vivo (dev / repo completo)."""
        self.blocos: list[dict] = []
        if corpus_path and Path(corpus_path).exists():
            self._carregar_corpus(Path(corpus_path))
        elif (Path(repo_root) / "livro").is_dir():
            self._carregar(repo_root)
        self._indexar()

    def _indexar(self) -> None:
        """Índice invertido + IDF pré-computado. Etapa 5 do rag-zero."""
        self.invertido: dict[str, dict[int, int]] = {}
        self.tamanhos: list[int] = []
        for i, b in enumerate(self.blocos):
            termos = b["termos"]
            self.tamanhos.append(len(termos))
            for termo, freq in Counter(termos).items():
                self.invertido.setdefault(termo, {})[i] = freq
        n = len(self.blocos)
        self.tamanho_medio = (sum(self.tamanhos) / n) if n else 0.0
        self.idf = {
            termo: math.log(1 + (n - len(post) + 0.5) / (len(post) + 0.5))
            for termo, post in self.invertido.items()
        }

    def _carregar_corpus(self, path: Path) -> None:
        try:
            dados = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        for b in dados:
            self.blocos.append({"fonte": b["fonte"], "titulo": b["titulo"], "texto": b["texto"],
                                "termos": _norm(b["titulo"] + " " + b["texto"])})

    def exportar(self, path: Path) -> int:
        """Grava o corpus (sem os termos — recomputados no load) para empacotar."""
        dados = [{"fonte": b["fonte"], "titulo": b["titulo"], "texto": b["texto"]}
                 for b in self.blocos]
        Path(path).write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        return len(dados)

    def _carregar(self, repo_root: Path) -> None:
        fontes = sorted(f for f in (repo_root / "livro").rglob("*.md")
                        if "en" not in f.relative_to(repo_root / "livro").parts[:1])
        comp = repo_root / "benchmark" / "comparativo.md"
        if comp.exists():
            fontes.append(comp)
        for f in fontes:
            try:
                texto = f.read_text(encoding="utf-8")
            except OSError:
                continue
            rel = f.relative_to(repo_root).as_posix()
            titulo_atual = f.stem
            buffer: list[str] = []

            def flush():
                if buffer:
                    corpo = " ".join(buffer).strip()
                    if len(corpo) > 40:
                        self.blocos.append(
                            {"fonte": rel, "titulo": titulo_atual, "texto": corpo,
                             "termos": _norm(titulo_atual + " " + corpo)})

            for linha in texto.splitlines():
                if linha.startswith("#"):
                    flush()
                    buffer = []
                    titulo_atual = linha.lstrip("#").strip()
                elif linha.strip():
                    buffer.append(linha.strip())
                else:
                    flush()
                    buffer = []
            flush()

    def buscar(self, query: str, k: int = 4) -> list[dict]:
        """BM25 Okapi. Devolve os k melhores blocos, com fonte para citação."""
        notas: dict[int, float] = {}
        for termo in _norm(query):
            postings = self.invertido.get(termo)
            if not postings:
                continue
            idf = self.idf[termo]
            for i, freq in postings.items():
                norma = 1 - self.B + self.B * (
                    self.tamanhos[i] / (self.tamanho_medio or 1))
                notas[i] = notas.get(i, 0.0) + idf * (freq * (self.K1 + 1)) / (
                    freq + self.K1 * norma)
        ordenados = sorted(notas.items(), key=lambda kv: (-kv[1], kv[0]))
        return [{"fonte": self.blocos[i]["fonte"],
                 "titulo": self.blocos[i]["titulo"],
                 "trecho": self.blocos[i]["texto"][:600]}
                for i, _ in ordenados[:k]]
