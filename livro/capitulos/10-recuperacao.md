# 10 — Recuperação: o Núcleo do RAG

> **Estado da arte capturado em 2026-08** · edição 0.1 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** O pipeline de três estágios e os trade-offs estão fechados; as medições comparadas e o Apêndice A são a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Descrever** o pipeline de recuperação em seus estágios e o que cada um resolve;
2. **Escolher** uma estratégia de chunking a partir da forma do documento e do tipo de pergunta;
3. **Explicar** por que busca densa e busca esparsa falham de formas diferentes — e por que a combinação supera as duas;
4. **Justificar** o reranking como estágio separado, com seu custo e seu retorno.

## O problema

A pergunta central da recuperação é enganosamente simples: *dado um corpus e uma pergunta, quais trechos colocar no contexto?* Cada palavra dessa frase esconde uma decisão de engenharia.

**"Trechos"** — o documento precisou ser cortado, e o corte já destruiu informação: o parágrafo que começa com "isso implica que..." perdeu o antecedente ao virar um chunk isolado.

**"Quais"** — a noção de relevância precisa virar operação computável, e as duas famílias disponíveis (léxica e semântica) erram em direções opostas.

**"Colocar"** — quantos, em que ordem, ocupando quanto do orçamento do cap. 08.

A maioria dos sistemas de RAG que "não funciona" falha aqui, no primeiro estágio, e o time passa meses ajustando o prompt de geração.

## Fundamentos científicos

