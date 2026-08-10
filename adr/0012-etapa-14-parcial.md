# 0012 — A etapa 14 entra parcial na 1.0

- **Status:** Aceito
- **Data:** 2026-08-09
- **Contexto (feature/spec):** `001-edicao-1-0`

## Contexto

O [ADR 0009](0009-escopo-da-edicao-1-0.md) listou, no piso do `rag-zero` para a 1.0, a
**etapa 14 completa** — as quatro métricas do cap. 21. Ela foi entregue **parcial**: as
métricas de recuperação existem e são usadas pelas etapas 5 e 8; *faithfulness* e *answer
relevance* não.

O rebaixamento aconteceu **sem registro**, e foi o revisor independente que o apontou:
mudança de escopo sem ADR viola a regra 5 do próprio plano deste ciclo.

## Decisão

**A etapa 14 entra na 1.0 com as métricas de recuperação apenas**, e o cap. 21 declara
isso na seção "Mão na massa" em vez de descrever a etapa completa no presente.

O motivo é substantivo, não de prazo: *faithfulness* e *answer relevance* exigem
**LLM-as-judge**. Um juiz não calibrado produz número com aparência de rigor — e o
próprio cap. 17 exige medir a concordância com julgamento humano **antes** de confiar no
juiz. Entregar a métrica sem a calibração seria publicar exatamente o anti-padrão que o
livro ensina a evitar.

## Alternativas avaliadas

- **A — Entregar com juiz não calibrado.** Prós: fecha o item do ADR 0009. Contras:
  produz número que o próprio livro classifica como "invenção com aparência de rigor".
- **B — Entregar com calibração humana.** Prós: correto. Contras: exige amostra revisada
  por gente — não é trabalho que uma execução autônoma possa fazer por si.
- **C — Entregar parcial e declarar (a escolhida).**

## Justificativa

O Princípio IV autoriza **declarar maturidade**; o que ele proíbe é fingir. E há uma
assimetria que decide: uma métrica de recuperação errada é visível (o recall não bate com
o que você vê no top-k); uma métrica de fidelidade com juiz não calibrado é **invisível**
— parece funcionar e mede outra coisa.

## Consequências

- **Positivas:** o livro não publica um número que ele mesmo ensina a desconfiar.
- **Negativas / custos aceitos:** o cap. 21 fica sem exercício executável das duas
  métricas de geração; a "Mão na massa" dele aponta para a etapa 5, que é o que existe.
- **Reversibilidade:** alta. A porta do juiz já existe (`LLMPort`); falta a calibração,
  que é trabalho de rodada própria com participação humana.
