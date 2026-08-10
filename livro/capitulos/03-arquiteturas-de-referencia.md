# 03 — Arquiteturas de Referência

> **Estado da arte capturado em 2026-08** · edição 1.0 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** Os quatro paradigmas e os padrões de fluxo estão fechados; o tratamento por implementação é a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Distinguir** os quatro paradigmas — Naive, Advanced, Modular e Agêntico — pelo que cada um resolve e pelo que cobra;
2. **Reconhecer** os quatro padrões de fluxo (linear, condicional, ramificado, em laço) dentro de qualquer arquitetura;
3. **Escolher** a topologia mínima que atende ao seu caso, em vez da mais sofisticada;
4. **Situar** o seu sistema atual no espectro — e saber qual é o próximo degrau, se houver.

## O problema

Duas patologias opostas, e a segunda é mais cara:

A primeira é **parar no ingênuo**: cortar, embeddar, buscar `top_k`, concatenar, responder. Funciona na demo, decepciona no corpus real, e o time conclui que "RAG não serve".

A segunda é **saltar para o sofisticado**: adotar grafo, multiagente e reflexão porque a demo ingênua decepcionou — sem ter medido qual estágio falhou. O resultado é um sistema com cinco peças móveis que ninguém entende, custo imprevisível, e a mesma qualidade de antes.

Entre os dois extremos existe uma progressão nomeada pela literatura, com degraus que se justificam por evidência. **Este capítulo é o mapa dessa progressão** — e a defesa contra a segunda patologia, que é a que mais destrói projetos.

## Fundamentos científicos

