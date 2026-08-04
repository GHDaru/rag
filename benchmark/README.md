# Avaliação de técnicas — metodologia

> A seção empírica do livro. **O objeto avaliado aqui é a técnica, não o produto.**
>
> Edição 0.1 · captura em 2026-08 · **status: metodologia esboçada, nenhuma avaliação executada.** As avaliações são a [rodada 4](../ROADMAP.md#rodada-4--avaliação-de-técnicas-o-benchmark-deste-livro) do ROADMAP.

## Por que existe

O livro afirma coisas como "busca híbrida é o upgrade de melhor relação benefício/esforço" (cap. 10) e "*contextual retrieval* e *late chunking* resolvem o mesmo problema com contas muito diferentes" (cap. 11). Hoje essas afirmações se apoiam em medições **de terceiros**, feitas em corpus de terceiros — e o Princípio I obriga a dizer isso a cada vez.

Esta seção existe para o livro parar de dever: medir aqui, com receita publicada, o que hoje ele só cita.

Há também um argumento de coerência: um livro que exige condição experimental de todo número que cita não pode publicar números próprios sem a mesma exigência. **A metodologia é o preço da cobrança.**

## O que se avalia — e o que não

**Avalia-se:** técnicas comparáveis sobre o mesmo corpus, com a mesma pergunta e o mesmo modelo. Exemplos: busca densa × esparsa × híbrida; com e sem reranking; *contextual retrieval* × *late chunking*; estratégias de chunking; famílias de raciocínio (cap. 03); otimizadores de prompt (cap. 06).

**Não se avalia:**

- **Produtos e fornecedores.** Nenhuma nota para "melhor vector store" ou "melhor framework". Isso é comparação de infraestrutura e envelhece em semanas — além de colidir com o Princípio VI (neutralidade).
- **Modelos.** Já existem benchmarks públicos melhores do que qualquer coisa que este projeto faria.
- **Qualquer coisa sem receita reproduzível.** Se o leitor não consegue rodar de novo, não é resultado — é anedota com número.

## As dimensões

Cada técnica avaliada recebe uma ficha com cinco dimensões:

| Dimensão | Pergunta | Como se mede |
|---|---|---|
| **Eficácia** | resolve o problema que promete? | métrica do estágio (cap. 16): recall, precision, faithfulness |
| **Custo de indexação** | o que se paga uma vez? | chamadas de LLM, tempo, armazenamento — por 1k chunks |
| **Custo de consulta** | o que se paga sempre? | chamadas extras, tokens, latência p50/p95 — por pergunta |
| **Complexidade** | o que se adiciona de peça móvel? | componentes novos e novos modos de falha |
| **Sensibilidade** | o ganho sobrevive à mudança de corpus/modelo? | repetir em ≥2 corpora |

A dimensão **sensibilidade** é a que mais importa e a que a literatura mais omite. Um ganho que só aparece em um corpus não é um resultado — é uma coincidência documentada.

## A escala

`0` não paga · `1` paga em caso específico (declarado) · `2` paga na maioria dos casos · `3` paga quase sempre, e o custo é baixo

A nota **nunca** é comparável entre dimensões diferentes, e só é comparável entre técnicas que atacam o **mesmo problema** (as quatro falhas do cap. 11). Comparar *contextual retrieval* com reescrita de consulta é erro de categoria: elas curam falhas diferentes.

## Regras de evidência (Princípio I aplicado a nós mesmos)

Toda avaliação publica, junto do número:

1. **O corpus** — origem, tamanho, número de documentos e de chunks, e se é público.
2. **As perguntas** — quantas, de onde vieram (sintéticas × reais), e quem verificou as respostas.
3. **O modelo** — qual, com que parâmetros, e em que data (modelos mudam sob o mesmo nome).
4. **O orçamento** — `top_k`, tamanho de chunk, limites, tetos.
5. **A receita** — o comando que reproduz, no repositório.
6. **O intervalo** — resultado de execução única não é resultado. Mínimo de 3 execuções, com dispersão reportada.

**Sem os seis itens, a avaliação não é publicada.** É a mesma régua que o livro aplica às fontes que cita.

## Os corpora planejados

1. **O próprio livro** — pequeno, em português, conhecido pelo autor, bom para diagnóstico e para o companion. Enviesado por ser texto didático bem estruturado.
2. **Um corpus de domínio** — documentação técnica real, com perguntas verificadas por gente. É o que dá validade externa, e é o item caro.

Rodar em dois é o mínimo para a dimensão **sensibilidade** significar alguma coisa.

## O que já se sabe que vai dar errado

Registrado antes de começar, por honestidade:

- **O corpus do livro é fácil demais.** Texto bem estruturado, com seções nomeadas, favorece chunking estrutural e infla o recall. Os números serão otimistas.
- **Perguntas sintéticas superestimam o recall** (cap. 16) — a pergunta gerada de um trecho é respondível por aquele trecho.
- **Um autor avaliando as técnicas que escolheu descrever** tem viés de confirmação. A mitigação possível é publicar a receita e convidar contestação; não há mitigação completa.

Declarar isso antes de medir é mais barato do que descobrir depois — e é o que o livro cobra de todo mundo que cita.

---

## Estrutura desta pasta (a partir da rodada 4)

```
benchmark/
├── README.md          ← esta metodologia
├── corpora/           ← descrição e receita de preparo de cada corpus
├── avaliacoes/        ← uma ficha por técnica avaliada
└── comparativo.md     ← a tabela consolidada, por problema
```
