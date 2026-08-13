# Tarefas 002 — Portões acionados e cadência do livro vivo

Cada tarefa tem um **comando** que a fecha. Tarefa sem verificação não é tarefa — é intenção.

## Lote A — decisões (concluído)

- [x] **A1** ADR 0013 — cadência do livro vivo no domínio de RAG (substitui o 0007)
- [x] **A2** ADR 0014 — autocontenção das etapas: núcleo único testado, delta derivado
- [x] **A3** ADR 0015 — links para o próprio repositório
- [x] **A4** 0007 → `Substituído por 0013`, com nota de substituição preservando o texto
- [x] **A5** `adr/README.md` com os três no índice
- [x] **A6** contagem do spec corrigida (32 → 30 arquivos), com a correção declarada
- [x] **A7** `plan.md` com Constitution Check

## Lote B — ADR 0015 (links)

- [ ] **B1** `publicar/sumario.json` ganha `"repo": { "base": ..., "ref": ... }`
- [ ] **B2** `build.mjs`: `GITHUB_BASE` derivado da configuração; `ref` com fallback para `main` **e aviso no log**
- [ ] **B3** corrigir o rodapé EN (`build.mjs:78`, aponta para `harness_engineering`)
- [ ] **B4** migrar as **49 ocorrências** em 30 arquivos para caminho relativo
- [ ] **B5** normalizar os links relativos ao gravar `docs/md/*.md` (senão quebram)
- [ ] **B6** link-check: validar `repoRel` contra o disco, acumulando falhas no padrão de `quebrados`
- [ ] **B7** checagem de regressão no verificador: `github.com/GHDaru/rag/` em `livro/**.md` → zero

**Fecha com:** `node build.mjs` verde · `grep -rc "github.com/GHDaru/rag/" livro/` → 0 · `blob/` uma vez em `publicar/`

## Lote C — ADR 0014 (etapas)

- [ ] **C1** constituição: restrição 4 reescrita; versão 3.0.0 → **3.1.0**, com nota de emenda
- [ ] **C2** Guia §5 e `rag-zero/README.md` com a redação nova
- [ ] **C3** bloco "O que esta etapa acrescenta" no cabeçalho dos 9 scripts de etapa
- [ ] **C4** `rag-zero/ferramentas/diff_etapas.py` → gera `rag-zero/DIFF.md`
- [ ] **C5** `rag-zero/ferramentas/verificar_etapas.py`: execução isolada, independência por AST, delta declarado, `DIFF.md` em dia, etapa ✅ com teste

**Fecha com:** `python3 ferramentas/verificar_etapas.py` verde · 48 testes verdes

## Lote D — ADR 0013 (cadência)

- [ ] **D1** Guia: nova **§7 Cadência do livro vivo**; checklist passa a §8
- [ ] **D2** linha de formato fixo `**Próxima janela: 2026-11**`, única e parseável
- [ ] **D3** tabela dos quatro gatilhos (G1–G4)
- [ ] **D4** verificador: janela declarada · janela cumprida (aviso 30d / falha 60d) · captura ≤ 2 janelas · placar sem ⏳ vencido
- [ ] **D5** CI: job `schedule` mensal rodando as checagens de cadência

**Fecha com:** `python3 specs/001-edicao-1-0/verificar.py` verde

## Lote E — A3 e A4

- [ ] **E1** 12 capítulos: remissão a "rodada 2" (concluída) → estado presente
- [ ] **E2** "39 testes" → 48 em `rag-zero/README.md` e `ROADMAP.md`
- [ ] **E3** checagem: cruza remissão a rodada com o ✅ do ROADMAP
- [ ] **E4** checagem: conta `def test_` e compara com o número publicado

## Lote F — R7 (fontes da indústria)

- [ ] **F1** cap. 06 — cada bullet com URL **ou removido**
- [ ] **F2** cap. 07 — idem
- [ ] **F3** cap. 15 — idem
- [ ] **F4** cap. 22 — inclui *"há registro público de vulnerabilidades"* **sem identificador**: ganha o identificador ou sai
- [ ] **F5** checagem: bullet em "Fontes da indústria" sem URL → falha

> **A saída "sai" é conforme.** O Princípio I aceita enfraquecer a afirmação; o que ele não
> aceita é sustentá-la sem fonte. Nenhuma referência nova entra sem a skill `academic-research`.

## Lote G — R8 (leitura executiva)

- [ ] **G1** cap. 21 · **G2** cap. 15 · **G3** cap. 06 — parágrafo único → lista de 3–5 itens
- [ ] **G4** checagem: "Leitura executiva" com mais de N caracteres fora de lista → falha

## Lote H — gate

- [ ] **H1** DoD: as seis verificações do `plan.md`, todas verdes
- [ ] **H2** revisão independente em contexto fresco, por quem não executou
- [ ] **H3** correções do parecer
- [ ] **H4** `livro/HISTORICO.md`: entrada da edição, com o modelo de IA registrado
- [ ] **H5** `ROADMAP.md` atualizado
- [ ] **H6** merge para a `main` — **com autorização explícita do autor**
