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
    """Só a LINHA de datação do cabeçalho — não toda menção a uma edição.

    A primeira versão desta checagem cobrava `edição X.Y` em qualquer posição do
    arquivo. O efeito foi perverso e é a lição mais cara deste ciclo: ela **forçou
    a reescrita de fatos históricos** ("capítulo criado na edição 0.2" virou
    "criado na edição 1.0") só para ficar verde. Uma checagem que só passa
    mentindo é pior que checagem nenhuma — ela transforma o portão em pressão
    para falsificar. O revisor independente pegou; eu não teria pegado.
    """
    linha_datacao = re.compile(r"^> \*\*Estado da arte capturado.*?· edição (\d+\.\d+)",
                               re.M)
    for p in capitulos():
        for m in linha_datacao.finditer(p.read_text(encoding="utf-8")):
            if m.group(1) != EDICAO_VIGENTE:
                falhas.append(f"R2 datação: {p.relative_to(RAIZ)} declara edição "
                              f"{m.group(1)}, vigente é {EDICAO_VIGENTE}")

    # Os dois arquivos que a versão anterior NÃO cobria — e que ficaram em 0.6.
    for extra, padrao in ((RAIZ / "CLAUDE.md", r"\*\*Edição (\d+\.\d+)"),
                          (RAIZ / "rag-zero" / "README.md", r"> Edição (\d+\.\d+)")):
        m = re.search(padrao, extra.read_text(encoding="utf-8"))
        if not m or m.group(1) != EDICAO_VIGENTE:
            falhas.append(f"R2 datação: {extra.relative_to(RAIZ)} declara "
                          f"{m.group(1) if m else '(nada)'}, vigente é {EDICAO_VIGENTE}")

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
# Só assuntos com dono INEQUÍVOCO e que aparecem colados à remissão. A lista é
# curta de propósito: uma checagem precisa vale mais que uma ampla e ruidosa.
DONO = {
    "regra de fundamentação": 15, "prompt de fundamentação": 15,
    "regra de abstenção": 15, "caminho de abstenção": 6,
    "estratégia de chunking": 5, "o corte": 5,
}


def r4_remissoes() -> None:
    # 4a — capítulo fora de faixa
    for p in capitulos() + [LIVRO / "glossario.md", LIVRO / "apendice-tecnicas.md",
                            LIVRO / "apendice-ecossistema.md"]:
        for m in re.finditer(r"caps?\. (\d{2})", p.read_text(encoding="utf-8")):
            if not (0 <= int(m.group(1)) <= 24):
                falhas.append(f"R4: {p.relative_to(RAIZ)} cita cap. {m.group(1)} "
                              f"(fora de 00–24)")

    # 4b — assunto mandado ao capítulo errado.
    #
    # A primeira versão desta checagem casava da esquerda para a direita e
    # **consumia o sujeito errado**: em "prompt de fundamentação, regra de
    # abstenção (cap. 11)" ela extraía "prompt", que não está no DONO — e
    # `fundamentação` nunca chegava a ser avaliada. O caso que dá nome ao
    # requisito passava batido. Agora a busca é pelo ALVO e olha para trás,
    # varrendo todos os assuntos conhecidos na janela.
    for p in capitulos():
        texto = p.read_text(encoding="utf-8")
        for m in re.finditer(r"\(caps?\. (\d{2})(?:[,/ e]+\d{2})*\)", texto):
            alvo = int(m.group(1))
            janela = texto[max(0, m.start() - 45):m.start()].lower()
            janela = janela.rsplit("|", 1)[-1].rsplit(". ", 1)[-1]
            # Só o assunto MAIS PRÓXIMO da remissão conta. Janela larga produz
            # falso positivo: "o componente de chunking (cap. 02)" é legítimo
            # quando a frase fala do componente, não da técnica.
            candidatos = [(janela.rfind(a), a, d) for a, d in DONO.items()
                          if a in janela]
            if not candidatos:
                continue
            _, assunto, dono = max(candidatos)
            if dono == alvo or re.search(rf"\b{dono:02d}\b", m.group(0)):
                continue
            falhas.append(
                f"R4: {p.relative_to(RAIZ)} manda '{assunto}' para o cap. "
                f"{alvo:02d}; o dono é o cap. {dono:02d}")

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


