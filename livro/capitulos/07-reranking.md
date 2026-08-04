# 07 — Reranking

> **Estado da arte capturado em 2026-08** · edição 0.2 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
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
- **A linhagem** — reordenação em estágios é prática consolidada em *Information Retrieval* muito antes dos LLMs (SIGIR, TREC). O arranjo "recuperar barato, reordenar caro" sobreviveu a várias gerações de modelo, o que é evidência de que ele resolve uma propriedade do problema, não da tecnologia. `[a validar]`
- **O lugar no paradigma** — na taxonomia de Gao ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)), reranking é uma das técnicas de **pós-recuperação** que definem o Advanced RAG. É um dos três acréscimos que separam o ingênuo do avançado (cap. 03). `[a validar]`

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

## Apêndice A — Como cada reranker funciona

**Rodada 1 (edição 0.2)**: a economia do estágio e o uso da nota estão descritos. O tratamento por implementação — arquiteturas de reranker, latência por documento, e as condições experimentais dos ganhos publicados — é a **rodada 2** do ROADMAP.

Enfileirado: cross-encoders e alternativas de última geração · reordenação em estágios na tradição de IR · calibração de nota para limiar · o lugar do reranking no Advanced RAG (2312.10997).