- **Os três paradigmas** — a survey de Gao et al. ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)) examina *"the progression of RAG paradigms, encompassing the **Naive RAG**, the **Advanced RAG**, and the **Modular RAG**"*. Não é cronologia apenas: é uma escada de sofisticação arquitetural, em que cada degrau existe para curar um defeito nomeado do anterior. É a taxonomia mais citada da área. ✓
- **Modular RAG** — [arXiv 2407.21059](https://arxiv.org/html/2407.21059v1) leva o terceiro degrau à sua formulação completa: um framework *"highly reconfigurable"* que *"**transcends the traditional linear architecture**"*, com módulos, operadores e padrões de fluxo recombináveis. É de onde vem a seção 3 deste capítulo — e a frase sobre a arquitetura linear é o que justifica tratar fluxo como decisão de projeto. ✓
- **O quarto degrau** — o survey de RAG agêntico ([arXiv 2501.09136](https://arxiv.org/abs/2501.09136)) formaliza a topologia em que um agente **decide** o fluxo em tempo de execução, com quatro padrões — *"reflection, planning, tool use, and multi-agent collaboration"* — contra a limitação dos *"**static workflows**"*. E [arXiv 2506.10408](https://arxiv.org/abs/2506.10408) dá o nome à fronteira: *predefined reasoning* (pipeline modular fixo) × *agentic reasoning* (o modelo orquestra sozinho). ✓

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **Onde a maioria realmente está** — a leitura de praticante de 2026 é que a maior parte dos sistemas em produção é **Advanced RAG** que se descreve como Modular. A diferença é verificável e não é retórica: em Modular RAG você **troca um módulo sem tocar nos vizinhos**. Se trocar o reranker exige mexer no montador de contexto, o sistema é avançado, não modular.
- **O movimento de 2026** — "context engineering na etapa de indexação" virou o foco dominante da otimização, o que na prática significa: os ganhos migraram do caminho de consulta para o de indexação (cap. 02).
- **O custo escondido do modular** — flexibilidade cobra em superfície de configuração. Um sistema com dez módulos plugáveis tem um espaço de combinações que ninguém avalia inteiro, e a maior parte das combinações nunca foi testada junta.

## O estado da arte

### 1. Os quatro paradigmas

| Paradigma | O fluxo | Cura do anterior | Cobra em |
|---|---|---|---|
| **Naive** | indexar → buscar `top_k` → concatenar → responder | — | falha fora do caso fácil |
| **Advanced** | + pré-recuperação (reescrita, metadado) e pós-recuperação (rerank, compressão) | recall e precisão baixos do ingênuo | mais estágios, mais latência |
| **Modular** | módulos recombináveis, com fluxo declarado | rigidez do pipeline fixo | superfície de configuração |
| **Agêntico** | o fluxo é decidido em runtime pelo modelo | incapacidade de adaptar à pergunta | previsibilidade de custo e latência |

A leitura que importa não é "o quarto é melhor". É que **cada degrau troca uma limitação por um custo**, e o degrau certo é o menor que resolve a sua falha medida (cap. 21).

O caso do **Advanced** merece destaque porque é onde mora a maioria e onde está o melhor retorno: reescrita de consulta na entrada, busca híbrida no meio, reranking na saída. Três acréscimos ao ingênuo que, juntos, resolvem a maior parte dos problemas reais — sem nenhuma peça móvel nova em runtime.

### 2. Naive não é sinônimo de errado

Vale defender o primeiro degrau, porque o desprezo por ele custa caro: **um RAG ingênuo bem instrumentado é a linha de base honesta do projeto.** Ele é rápido de montar, fácil de entender, e produz o número contra o qual todo degrau seguinte precisa se justificar.

O erro não é começar ingênuo — é **ficar** ingênuo sem medir, ou **sair** dele sem medir. A regra prática: nenhum degrau é subido sem o número do degrau anterior na mão.

### 3. Os quatro padrões de fluxo

Independente do paradigma, o fluxo de qualquer sistema é composto de quatro formas — e nomeá-las torna a arquitetura discutível:

| Padrão | Forma | Exemplo | Custo |
|---|---|---|---|
| **Linear** | A → B → C, sempre | o pipeline clássico | previsível |
| **Condicional** | if X então A, senão B | roteamento por tipo de pergunta | 1 classificação |
| **Ramificado** | A **e** B em paralelo, depois funde | busca híbrida; múltiplas consultas | N buscas, 1 fusão |
| **Em laço** | repete até um critério | reflexão; multi-hop | **imprevisível** — exige teto |

Duas leituras práticas:

- **Busca híbrida é um padrão ramificado**, não um "tipo de busca". Enxergar assim explica por que a fusão de ranking é uma decisão de arquitetura, e não um detalhe de configuração (cap. 06).
- **Só o laço é imprevisível.** Linear, condicional e ramificado têm custo calculável antes de rodar. O laço não — e é por isso que ele é o único que exige teto obrigatório (cap. 18). Um sistema que mistura os quatro tem o custo do pior caso do laço, não a média dos quatro.

### 4. Escolher a topologia mínima

A pergunta certa não é "qual arquitetura adotar", é "**qual é o menor degrau que resolve a falha que eu medi**". A ordem de decisão:

1. **Meça** (cap. 21). Sem a tabela de diagnóstico, qualquer escolha aqui é palpite caro.
2. **Se o recall está baixo** → o problema é anterior à arquitetura: corpus (04) ou representação (05). Nenhuma topologia conserta índice ruim.
3. **Se a precisão está baixa** → Advanced resolve: reranking e `top_k` menor.
4. **Se a pergunta não se parece com a resposta** → Advanced na entrada: reescrita (08).
5. **Se as perguntas são heterogêneas** → condicional: roteamento por tipo.
6. **Se algumas exigem múltiplos saltos** → laço, com teto (18).
7. **Se o time precisa trocar peças sem quebrar vizinhos** → modular, e o critério é o teste: trocar o reranker sem tocar no montador.

O item 2 é o que mais economiza tempo de time: **a maior parte das discussões de arquitetura em projetos de RAG deveria ter sido uma discussão sobre o corpus.**

### 5. A honestidade sobre o modular

"Modular" virou adjetivo de marketing. O critério verificável, de novo: **trocar um módulo sem tocar nos vizinhos.** Se o sistema não passa nesse teste, chamá-lo de modular só atrapalha o diagnóstico.

E há um custo que a literatura de entusiasmo omite: modularidade multiplica o espaço de configuração. Dez módulos com três opções cada são milhares de combinações, das quais você avaliou talvez cinco. A modularidade é boa para **evoluir**, e é uma armadilha se usada para **adiar a decisão** — "deixa plugável" costuma significar "não decidimos".

### Leitura executiva

Quatro paradigmas em escada — **Naive → Advanced → Modular → Agêntico** — e cada degrau **troca uma limitação por um custo**. O degrau certo é o menor que resolve a falha que você **mediu**, não o mais sofisticado. **O que roubar:** a maioria dos ganhos reais está no **Advanced** (reescrita na entrada + busca híbrida no meio + reranking na saída) — três acréscimos sem nenhuma peça móvel nova em runtime. E defenda o ingênuo: **um RAG naive bem instrumentado é a linha de base honesta** contra a qual todo degrau seguinte se justifica; o erro não é começar ingênuo, é subir ou ficar sem medir. **Os quatro padrões de fluxo** (linear, condicional, ramificado, em laço) tornam a arquitetura discutível — e a leitura que decide projeto é: **só o laço é imprevisível**, e por isso é o único que exige teto. **A regra que mais economiza tempo:** se o recall está baixo, o problema é anterior à arquitetura — é corpus ou representação, e nenhuma topologia conserta índice ruim. **Sobre "modular":** o critério é verificável — trocar um módulo sem tocar nos vizinhos. Se não passa, é Advanced com nome bonito.

## Mão na massa — rag-zero, etapa 2

Na etapa 2 você monta o `rag-zero` **ingênuo e inteiro**: corte fixo, embedding, `top_k`, concatenação, resposta. Sem reescrita, sem rerank, sem laço. E roda o eval sobre ele. O número que sai daí é a linha de base do livro — todos os degraus seguintes serão medidos contra ele, e alguns não vão se justificar. O exercício de completude: o registrador da linha de base vem esqueletado; você decide o que guardar de cada execução para que a comparação seja honesta seis capítulos depois.

## Verificação

1. Seu sistema tem reescrita de consulta, busca híbrida e reranking, e o time o chama de "modular". Que teste decide se o nome está certo?
2. O recall do seu RAG é 0,55. Por que adotar RAG agêntico provavelmente **não** vai resolver, e o que resolveria?
3. Classifique nos quatro padrões de fluxo: (a) busca densa + BM25 com fusão; (b) classificar a pergunta e escolher a fonte; (c) buscar, avaliar, buscar de novo. Qual exige teto e por quê?

---

## Apêndice A — Como cada framework materializa os paradigmas

> Tratamento por implementação, com URL.

| Paradigma | Como aparece na prática | O que reter |
|---|---|---|
| **Naive** | o *quickstart* de qualquer framework | é literalmente o tutorial de primeira página dos três. **Pegadinha:** a maioria dos sistemas que se dizem avançados parou aqui e acrescentou um reranker. |
| **Advanced** | pré e pós-recuperação plugados no mesmo pipeline linear | continua linear. Acrescentar reescrita e reranking **não** torna o sistema modular. |
| **Modular** | grafos de fluxo com nós e arestas (LangGraph, *workflows* do LlamaIndex, *pipelines* do Haystack) | é aqui que roteamento e ramificação viram primeira classe. **O teste do capítulo:** trocar um módulo sem tocar nos vizinhos. Se o roteador conhece o formato interno do retriever, não é modular — é um `if`. |
| **Agêntico** | recuperação exposta como **ferramenta** ao modelo | ver o [cap. 18](18-rag-agentico.md). **Pegadinha:** o framework dá o laço; o **teto** do laço é sempre seu. |

**A leitura de Gao que fecha o apêndice:** o Advanced RAG é descrito como quem *"employs **pre-retrieval and post-retrieval** strategies"* — as duas continuam presas a uma sequência. É *Modular RAG* que *"**transcends the traditional linear architecture**"*. A fronteira entre o segundo e o terceiro degrau não é quantidade de técnica; é **topologia**.