- **Chunking tem literatura própria** — *Reconstructing Context: Evaluating Advanced Chunking Strategies for RAG* ([arXiv 2504.19754](https://arxiv.org/abs/2504.19754)) avalia estratégias avançadas em vez de assumi-las, e é o ponto de partida para não escolher tamanho de chunk por superstição. `[a validar]`
- **Seleção adaptativa de método** — há trabalho recente sobre escolher a estratégia de chunking por documento em vez de fixar uma para o corpus inteiro ([arXiv 2603.25333](https://arxiv.org/abs/2603.25333)), o que reconhece formalmente que "um tamanho serve para tudo" é a hipótese errada. `[a validar]`
- **Recuperação como componente da disciplina** — o survey [arXiv 2507.13334](https://arxiv.org/abs/2507.13334) posiciona "context retrieval and generation" como o primeiro dos três componentes, com o RAG como implementação que o combina com os demais. `[a validar]`
- **Benchmarks de recuperação pura** — **BEIR** (recuperação zero-shot em domínios variados) e **MTEB** (avaliação ampla de modelos de embedding) são as referências para medir **este** estágio isolado do resto do pipeline. A separação importa: um sistema pode ter recuperação ótima e resposta ruim, e o diagnóstico depende de medir os dois separadamente (cap. 16). `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **O pipeline de três estágios** — a arquitetura convergente é: **recuperação ampla e barata** (candidatos) → **fusão** de sinais léxico e semântico → **reranking caro e preciso** sobre poucos. A prática de 2026 trata os três como estágios distintos com métricas próprias, e não como uma caixa só.
- **Busca híbrida** — a combinação de embeddings densos com BM25, por fusão de ranking, é o padrão de fato. A razão é diagnóstica: busca densa erra em termos raros, códigos, nomes próprios e números; busca esparsa erra em paráfrase e sinônimo. Os erros são **complementares**, não sobrepostos.
- **Reranking** — um modelo de reordenação (tipicamente *cross-encoder*) sobre os N primeiros candidatos. É caro por documento e por isso só se aplica a poucos; e é, segundo a experiência publicada dos praticantes, **o estágio de maior retorno marginal** quando os dois anteriores já estão razoáveis.

## O estado da arte

### 1. Chunking: o corte que decide tudo

O chunk é a unidade atômica de tudo que vem depois. Errar aqui não é recuperável adiante.

| Estratégia | Como corta | Boa para | Falha em |
|---|---|---|---|
| **Nenhuma** | o documento inteiro é a unidade | FAQ, tickets, descrições curtas | documento longo |
| **Tamanho fixo** | N tokens, com sobreposição | corpus homogêneo; linha de base honesta | corta no meio de raciocínio |
| **Recursiva** | quebra por separadores em cascata (parágrafo → frase → token) | o padrão razoável para a maioria dos corpora | ainda é corte cego, só que educado |
| **Estrutural** | por marcação do documento (título, seção, célula) | documentos com hierarquia real | documento sem estrutura confiável |
| **Semântica** | por quebra de tópico detectada | prosa longa sem seções | custo de pré-processamento; fronteiras instáveis |
| **Sentence-window** | indexa a frase, entrega a janela em volta dela | precisão de busca com contexto na entrega | janela fixa nem sempre é a certa |
| **Proposition** | decompõe em afirmações autocontidas e indexa cada uma | pergunta factual específica | caro (uma passada de LLM) e perde o encadeamento |
| **Hierárquica** | indexa pequeno, entrega o pai | quando o vizinho importa | complexidade de índice |

As três últimas compartilham a mesma ideia, e vale nomeá-la porque é o padrão de projeto mais útil do capítulo: **desacoplar a unidade de busca da unidade de entrega.** O que se indexa (pequeno, preciso, bom para o ranking) não precisa ser o que se envia ao modelo (maior, com contexto suficiente para responder). Quase todo sistema que fixa as duas coisas no mesmo chunk está aceitando um compromisso que não precisava aceitar.

Três regras que a prática consolidou, e que valem mais que a escolha da estratégia:

- **Sobreposição não é opcional** quando se usa corte cego. É o remendo mais barato para a fronteira mal colocada.
- **Metadado junto do chunk** (documento de origem, seção, data, permissão) é o que permite filtrar antes de buscar — e filtro antes da busca costuma render mais que qualquer ajuste de similaridade.
- **O tamanho ótimo depende da pergunta, não do documento.** Perguntas factuais favorecem chunks pequenos; perguntas que exigem contexto favorecem grandes. Corpus com os dois tipos de pergunta pedem índice com mais de uma granularidade — e é aí que a estratégia hierárquica paga.

### 2. Denso, esparso, e por que os dois

A busca densa representa texto como vetor e mede proximidade semântica: acha "veículo" quando você perguntou "carro". A busca esparsa (BM25 e parentes) pontua por sobreposição de termos: acha exatamente `ERR_4021` porque o token está lá.

Os modos de falha são espelhados:

- **Densa falha** em identificador, código de erro, nome próprio raro, número, jargão fora do domínio de treino do modelo de embedding.
- **Esparsa falha** em sinônimo, paráfrase, pergunta escrita com vocabulário diferente do documento.

Como os erros são complementares, a fusão dos dois rankings recupera casos que nenhum dos dois pega sozinho. **Este é o upgrade de maior relação benefício/esforço do capítulo** — e é o primeiro a tentar quando um RAG "não encontra o óbvio", porque quase sempre o óbvio é um termo literal que o índice denso não viu.

### 3. Reranking: por que um terceiro estágio

Os dois primeiros estágios otimizam **recall** barato: trazer os candidatos certos entre os primeiros 50 ou 100. Reranking otimiza **precisão** cara: reordenar esses poucos com um modelo que lê a pergunta e o documento **juntos** (em vez de comparar dois vetores calculados separadamente), e ficar com os 5 melhores.

A economia do arranjo é o ponto: o modelo caro só vê o que o barato já filtrou. É a mesma lógica de qualquer sistema de recuperação em escala, e é por isso que o arranjo sobreviveu a várias gerações de modelo.

O ganho reportado pelos praticantes é cumulativo com os estágios anteriores — a curva importa mais que os números: cada estágio adiciona, e o reranking é o que mais adiciona **por último**. Os números específicos publicados (ver [panorama](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md)) vêm de corpus dos próprios proponentes, e este livro os trata como hipótese a reproduzir.

### 4. O teto vem de antes: o corpus

Todos os estágios anteriores são otimizações **sobre o que está no índice**. Nenhum deles inventa informação que o corpus não tem, e nenhum distingue um documento correto de um obsoleto — os dois embeddam igual.

Isso é assunto do **[cap. 09](09-corpus.md)**, que vem antes deste exatamente por isso: frescor, procedência, deduplicação e permissão definem o teto de tudo que este capítulo otimiza. Se o seu recall está baixo, verifique lá antes de mexer aqui — é mais barato e é mais frequente.

### 5. O que quase sempre falta

Três coisas ausentes na maioria dos pipelines, em ordem de dano:

- **Filtro por permissão antes da busca.** Recuperar e depois filtrar vaza — na latência e, dependendo da implementação, no conteúdo. É requisito de segurança, não de performance.
- **Um caminho para "não encontrei".** Sistema que sempre devolve `top_k` resultados sempre devolve algo — mesmo quando o corpus não tem a resposta. Sem limiar de similaridade e sem caminho de abstenção, a alucinação fundamentada em ruído é inevitável. O sinal operacional correspondente — a **taxa de resultado zero** — é o instrumento que mostra se esse caminho existe e com que frequência é usado (cap. 16).
- **Medição isolada deste estágio.** Sem medir recuperação separada da geração, todo diagnóstico vira palpite (cap. 16).

### Leitura executiva

Recuperação é um pipeline de **três estágios com métricas próprias**: candidatos baratos → fusão de sinais → reranking caro sobre poucos. **O que roubar, em ordem de retorno:** (1) **busca híbrida** — densa e esparsa erram em direções complementares (densa perde código e nome próprio; esparsa perde paráfrase), e a fusão é o upgrade de melhor relação benefício/esforço; (2) **reranking** como terceiro estágio, que é o que mais adiciona por último; (3) **metadado junto do chunk**, porque filtrar antes de buscar rende mais que ajustar similaridade. **O padrão de projeto do capítulo:** *desacople a unidade de busca da unidade de entrega* — o que se indexa (pequeno, preciso) não precisa ser o que se envia (maior, com contexto). É o que sentence-window, proposition e chunking hierárquico têm em comum. **O corte decide tudo:** o tamanho ótimo depende da **pergunta**, não do documento. **O teto vem de antes:** frescor, procedência e duplicação limitam a recuperação antes de qualquer escolha técnica deste capítulo — documento revogado embedda igual ao vigente (cap. 09). **O que quase sempre falta:** filtro por permissão **antes** da busca, um caminho explícito para "não encontrei" (com a taxa de resultado zero monitorada), e medir este estágio isolado da geração.

## Mão na massa — contexto-zero, etapa 9

Na etapa 9 você constrói a recuperação do `contexto-zero` **na mão, antes de qualquer biblioteca**: um BM25 em cerca de 40 linhas sobre o texto deste livro, com chunking estrutural por seção e metadados. Sem vector store, sem framework. O objetivo pedagógico é que você veja o ranking acontecer. Na etapa 10 entram embeddings, fusão e reranking — e a comparação entre as duas etapas é o conteúdo, não o resultado final.

## Verificação

1. Seu RAG não encontra documentos quando o usuário busca por um código de produto (`XR-4400-B`), mas encontra bem por descrição. Qual estágio está faltando e por quê?
2. Um chunk de 200 tokens dá boa precisão e péssima capacidade de responder "resuma a seção". Descreva uma solução de índice que atenda aos dois casos sem duplicar o corpus inteiro.
3. Por que filtrar por permissão **depois** da recuperação é um problema de segurança, e não só de eficiência?

---

## Apêndice A — Como cada abordagem trata a recuperação

> Tratamento por técnica e implementação, com URL — complementação online, expandida a cada rodada.

**Rodada 1 (edição 0.1)**: o pipeline de três estágios e os modos de falha complementares estão descritos. O tratamento por implementação — famílias de modelo de embedding, algoritmos de fusão de ranking, arquiteturas de reranker, e o que BEIR/MTEB medem exatamente — é o trabalho da **rodada 2** do ROADMAP.

Enfileirado: BM25 e variantes · modelos de embedding e o que MTEB mede · fusão recíproca de ranking e alternativas · rerankers *cross-encoder* e de última geração · estratégias de chunking comparadas com medição · índices com múltipla granularidade.