def r7_artefato_concreto() -> None:
    """Nenhum capítulo prescreve uma forma sem exibir um exemplo dela.

    A checagem exige bloco de código **fora** da seção "Mão na massa" — porque o
    bloco de lá é a *invocação* (`cd rag-zero && python3 …`), não um artefato. O
    revisor independente pegou exatamente isso: 17 capítulos tinham bloco de
    código, e em todos era só o comando.
    """
    for stem in ("06-busca", "11-anatomia-do-prompt", "15-geracao-fundamentada"):
        p = LIVRO / "capitulos" / f"{stem}.md"
        texto = p.read_text(encoding="utf-8")
        corpo = re.sub(r"^## Mão na massa.*?(?=^## |\Z)", "", texto,
                       flags=re.M | re.S)
        if "```" not in corpo:
            falhas.append(f"R7: {p.relative_to(RAIZ)} prescreve uma forma sem "
                          f"exibir um exemplo dela fora da 'Mão na massa'")


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
# R3 e R4 (spec 002) — o livro não fala do repositório no tempo errado
# --------------------------------------------------------------------------- #

def r3_rodada_concluida() -> None:
    """Nenhum capítulo promete no futuro uma rodada que o ROADMAP dá por concluída.

    Era o achado A3: treze capítulos diziam "o tratamento por implementação **é a
    rodada 2 do ROADMAP**" com os 22 Apêndices A já preenchidos desde 2026-08-09. Não
    é erro de digitação — é o livro descrevendo um estado que deixou de existir, que
    é o mesmo defeito que a edição 1.0 inteira foi corrigir.
    """
    roadmap = (RAIZ / "ROADMAP.md").read_text(encoding="utf8")
    concluidas = {int(m.group(1))
                  for m in re.finditer(r"^##\s*Rodada\s+(\d+)\b[^\n]*✅", roadmap, re.M)}
    futuro = re.compile(r"(?:é|são|será|serão|fica para|ficam para)\s+a\s+rodada\s+(\d+)", re.I)
    for p in capitulos():
        for n, linha in enumerate(p.read_text(encoding="utf8").splitlines(), 1):
            for m in futuro.finditer(linha):
                if int(m.group(1)) in concluidas:
                    falhas.append(
                        f"R3: {p.relative_to(RAIZ)}:{n} remete ao futuro a rodada "
                        f"{m.group(1)}, que o ROADMAP dá por concluída")


def r4_contagem_de_testes() -> None:
    """Número de testes publicado bate com o número de testes que existem.

    Achado A4: "39 testes" no `README.md` da trilha e no ROADMAP, quando eram 48. Um
    número desatualizado é uma afirmação falsa — só que barata de conferir, e por isso
    imperdoável num livro que cobra condição experimental ao lado de cada número.
    """
    reais = sum(len(re.findall(r"^def test_", t.read_text(encoding="utf8"), re.M))
                for t in sorted((RAIZ / "rag-zero/tests").glob("test_*.py")))
    for rel in ("rag-zero/README.md", "ROADMAP.md", "CLAUDE.md", "README.md"):
        arq = RAIZ / rel
        if not arq.exists():
            continue
        for m in re.finditer(r"(\d+)\s+testes", arq.read_text(encoding="utf8")):
            if int(m.group(1)) != reais:
                falhas.append(f"R4: {rel} diz '{m.group(1)} testes'; são {reais}")


