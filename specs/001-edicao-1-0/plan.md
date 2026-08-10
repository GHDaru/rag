# Plano 001 — Edição 1.0

- **Spec:** [`spec.md`](spec.md) · **Decisões:** [ADR 0009](../../adr/0009-escopo-da-edicao-1-0.md), [ADR 0010](../../adr/0010-chat-companion-na-1-0.md)
- **Data:** 2026-08-09

## Constitution Check — o portão

Conformidade com os **oito princípios** da [constituição](../../.specify/memory/constitution.md).
Este é o lugar físico onde a conformidade é verificada; sem ele, o ciclo não tem portão.

| # | Princípio | Como este plano o respeita | Risco residual |
|:---:|---|---|---|
| I | **Evidência acima de retórica** | R9 exige **zero afirmação do corpo apoiada em fonte não-✓**. Regra imposta ao run: **nenhuma referência nova entra durante a execução autônoma** — o precedente da citação inventada no PDF do RAGAS (registrado no `HISTORICO.md`) mostra que resumo automático de fonte não é validação. Só se consome o que já é ✓; o resto é enfraquecido. | Baixo. A saída "enfraquecer a afirmação" está sempre disponível e é conforme. |
| II | **Fonte-base é a técnica reprodutível** | Os 22 Apêndices A já trazem paper **+** implementação com URL conferida. R7 acrescenta o que faltava do lado do leitor: o **artefato concreto** no corpo. | Baixo. |
| III | **Método pedagógico combinado** | R6 e R8 atacam a quebra central do parecer didático: a espinha 4C/ID existe e é **invisível**. Ligar capítulo ↔ etapa e construir a etapa 2 (a única *learning task* que entrega um sistema inteiro cedo) restaura a escada. | Médio: 10 de 17 etapas seguem não construídas. Mitigado por R8 (declarar, nunca fingir). |
| IV | **Livro vivo** | R2 (datação coerente) e R10 (entrada 1.0 no `HISTORICO.md` com modelo e sessão). **Uma entrada por lote mergeado**, escrita no momento do lote — não reconstruída no fim. | Baixo. |
| V | **Segurança** | Nenhum segredo entra em arquivo ou commit. O ADR 0010 remove a pressão de deploy, que era justamente o vetor que exigiria credencial. Conteúdo recuperado segue tratado como dado, nunca instrução — e o `rag-zero` codifica isso (`Contexto.montar()` delimita bloco externo). | Baixo. |
| VI | **Neutralidade e acessibilidade** | O `rag-zero` roda **sem dependência externa, sem GPU e sem credencial** — verificado. Nenhum item da 1.0 introduz custo para o leitor. | Baixo. |
| VII | **Spec-driven e branch-per-melhoria** | Este ciclo restabelece o rastro: `specs/001-edicao-1-0/` + ADRs deste projeto a partir do 0009. **Desvio declarado abaixo.** | Ver desvio. |
| VIII | **O escopo é o sistema** | R3 corrige o metadado de citação, que descrevia o objeto revogado. `CLAUDE.md` passa a resumir a redação 3.0.0. | Baixo. |

### Desvio declarado — Princípio VII (branch)

A constituição pede branch `NNN-nome`. Este ciclo roda na branch
`claude/rag-prompt-engineering-project-d4vdak`, **fixada pelo ambiente de execução** e
que não pode ser trocada sem autorização explícita do autor.

Mitigação aplicada: os artefatos de spec (`spec.md`, `plan.md`, `tasks.md`), o
Constitution Check e o merge único por lote são preservados — que é **o conteúdo** do
princípio. O nome da branch é a **forma**. O desvio fica registrado aqui para não ser
confundido com conformidade.

### Regras impostas a esta execução longa

Vindas do parecer de processo, e vinculantes:

1. **Nenhuma referência nova** durante o run autônomo. Só fontes já ✓.
2. **Quem executa não verifica.** Cada lote passa por agente revisor em **contexto
   fresco**, distinto de quem produziu.
3. **Uma entrada de `HISTORICO.md` por lote**, escrita no lote.
4. **Merge acumulado**, não contínuo — o merge na `main` publica (ADR 0001).
5. **Toda decisão vira ADR** antes de virar código.

## Lotes, em ordem de dependência

O item 0 é portão: nada abaixo começa antes dele.

| Lote | Entrega | Depende de | Verificação |
|:---:|---|---|---|
| **A** | spec + plan + tasks + ADRs 0009/0010; coerência de estado (datação, `README.md`, `CITATION.cff`, `.zenodo.json`, `CLAUDE.md`, README do companion) | — | `grep` de edição antiga vazio; sem contradição no README |
| **B** | remissões corretas; siglas expandidas + verbetes; página "Como ler este livro" | A | script de verificação de remissão e de sigla |
| **C** | artefato concreto por capítulo; "Mão na massa" com arquivo/comando/saída; `rag-zero` no sumário | A | build verde; toda "Mão na massa" com bloco de código |
| **D** | `rag-zero`: etapas 1, 2, 7, 8 e 14 completa; etapas restantes declaradas | A | suíte verde e ampliada |
| **E** | evidência: zero afirmação do corpo em fonte não-✓ | A | `grep` de `[a validar]` cruzado com o corpo |
| **F** | gate: revisão independente, DoD, `HISTORICO.md` 1.0, ROADMAP | A–E | build + link-check + duas suítes verdes; parecer do revisor |

## Definition of Done (DoD)

Verificável por comando, sem julgamento:

```bash
cd publicar && node build.mjs && node verifica-capitulos.mjs   # build + template
cd rag-zero && python3 -m pytest tests/ -q                     # suíte da trilha
cd chat-companion/backend && python3 -m pytest tests/ -q       # suíte do companion
python3 specs/001-edicao-1-0/verificar.py                      # R2, R4, R5, R6
```

Mais o portão humano: **o merge na `main` publica**, e autorizar execução longa não é
autorizar merge sem revisão.
