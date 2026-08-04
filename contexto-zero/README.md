# contexto-zero — a trilha prática

> O livro executável: um sistema de prompt + contexto construído do zero, **uma etapa por capítulo**.
>
> Edição 0.1 · **status: planejado.** As etapas estão especificadas abaixo e descritas na seção "Mão na massa" de cada capítulo. A implementação é a [rodada 3](../ROADMAP.md#rodada-3--contexto-zero-a-trilha-prática) do ROADMAP.

## O que é

A espinha 4C/ID do livro (Princípio III): cada etapa é uma *learning task* inteira — não um fragmento — e o capítulo correspondente é a *supportive information* que a sustenta.

**Stack:** Python + FastAPI + um chat mínimo em HTML/JS. **Custo zero e sem GPU** (Princípio VI).

## As quatro regras da construção

Da seção "Restrições" da [constituição](../.specify/memory/constitution.md):

1. **Do zero antes da biblioteca.** BM25 em ~40 linhas antes de qualquer vector store; um otimizador de prompt em ~60 linhas antes do DSPy. A biblioteca entra depois, nomeada como **escolha** — não como pré-requisito. O objetivo é que você veja o mecanismo funcionar antes de delegá-lo.
2. **Arquitetura hexagonal por refatoração.** Cada porta nasce da dor do capítulo: `LLMPort` na etapa 0, `RetrieverPort` na 8, `MemoryPort` na 11, `EvalPort` na 14. Nunca estrutura antecipada.
3. **Completion problem, não folha em branco** (Carga Cognitiva). Cada etapa entrega o esqueleto e deixa para você a parte que **carrega a decisão** — a política de corte, o critério de saliência, o peso da fusão. É onde mora o aprendizado.
4. **Anti-apodrecimento.** Modelo atrás de porta; etapas autocontidas e executáveis; erro didático deliberado é comentado como tal.

## As 16 etapas

| Etapa | Cap. | Constrói | Prova (o teste que fecha) |
|:---:|:---:|---|---|
| 0 | 01 | chat + `LLMPort` + **contador de tokens por bloco** | o contador imprime a composição do contexto |
| 1 | 02 | prompt em blocos nomeados | material com instrução hostil embutida não muda o comportamento |
| 2 | 03 | duas famílias de raciocínio comparadas | tabela custo × acerto sobre 20 perguntas |
| 3 | 04 | schema + validação + reparo com teto | schema impossível falha explicitamente, sem laço |
| 4 | 05 | cinco camadas + cascata de regras | **estabilidade de prefixo**: mesmos bytes entre dois turnos |
| 5 | 06 | otimizador mínimo (~60 linhas) | o overfitting aparece: treino sobe, validação não |
| 6 | 07 | conjunto de eval + **calibração do juiz** | concordância juiz × humano reportada antes de usar o número |
| 7 | 08 | orçamento com política de corte | resultado gigante estoura e o corte segue a política escrita |
| 8 | 09 | **BM25 na mão** (~40 linhas) + chunking estrutural | ranking sobre o texto do livro, sem biblioteca |
| 9 | 09–10 | embeddings + fusão + reranking + contextual retrieval | medição por estágio: o ganho de cada um, isolado |
| 10 | 11 | recuperação como ferramenta + reflexão + teto | custo médio por pergunta, antes e depois da autonomia |
| 11 | 12 | memória com procedência, data e exclusão | fato de fonte externa **não** vira fato do usuário; exclusão apaga |
| 12 | 13 | compactação + estado estruturado | restrição do turno 2 sobrevive ao turno 40, após 2 compactações |
| 13 | 14 | ferramentas com teto no adaptador | ferramenta de 50k tokens não quebra o orçamento da etapa 7 |
| 14 | 15 | as quatro métricas + tabela de diagnóstico | eval da etapa 8 × etapa 9: o ganho esperado aparece? |
| 15 | 16 | **atacar o próprio sistema** | quanto cada camada de defesa bloqueia — e o que continua passando |
| 16 | 17 | painel custo + cache + latência + qualidade | a taxa de acerto de cache antes e depois de reordenar as camadas |

## A tese pedagógica das etapas

Três delas carregam o argumento do livro inteiro, e valem mesmo isoladas:

- **Etapa 0 — o contador.** O instrumento que você vai olhar em todas as outras. A maior parte dos sistemas em produção não tem nada equivalente, e é por isso que degradam de forma inexplicável (cap. 08).
- **Etapa 14 — o eval desconfortável.** Rodar a avaliação sobre a etapa 8 (só BM25) e sobre a etapa 9 (pipeline completo) e verificar se o ganho **que você esperava** aparece. Às vezes não aparece. Esse é o conteúdo.
- **Etapa 15 — atacar o próprio sistema.** A única forma de aprender o cap. 16 é ver a defesa textual falhar e a defesa de privilégio segurar.

## Relação com o chat companion

O [`chat-companion/`](../chat-companion/) **é o contexto-zero rodando em produção**: mesmo `LLMPort`, mesmo índice BM25 (a etapa 8), mesmo gating de capacidades por capítulo. Isso é deliberado — o exemplo real que o livro disseca é o próprio livro respondendo ao leitor.

Conforme as etapas avançarem, o companion avança junto: a etapa 9 (embeddings + fusão + reranking) substitui o índice atual, a etapa 11 liga a memória, a etapa 16 acende o painel.