# --------------------------------------------------------------------------- #
# ADR 0013 — cadência do livro vivo
# --------------------------------------------------------------------------- #
#
# Estas quatro checagens têm uma característica que as outras não precisam ter: elas
# podem **ficar vermelhas pela passagem do tempo**, sem ninguém commitar nada. É de
# propósito — num livro cuja tese é a cláusula de expiração, o tempo é a única coisa
# que deveria conseguir quebrar o portão sozinha.
#
# E há uma armadilha desenhada de frente: cobrar data fresca sem cobrar releitura
# transforma o portão em pressão para **datar uma mentira**. Por isso a checagem de
# captura tem folga de duas janelas, e o remédio dela é reler — nunca só reescrever a
# data. É a lição do ciclo 001, anotada no cabeçalho de `r2_datacao`.

JANELA_RE = re.compile(r"^\*\*Próxima janela: (\d{4})-(\d{2})\.?\*\*", re.M)


def _mes(ano: int, mes: int) -> int:
    return ano * 12 + mes


def _hoje() -> tuple[int, int, int]:
    from datetime import date
    h = date.today()
    return h.year, h.month, h.day


def adr13_janela_declarada() -> None:
    """O Guia declara UMA próxima janela, em formato que a máquina lê."""
    guia = (LIVRO / "GUIA-EDITORIAL.md").read_text(encoding="utf8")
    achadas = JANELA_RE.findall(guia)
    if len(achadas) != 1:
        falhas.append(f"ADR 0013: o Guia deveria ter exatamente uma linha "
                      f"`**Próxima janela: AAAA-MM**`; tem {len(achadas)}")


def adr13_janela_cumprida() -> None:
    """A janela venceu e não houve edição? Aviso aos 30 dias, falha aos 60.

    A gradação existe para o repositório não ficar vermelho por um atraso de dias —
    um portão que grita cedo demais é um portão que se aprende a ignorar.
    """
    guia = (LIVRO / "GUIA-EDITORIAL.md").read_text(encoding="utf8")
    m = JANELA_RE.search(guia)
    if not m:
        return
    ano, mes = int(m.group(1)), int(m.group(2))
    hoje_a, hoje_m, hoje_d = _hoje()
    # meses decorridos desde o início da janela (aprox. suficiente: 30d ≈ 1 mês)
    atraso = _mes(hoje_a, hoje_m) - _mes(ano, mes)
    if atraso < 1:
        return

    historico = (LIVRO / "HISTORICO.md").read_text(encoding="utf8")
    cumprida = any(_mes(int(a), int(mm)) >= _mes(ano, mes)
                   for a, mm in re.findall(r"^### .*?— (\d{4})-(\d{2})-\d{2}", historico, re.M))
    if cumprida:
        return
    alvo = f"{ano}-{mes:02d}"
    if atraso >= 2:
        falhas.append(f"ADR 0013: a janela {alvo} venceu há mais de 60 dias e não há "
                      f"edição correspondente no HISTORICO — o livro vivo parou")
    else:
        avisos.append(f"ADR 0013: a janela {alvo} venceu e ainda não há edição no HISTORICO")


def adr13_captura_recente() -> None:
    """Nenhum capítulo com captura mais velha que duas janelas (6 meses).

    **O remédio é reler o capítulo**, não trocar a data. Trocar a data sem reler passa
    nesta checagem e falsifica o livro — que é exatamente o dano que o ciclo 001 sofreu
    e o motivo de a folga aqui ser generosa.
    """
    hoje_a, hoje_m, _ = _hoje()
    for p in capitulos():
        m = re.search(r"[Cc]apturado em\*{0,2}:?\s*\*{0,2}(\d{4})-(\d{2})", p.read_text(encoding="utf8"))
        if not m:
            continue
        idade = _mes(hoje_a, hoje_m) - _mes(int(m.group(1)), int(m.group(2)))
        if idade > 6:
            falhas.append(f"ADR 0013: {p.relative_to(RAIZ)} capturado em "
                          f"{m.group(1)}-{m.group(2)} — {idade} meses, mais de duas janelas. "
                          f"Releia o capítulo (trocar só a data é falsificar)")


