# 07 — Reranking

> **Estado da arte capturado em 2026-08** · edição 0.4 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** Componente que aprofunda: **reranker** (cap. 02).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Explicar** por que reordenar exige um modelo diferente do que recupera;
2. **Dimensionar** o estágio: quantos candidatos entram, quantos saem, quanto custa;
3. **Usar** a nota do reranker como sinal — limiar, abstenção e monitoramento;
4. **Decidir** quando o reranking não se justifica.

## O problema

O capítulo anterior entrega candidatos: 50, 100, às vezes 200 trechos plausíveis, ordenados por uma similaridade barata. O contexto comporta cinco.

A distância entre "está entre os 100" e "está entre os 5" é onde mora a diferença entre um RAG que traz ruído pago e um que traz resposta. E ela não se fecha melhorando a busca: a busca é otimizada para ser **barata em escala**, e essa economia tem um teto de precisão.

O reranking existe porque as duas tarefas são diferentes o bastante para exigirem modelos diferentes — e porque a segunda pode ser cara, já que opera sobre poucos.

## Fundamentos científicos

- **A diferença arquitetural** — a busca densa compara vetores calculados **separadamente** para pergunta e documento (*bi-encoder*): rápida, indexável, e cega para a interação entre os dois textos. O reranker típico é um *cross-encoder*: lê pergunta e documento **juntos** e pontua a relevância da relação. Ganha em precisão exatamente onde o outro é estruturalmente limitado. `[a validar]`
- **A linhagem, e a conta** — reordenação em estágios é prática consolidada em *Information Retrieval* muito antes dos LLMs. E o BEIR ([arXiv 2104.08663](https://arxiv.org/abs/2104.08663)) mede as duas metades da tese deste capítulo numa frase só: *"**re-ranking** and late-interaction-based models on average achieve the **best zero-shot performances**, however, **at high computational costs**"*. Maior retorno **e** maior custo — é por isso que ele é o terceiro estágio, e não o primeiro. ✓
- **O lugar no paradigma** — a survey de Gao ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)) descreve o Advanced RAG como quem *"employs **pre-retrieval and post-retrieval** strategies"*, e situa este capítulo do lado de lá: *"The main methods in post-retrieval process include **rerank chunks** and context compressing"*. Vale reter o **porquê** que ela dá para reordenar: *"to relocate the most relevant content to the **edges of the prompt**"* — ou seja, o reranking não serve só para cortar, serve para **posicionar**, e isso liga direto ao cap. 20. ✓

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **O estágio de maior retorno marginal** — a experiência publicada por praticantes converge: quando busca e fusão já estão razoáveis, o reranker é o que mais adiciona. Os números específicos vêm de corpora dos próprios proponentes e este livro os trata como hipótese a reproduzir (cap. 21).
- **A oferta** — rerankers como serviço e modelos abertos coexistem; a decisão prática costuma ser latência e custo por documento, não qualidade de topo.
- **O uso que quase ninguém faz** — aproveitar a **nota** do reranker, e não apenas a ordem. Ela é um sinal calibrado de relevância, e é o que permite limiar e abstenção.

## O estado da arte

### 1. A economia do arranjo

```
busca (barata)  →  N candidatos (50-200)  →  reranker (caro)  →  K finais (3-10)
   ~O(log n) no índice                         ~O(N) chamadas de modelo
```

O modelo caro só vê o que o barato já filtrou. Toda a viabilidade do estágio depende disso — e é o que decide os dois parâmetros:

- **N muito pequeno**: o reranker não tem o que consertar; se o certo não está entre os candidatos, reordenar não o traz.
- **N muito grande**: custo e latência lineares, com retorno decrescente.
- **K** é decisão de orçamento (cap. 20), não de qualidade: quantos trechos o contexto comporta sem afogar a instrução.

A pergunta de projeto é **quanto recall você compra em N para converter em precisão em K**. E ela tem resposta medida, não escolhida: aumentar N só ajuda enquanto o *context recall* em N estiver subindo (cap. 21).

### 2. A nota é mais útil que a ordem

Um reranker devolve pontuações, e a maioria dos sistemas descarta todas menos a ordenação. As três coisas que a nota habilita:

- **Limiar e abstenção.** Nenhum candidato acima do limiar significa "não encontrei" (cap. 15). Sem nota, o sistema sempre devolve K resultados — mesmo quando o corpus não tem a resposta.
- **K variável.** Em vez de sempre 5, mande quantos passarem do limiar. Perguntas fáceis gastam menos contexto; difíceis gastam mais. É orçamento adaptativo de graça.
- **Monitoramento.** A **distribuição** das notas ao longo do tempo denuncia mudança no corpus ou no padrão de perguntas antes de qualquer métrica de qualidade acusar (cap. 21).

