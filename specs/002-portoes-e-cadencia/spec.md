# Spec 002 — Portões acionados e cadência do livro vivo

- **Status:** em implementação
- **Data:** 2026-08-09
- **Origem:** auditoria comparativa com o livro irmão *Engenharia de Harness*, em contexto fresco

## O QUÊ

Fazer os portões que a 1.0 construiu **serem acionados**, e dar ao livro vivo a
**cadência** que a tese dele exige.

## O PORQUÊ

A edição 1.0 fechou coerente. A auditoria comparativa mostrou que ela fechou **frágil**:
os portões existem e ninguém os aciona; e o livro cuja tese central é a cláusula de
expiração não tem política de quando expira.

Cada achado abaixo foi **verificado por comando** antes de entrar aqui.

| # | Achado | Evidência verificada |
|:---:|---|---|
| A1 | **O CI não roda nenhum portão.** `publicar.yml` faz `npm ci` → `build` → `pdf` → deploy. Não roda `verificar.py`, não roda os 48 testes, não roda `check-companion.sh`. E `rag-zero/**` não está nos `paths` do gatilho | `grep "run:" .github/workflows/publicar.yml` |
| A2 | **O ADR 0007 está "Aceito" e nunca foi implementado.** Ele manda o Guia Editorial ganhar a seção "Cadência do livro vivo"; ela não existe. O harness tem | `grep -c "Cadência" livro/GUIA-EDITORIAL.md` → **0**; no harness → **1** |
| A3 | **12 capítulos remetem à rodada 2**, concluída em 2026-08-09, com o Apêndice A já preenchido | 12 arquivos |
| A4 | **"39 testes"** no `rag-zero/README.md` e no `ROADMAP.md`; são **48** | `grep -c "^def test_"` → 48 |
| A5 | **`top_k` órfão**: 29 ocorrências nos capítulos, **zero verbete** no glossário. É o parâmetro mais citado do livro | contagem direta |
| A6 | **Edição fossilizada** em arquivos que o R2 não cobre: `GUIA-EDITORIAL.md` e `benchmark/README.md` em "Edição 0.1", e a skill `academic-research` afirmando *"nenhuma referência tem status ✓"* — **falso**, são 42 | `sed -n '5p'`; `grep` na skill |
| A7 | **"Fontes da indústria" sem fonte.** Caps. 06, 07, 15 e 22 têm bullets sem URL. O 22 diz *"há registro público de vulnerabilidades"* **sem um identificador**. Densidade: harness 9,2 links externos/cap; RAG ~6,8 | contagem de links |
| A8 | **"Leitura executiva" virou o capítulo comprimido.** Harness ~600 caracteres em lista; RAG 1.050–1.500 num parágrafo único com 6–8 marcadores | medição direta |

**A causa comum de A1 a A6:** o portão existe e não é acionado, ou a decisão existe e não
foi executada. **A7 e A8 são de conteúdo**, e A7 é a que decide se o livro é citável.

## Requisitos e critérios de aceite

| # | Requisito | Critério verificável |
|:---:|---|---|
| R1 | O CI aciona os portões | `publicar.yml` roda `verificar.py`, `pytest` das duas suítes e `check-companion.sh`; `rag-zero/**` nos `paths` |
| R2 | O livro vivo tem cadência declarada | seção no Guia com a **próxima janela datada** e o gatilho extraordinário adaptado ao domínio |
| R3 | Nenhum capítulo remete a rodada concluída | checagem nova no verificador: cruza remissão a rodada com o ✅ do ROADMAP |
| R4 | Números do repositório batem com o repositório | checagem nova: conta `def test_` e compara com README e ROADMAP |
| R5 | Sem jargão órfão | `top_k` e `recall@k` com verbete e definição na primeira ocorrência |
| R6 | Datação coerente em **todo** arquivo publicado | R2 do verificador ampliado para `livro/*.md`, `benchmark/`, `.claude/skills/**` |
| R7 | "Fontes da indústria" com fonte | cada bullet ganha URL **ou** sai. Prioridade: 06, 07, 15, 22 |
| R8 | "Leitura executiva" volta a ser *how-to* | lista de 3–5 itens, não parágrafo. Prioridade: 21, 15, 06 |

## Fora de escopo

Medição própria (rodada 4) · catálogo exaustivo (rodada 5) · Radar (6) · inglês (7) · DOI ·
deploy do companion · etapas 11–13, 15–16 da trilha.

## Decisões que precisam de ADR antes da implementação

1. **Cadência do livro vivo no domínio de RAG** — o ADR 0007 herdado tem gatilho de
   "re-sync de forks", que não existe aqui. Precisa de política própria.
2. **Autocontenção das etapas** — a constituição exige "etapas autocontidas"; o `rag-zero`
   trocou 13 diretórios independentes por pacote compartilhado + 48 testes. A troca é
   defensável e **não está registrada**.
3. **Convenção de links para o repositório** — 49 URLs absolutas (em 30 arquivos) com
   `main` codificado, que o link-check não valida. A convenção não está escrita em lugar
   nenhum.

**As três decisões estão tomadas:** [ADR 0013](../../adr/0013-cadencia-livro-vivo-rag.md),
[ADR 0014](../../adr/0014-autocontencao-das-etapas.md) e
[ADR 0015](../../adr/0015-links-para-o-proprio-repositorio.md). Ordem de implementação:
**0015 → 0014 → 0013**.

> **Correção de contagem (2026-08-13).** Este spec registrou "49 URLs absolutas em **32**
> arquivos". A contagem conferida é **49 ocorrências em 30 arquivos**: o número de
> ocorrências estava certo, o de arquivos não. A regra de evidência (Princípio I) vale
> também para o texto do processo.