def adr13_placar_honesto() -> None:
    """Aposta do registro de expiração com prazo vencido não fica ⏳.

    A saída honesta é o veredito — inclusive ❌. Aposta refutada não se apaga: o placar
    só vale alguma coisa se ele puder marcar contra a casa.
    """
    historico = (LIVRO / "HISTORICO.md").read_text(encoding="utf8")
    hoje_a, hoje_m, _ = _hoje()
    for linha in historico.splitlines():
        m = re.match(r"\|\s*(A\d+)\s*\|.*\|\s*(\d{4})-(\d{2})\s*\|.*\|\s*⏳", linha)
        if m and _mes(int(m.group(2)), int(m.group(3))) < _mes(hoje_a, hoje_m):
            falhas.append(f"ADR 0013: a aposta {m.group(1)} venceu em "
                          f"{m.group(2)}-{m.group(3)} e segue ⏳ — dê o veredito")


# --------------------------------------------------------------------------- #
# ADR 0015 — links para o próprio repositório
# --------------------------------------------------------------------------- #

def adr15_links_relativos() -> None:
    """Nenhum link de arquivo do repositório escrito como URL absoluta.

    O motor já converte caminho relativo na URL pública desde sempre; as 49 URLs
    absolutas que existiam contornavam esse mecanismo e, por serem externas,
    **nenhum portão as validava**. Com a forma relativa, o build confere cada uma
    contra o disco.

    A checagem mira `/blob/` — o link para um **arquivo**. A URL da raiz do
    repositório continua legítima: em `autor.md` ela é a citação bibliográfica da
    obra, não uma referência a código.
    """
    for p in sorted(LIVRO.rglob("*.md")):
        for n, linha in enumerate(p.read_text(encoding="utf8").splitlines(), 1):
            if "github.com/GHDaru/rag/blob/" in linha or "github.com/GHDaru/rag/tree/" in linha:
                falhas.append(
                    f"ADR 0015: {p.relative_to(RAIZ)}:{n} usa URL absoluta para o próprio "
                    f"repositório — use caminho relativo; o motor resolve e o build valida")


def adr15_fonte_unica() -> None:
    """A base pública do repositório vive em UM lugar no motor.

    E nenhum resíduo do fork: o rodapé da edição em inglês apontava para o
    repositório do livro irmão — bug real, encontrado ao escrever o ADR.
    """
    for arq in sorted((RAIZ / "publicar").glob("*.mjs")):
        texto = arq.read_text(encoding="utf8")
        if "harness_engineering" in texto:
            falhas.append(f"ADR 0015: {arq.relative_to(RAIZ)} referencia o repositório do "
                          f"livro irmão — resíduo do fork")
        literais = len(re.findall(r'"https://github\.com/GHDaru/rag/(?:blob|tree)/', texto))
        if literais:
            falhas.append(f"ADR 0015: {arq.relative_to(RAIZ)} tem {literais} URL(s) de "
                          f"repositório literal(is) — derive de `repo` em sumario.json")

    cfg = json.loads((RAIZ / "publicar/sumario.json").read_text(encoding="utf8")).get("repo")
    if not cfg or "base" not in cfg or "ref" not in cfg:
        falhas.append("ADR 0015: `publicar/sumario.json` sem o bloco `repo` (base + ref)")


# --------------------------------------------------------------------------- #

def main() -> int:
    for checagem in (r2_datacao, r3_citacao, r4_remissoes, r5_siglas,
                     r5_glossario, r5_fonte_unica, r6_mao_na_massa, r7_artefato_concreto,
                     r6_sumario, r8_etapas_honestas, r3_rodada_concluida, r4_contagem_de_testes,
                     adr13_janela_declarada, adr13_janela_cumprida,
                     adr13_captura_recente, adr13_placar_honesto,
                     adr15_links_relativos, adr15_fonte_unica):
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
