# Spec 001 — Edição 1.0 do livro *Engenharia de RAG*

- **Status:** em implementação
- **Data:** 2026-08-09
- **Decisão de escopo:** [ADR 0009](../../adr/0009-escopo-da-edicao-1-0.md)

## O QUÊ

Fechar a **primeira versão** do livro: uma edição em que o que o livro **afirma** e o que
o livro **entrega** coincidem, e em que o leitor consegue **construir**, não só decidir.

## O PORQUÊ

Dois pareceres independentes, em contexto fresco, chegaram à mesma causa por caminhos
diferentes — e suas acusações foram verificadas uma a uma no repositório antes de virarem
plano:

| Origem | Diagnóstico | Evidência verificada |
|---|---|---|
| Processo | incoerência de **estado** | `README.md` anunciava "Edição 0.2" com a vigente em 0.6, e se contradizia em duas linhas sobre os Apêndices A; 29 cabeçalhos de capítulo com edição errada; `CITATION.cff` descrevendo o objeto da constituição revogada |
| Processo | ausência de **rastro** | `specs/` inexistente; `feature.json` apontando para spec do livro irmão; nenhum ADR deste projeto; nenhum `plan.md` — logo, **nenhum Constitution Check** em cinco edições |
| Didática | incoerência de **promessa** | 20 dos 25 capítulos sem um único bloco de código; o cap. 15 prescreve o prompt de fundamentação e nunca o mostra; `rag-zero` ausente de `sumario.json`; nove capítulos descrevem no presente etapas não construídas |
| Didática | vazão de **navegação** | *Retrieval-Augmented Generation* (RAG) nunca expandida no corpo dos caps. 00–01; `top_k` usado ~20 vezes sem definição; a tabela de diagnóstico do cap. 21 remete ao capítulo errado |

## Requisitos e critérios de aceite

Cada requisito tem um critério **verificável** — um `pass/fail` que um agente produz e um
portão confere (Princípio IV do método: *prove, não afirme*).

| # | Requisito | Critério de aceite (verificável) |
|:---:|---|---|
| R1 | Rastro de processo restabelecido | `specs/001-edicao-1-0/` com `spec.md`, `plan.md` (com Constitution Check) e `tasks.md`; `feature.json` apontando para spec existente |
| R2 | Estado coerente | zero ocorrência de edição desatualizada em cabeçalho de capítulo; `README.md` sem afirmação contraditória; `grep` de edição antiga retorna vazio |
| R3 | Metadado de citação correto | `CITATION.cff` e `.zenodo.json` descrevem o objeto da constituição 3.0.0, com versão `1.0.0` |
| R4 | Remissões corretas | zero remissão de capítulo apontando para o capítulo errado; zero remissão de etapa do `rag-zero` com número divergente do `README.md` da trilha |
| R5 | Siglas sem órfã | toda sigla expandida na **primeira ocorrência do capítulo** e presente no glossário — verificado por script |
| R6 | Escada de execução visível | todo "Mão na massa" com **caminho de arquivo, comando e saída esperada**; `rag-zero` presente em `sumario.json` |
| R7 | Concreto onde há prescrição | nenhum capítulo prescreve uma forma sem exibir um exemplo dela; prioridade nos caps. 06, 11 e 15 |
| R8 | Piso da trilha construído | etapas 1, 2, 7, 8 e 14 executáveis com teste; etapas não construídas **declaradas** como especificadas, nunca no presente do indicativo |
| R9 | Evidência sem dívida escondida | **nenhuma afirmação do corpo apoiada em fonte não-✓** — validada ou enfraquecida |
| R10 | Gate | revisão independente em contexto fresco; DoD verde (build, link-check, suítes); entrada 1.0 no `HISTORICO.md` |

## Fora de escopo (decidido no ADR 0009)

Rodada 4 (medição própria) · rodada 5 (as 58 técnicas do *The Prompt Report*) · rodada 6
(Radar e placar de expiração) · rodada 7 (edição em inglês) · DOI e PDF consolidado ·
deploy do chat companion (ADR 0010) · etapas 15–16 do `rag-zero`.

## Ambiguidades resolvidas (clarify)

1. **"Terminar o livro" significa cobrir todo o ROADMAP?** Não. Significa a v1 declarada
   no ROADMAP desde a edição 0.1, que já excluía inglês, Radar e benchmark de frameworks.
   Resolvido no ADR 0009.
2. **O companion precisa estar no ar?** Não; a **afirmação** é que precisa ser
   verdadeira. Resolvido no ADR 0010.
3. **As 13 referências ⏳ precisam virar ✓?** Não. O critério é R9 — nenhuma afirmação do
   corpo depender delas. Validar é uma das duas saídas; enfraquecer a afirmação é a outra.