O segundo item é o mais subestimado: `top_k` fixo é uma decisão que finge que todas as perguntas têm a mesma dificuldade.

### 3. Quando não vale

Registrado porque este livro se recusa a vender estágio:

- **Corpus pequeno**, em que a busca já devolve quase tudo relevante nos primeiros lugares.
- **Latência apertada** — o reranker é síncrono e está no caminho crítico.
- **Recall baixo** — se o certo não chega aos candidatos, reordenar não inventa. O problema é anterior (caps. 04, 05, 06). Este é o erro mais comum: adotar reranking para curar uma falha de recall.
- **Volume altíssimo com margem apertada** — o custo é por documento reordenado, em toda requisição.

### Leitura executiva

Busca e reordenação são tarefas diferentes o bastante para exigirem **modelos diferentes**: a busca densa compara vetores calculados separadamente (*bi-encoder*) e é cega à interação entre pergunta e documento; o reranker lê os dois **juntos** (*cross-encoder*) e ganha precisão exatamente onde o outro é estruturalmente limitado. **O que roubar:** o arranjo "recuperar barato, reordenar caro" — o modelo caro só vê o que o barato filtrou — e a pergunta de projeto que dele decorre: **quanto recall você compra em N para converter em precisão em K**, respondida por medição, não por escolha. **O que quase ninguém aproveita:** a **nota**, não só a ordem. Ela habilita limiar e abstenção ("não encontrei"), **K variável** (perguntas fáceis gastam menos contexto — orçamento adaptativo de graça) e monitoramento pela distribuição, que denuncia mudança no corpus antes de qualquer métrica de qualidade. **Quando não vale:** corpus pequeno, latência apertada, volume com margem fina — e sobretudo **recall baixo**, porque reordenar não inventa o que não chegou. Adotar reranking para curar falha de recall é o erro mais comum deste capítulo.

## Mão na massa — rag-zero, etapa 6

Na etapa 6 você acrescenta o reranker ao `rag-zero` e mede três coisas: o ganho de precisão sobre a etapa 4, o custo por pergunta, e a curva de N (20, 50, 100) até o retorno virar plano. Depois troca `top_k` fixo por K variável com limiar, e compara o gasto médio de contexto. O exercício de completude: o limiar vem esqueletado — você o calibra e descobre que ele é a fronteira entre "não sei" e alucinação.

## Verificação

1. Seu *context recall* em N=100 é 0,62. Vale adotar reranking? O que fazer antes?
2. Descreva duas coisas que a nota do reranker permite e a ordem não.
3. Por que aumentar N indefinidamente para de ajudar, e como identificar o ponto?

---

## Apêndice A — Como cada abordagem reordena

> Tratamento por implementação, com URL.

| O quê | Implementação de referência | O que reter |
|---|---|---|
| **Cross-encoder aberto** | `CrossEncoder` do [sentence-transformers](https://github.com/UKPLab/sentence-transformers) | a rota de custo zero e sem GPU para N pequeno; é a que o `rag-zero` usa. **Pegadinha:** o custo é **linear em N**, e a latência de um lote de 100 num CPU comum surpreende quem só testou com 10. |
| **Reranking como serviço** | APIs de reranking dos provedores | tiram o modelo da sua infraestrutura e devolvem nota normalizada. **Pegadinha:** a nota é comparável **dentro** de uma consulta, não entre consultas nem entre versões do modelo — um limiar fixo calibrado hoje expira na próxima versão. |
| **Reranking por LLM** | *listwise*, pedindo ao modelo que ordene os candidatos | dispensa modelo dedicado. **Pegadinha:** não devolve nota utilizável como limiar (§ sobre usar a nota), e o resultado depende da ordem de entrada — o que é viés de posição, o mesmo do cap. 20. |
| **Onde ele encaixa** | `ContextualCompressionRetriever` (LangChain), *node postprocessors* (LlamaIndex), `Ranker` (Haystack) | os três tratam reranking como **pós-processador do retriever**, que é o desenho correto: o retriever não sabe que existe reranker. |

**A ligação que a survey de Gao acrescenta:** reranking é pós-recuperação e serve também para *"relocate the most relevant content to the **edges of the prompt**"*. Se a sua implementação reordena e depois concatena na ordem, ela está usando metade da técnica.
