# Plano 002 — Portões acionados e cadência do livro vivo

- **Spec:** [`spec.md`](spec.md)
- **Decisões:** [ADR 0013](../../adr/0013-cadencia-livro-vivo-rag.md) · [ADR 0014](../../adr/0014-autocontencao-das-etapas.md) · [ADR 0015](../../adr/0015-links-para-o-proprio-repositorio.md)
- **Data:** 2026-08-13

## Constitution Check — o portão

Conformidade com os **oito princípios** da [constituição](../../.specify/memory/constitution.md).

| # | Princípio | Como este plano o respeita | Risco residual |
|:---:|---|---|---|
| I | **Evidência acima de retórica** | É o eixo do ciclo. R7 obriga cada bullet de "Fontes da indústria" a ter URL **ou sair** — e a saída "sai" está sempre disponível, então nenhuma pressão de portão empurra para inventar fonte. O ADR 0015 aplica o mesmo princípio ao **próprio repositório**: 49 afirmações sobre onde o código está, hoje sem verificação. A contagem errada do próprio spec (32 → 30 arquivos) foi corrigida pela mesma régua. | Baixo. |
| II | **Fonte-base é a técnica reprodutível** | R7 conserta a metade da indústria; os 22 Apêndices A já trazem paper + implementação. O ADR 0013 põe a reconferência das URLs do Apêndice A como **item 1 da janela** — é o que apodrece primeiro. | Baixo. |
| III | **Método pedagógico combinado** | R8 devolve a "Leitura executiva" ao gênero *how-to* do Diátaxis (hoje é o capítulo comprimido num parágrafo — mistura de gêneros que a constituição proíbe). O ADR 0014 recupera o *fading* do 4C/ID pelo delta declarado por etapa. | Baixo. |
| IV | **Livro vivo** | É o coração do ciclo: o ADR 0013 dá cadência à tese da expiração. **A regra de ouro está no ADR:** recapturar data **só onde houve releitura**. | Médio → mitigado. A tentação de datar sem reler é exatamente o erro do ciclo 001; a checagem 3 do 0013 (nenhum capítulo com captura > 2 janelas) sangra no lugar certo sem forçar a mentira. |
| V | **Segurança** | Nenhum segredo entra em arquivo ou commit. O CI acionado (R1) não introduz credencial: build, `pytest` e scripts locais, sem chave. O `check-companion.sh` continua verificando **afirmação × realidade**, nas duas direções. | Baixo. |
| VI | **Neutralidade e acessibilidade** | Nada aqui introduz custo, GPU ou credencial para o leitor. O ADR 0014 preserva explicitamente "um comando, sem rede, sem credencial, sem dependência externa" como propriedade **testada**, não prometida. | Baixo. |
| VII | **Spec-driven e branch-per-melhoria** | spec → plan (este) → tasks → implement. As três decisões viraram ADR **antes** de virar código, como a regra 5 do ciclo 001 exige. **Desvio de branch declarado abaixo.** | Ver desvio. |
| VIII | **O escopo é o sistema** | R7 e R8 tocam conteúdo de capítulo sem mexer em escopo: nenhum capítulo muda de componente declarado. | Baixo. |

### Desvio declarado — Princípio VII (branch)

Como no ciclo 001: a constituição pede branch `NNN-nome`; a execução roda em
`claude/rag-prompt-engineering-project-d4vdak`, **fixada pelo ambiente** e não trocável sem
autorização explícita do autor. Preservados **o conteúdo** do princípio — artefatos de spec,
Constitution Check, merge único por lote. O nome da branch é a forma; o desvio fica
registrado para não ser confundido com conformidade.

### Regras impostas a esta execução

Herdadas do ciclo 001 e revalidadas:

1. **Nenhuma referência nova** entra sem passar pela skill `academic-research`. R7 se resolve
   com fonte da **indústria** (documentação oficial, post de engenharia assinado), não com
   paper novo.
2. **Quem executa não verifica.** Revisão independente em contexto fresco antes do merge.
3. **Uma entrada de `HISTORICO.md` por lote**, escrita no lote.
4. **Merge acumulado** — o merge na `main` publica (ADR 0001).
5. **Toda decisão vira ADR** antes de virar código. *(Cumprida: 0013, 0014, 0015.)*
6. **Nenhuma checagem que só passe mentindo.** Toda checagem nova deve ter uma saída honesta
   além de "ficar verde" — é a lição mais cara do ciclo 001, e está anotada no cabeçalho de
   `r2_datacao` em `../001-edicao-1-0/verificar.py`.

## Lotes, em ordem de dependência

A ordem vem do parecer: **0015 primeiro** (mecânico, fecha o ponto cego do build e destrava o
link-check que os outros usam), depois **0014** (a emenda precisa estar de pé antes de novas
etapas), depois **0013** (a cadência precisa do CI acionado para ter onde falhar).

| Lote | Entrega | Requisito | Depende de | Verificação |
|:---:|---|:---:|---|---|
| **A** | ADRs 0013–0015; 0007 → substituído; índice; contagem do spec corrigida | — | — | `adr/README.md` coerente; `grep` de "32 arquivos" vazio |
| **B** | **ADR 0015**: 49 links → relativos; `repo` em `sumario.json`; base única; bug do rodapé EN; normalização do `docs/md/`; link-check validando contra o disco | R1 | A | build verde; `grep github.com/GHDaru/rag/ livro/` → 0; `blob/` uma vez em `publicar/` |
| **C** | **ADR 0014**: constituição 3.1.0; Guia §5 e `rag-zero/README.md`; blocos de delta; `DIFF.md` gerado; `verificar_etapas.py` | R4 | A | `verificar_etapas.py` verde; 48 testes verdes; `DIFF.md` regenerado bate |
| **D** | **ADR 0013**: Guia §7 "Cadência do livro vivo" (checklist → §8); checagens de janela no verificador; job agendado | R2, R6 | A, B | `verificar.py` verde; linha `**Próxima janela: 2026-11**` única e parseável |
| **E** | Conteúdo: A3 (12 capítulos remetendo a rodada concluída) e A4 (39 → 48 testes) | R3, R4 | C | checagens novas no verificador |
| **F** | **R7 — "Fontes da indústria" com fonte.** Caps. 06, 07, 15, 22. Cada bullet ganha URL **ou sai** | R7 | A | zero bullet sem URL nos quatro capítulos |
| **G** | **R8 — "Leitura executiva" volta a ser lista de 3–5 itens.** Caps. 21, 15, 06 | R8 | A | nenhuma Leitura executiva em parágrafo único |
| **H** | Gate: revisão independente, DoD, `HISTORICO.md`, ROADMAP | — | A–G | DoD abaixo + parecer do revisor |

O lote **F** é o que decide se o livro é citável, e o mais caro. Se algum bullet não tiver
fonte que o sustente, **ele sai** — enfraquecer é conforme; inventar não é.

## Definition of Done (DoD)

Verificável por comando, sem julgamento:

```bash
cd publicar && node build.mjs && node verifica-capitulos.mjs   # build + template + link-check
cd rag-zero && python3 -m pytest tests/ -q                     # 48 testes
cd rag-zero && python3 ferramentas/verificar_etapas.py         # ADR 0014
cd chat-companion/backend && python3 -m pytest tests/ -q       # suíte do companion
python3 specs/001-edicao-1-0/verificar.py                      # R2–R8 + cadência
bash scripts/check-companion.sh                                # afirmação × realidade
```

Mais o portão humano: **o merge na `main` publica**, e autorizar execução longa não é
autorizar merge sem revisão.
