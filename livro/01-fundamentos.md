# 01 — Fundamentos

> **Estado da arte capturado em 2026-08** · edição 1.0 · [histórico e registro de expiração](HISTORICO.md)
>
> **Maturidade: fundação.** O vocabulário e a taxonomia por sintoma estão fechados. A rodada 2 validou a maior parte das referências; o que segue `[a validar]` são as afirmações sobre a herança de *Information Retrieval* (SIGIR, TREC), que precisam de fonte com URL.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Definir** os termos que o livro inteiro usa, e desfazer as três confusões mais caras;
2. **Situar** o RAG na linhagem de *Information Retrieval* — e dizer o que ele herdou e o que inventou;
3. **Classificar** um problema real na taxonomia por sintoma, para entrar no livro pelo lugar certo;
4. **Aplicar** a cláusula de expiração a qualquer texto técnico da área, inclusive a este.

## O problema

Campo novo, vocabulário instável. "Recuperação" às vezes significa o estágio de busca, às vezes o pipeline inteiro; "RAG" às vezes é a técnica, às vezes o produto; "contexto" nomeia coisas de três níveis diferentes.

Sem desambiguar, duas pessoas discutem arquitetura falando de coisas distintas com a mesma palavra — e a discussão que parecia técnica era de vocabulário.

Este capítulo fixa os termos, dá a linhagem, e entrega o mapa de entrada por sintoma. É o capítulo ao qual os outros voltam.

## Fundamentos científicos

- **A herança** — *Information Retrieval* é um campo com décadas de acumulação: SIGIR, TREC, e um corpo de métricas, benchmarks e métodos que o RAG herdou quase inteiro. **Neural IR** é a virada que trouxe representações densas para dentro dele. Ignorar essa linhagem é reinventar mal o que já estava resolvido. `[a validar]`
- **A absorção** — a comunidade de IR não tratou o RAG como estranho: criou **track dedicado no TREC**, com avaliação de atribuição de fonte e completude, não só de correção. É o sinal mais forte de que RAG é subcampo de IR, e não disciplina paralela. `[a validar]`
- **A sistematização** — a survey de Gao et al. ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)) organiza a área em *"the tripartite foundation… the **retrieval**, the **generation** and the **augmentation** techniques"* e em três paradigmas — *"the **Naive RAG**, the **Advanced RAG**, and the **Modular RAG**"*. É a referência mais citada e a espinha dos caps. 02 e 03. ✓
- **A degradação que justifica recuperar** — *Lost in the Middle* ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)) mede que o aproveitamento é melhor nas pontas e cai no meio, *"even for explicitly long-context models"*. Não é detalhe de tuning: é a razão empírica de "mandar tudo" ser anti-padrão (cap. 20). ✓

(Bibliografia completa: [`bibliografia.md`](bibliografia.md).)

## O estado da arte

### 1. O vocabulário mínimo

| Termo | O que é neste livro | O que **não** é |
|---|---|---|
| **recuperação** (*retrieval*) | selecionar trechos de um corpus por relevância a uma consulta | não é RAG |
| **RAG** | recuperação **+** geração fundamentada no recuperado | não é "busca com LLM em cima" |
| **corpus** | o conjunto de documentos que o sistema pode consultar | não é o índice |
| **índice** | a estrutura que torna o corpus buscável | não é o corpus |
| **chunk** | a unidade indexada e recuperada | não é parágrafo, necessariamente |
| **embedding** | representação vetorial para medir similaridade | não é compreensão |
| **candidatos** | o que a busca devolve, antes de reordenar | não é o contexto |
| **contexto** | o que efetivamente vai para o modelo, montado | não é tudo que foi recuperado |
| **fundamentação** (*grounding*) | a resposta ser sustentada pelo que foi recuperado | não é a resposta estar correta |

### 2. As três confusões que mais custam

**Recuperação ≠ RAG.** Buscar é metade. RAG é buscar *e* gerar uma resposta sustentada no que se buscou — e a maior parte das falhas de produção mora na segunda metade (caps. 15 e 21). Times que medem só recuperação declaram vitória cedo demais.

**Candidatos ≠ contexto.** Entre "a busca devolveu 50" e "o modelo recebeu 5" há decisões — quantos, em que ordem, comprimidos ou não. É a camada de **aumento** do cap. 02, e ela costuma não ter dono.

**Fundamentada ≠ correta.** Uma resposta pode estar certa e não ser fundamentada (o modelo respondeu de memória), ou errada e perfeitamente fundamentada (o corpus estava errado). São dois eixos independentes, e confundi-los faz o time consertar no lugar errado (caps. 15, 21).

### 3. De onde o RAG vem

Vale situar, porque muda a postura de quem constrói:

- **O que o RAG herdou de IR:** a arquitetura em estágios (recuperar barato → reordenar caro), as métricas (precisão, recall, ordenação), a cultura de benchmark (TREC, BEIR), e a noção de que relevância é medida, não opinada.
- **O que o RAG acrescentou:** um consumidor que **lê** os resultados em vez de mostrá-los a uma pessoa. Isso muda o que é "bom": não basta o certo estar entre os dez primeiros — ele precisa caber no orçamento, estar em ordem aproveitável, e vir com procedência para ser citado.
- **O que ainda é problema aberto:** avaliar a geração fundamentada com o mesmo rigor com que IR avalia recuperação. É onde a área está mais imatura (cap. 21).

A moral prática: **quando um problema deste livro parecer novo, verifique se IR não o resolveu em 1998.** Frequentemente resolveu.

### 4. A taxonomia por sintoma

A forma útil de entrar no livro não é pelo sumário — é pelo sintoma:

| Sintoma observado | Natureza | Onde ler |
|---|---|---|
| Cita documento revogado ou desatualizado | corpus | 04 |
| Não encontra identificador, código, sigla | busca (falta esparsa) | 06 |
| Não encontra paráfrase | busca (falta densa) ou representação | 05, 06 |
| Traz o trecho certo sem contexto suficiente | chunking / indexação | 05, 09 |
| Traz relevante e irrelevante junto | reranking, `top_k` | 07 |
| Degrada da terceira pergunta em diante | referência entre turnos | 08, 19 |
| Precisa juntar informação de vários documentos | multi-hop | 10, 18 |
| "Quais os temas de tudo isso?" | pergunta global | 10 |
| Recupera certo e responde errado | geração | 15 |
| Responde certo mas não sei se usou a fonte | fundamentação | 15, 21 |
| Inventa quando não sabe | abstenção | 06, 15 |
| Piorou e ninguém sabe quando | observabilidade | 21 |
| Um documento fez o sistema agir errado | segurança | 22 |
| Funciona e custa demais | custo | 23 |

### 5. A cláusula de expiração

A tese que o livro assume: **boa parte do que se descreve aqui é temporária, e a honestidade é dizer qual parte.**

O critério, que você pode aplicar contra este livro:

- **A técnica compensa uma limitação do modelo?** Expira quando a limitação expirar. Muita coisa de 2023 morreu assim.
- **A técnica assume um preço ou um tamanho de janela?** Expira quando a economia mudar — e ela mudou de ordem de grandeza mais de uma vez.
- **A técnica resolve um problema de informação?** (o que não está nos pesos, o que não cabe, o que não pode ser confiado) Provavelmente **não** expira: muda de forma, não de existência.

O que este livro aposta que sobrevive: a **arquitetura em estágios**, a exigência de **procedência**, a distinção **fundamentada × correta**, e a disciplina de **medir**. São propriedades do problema, não do modelo da vez.

O placar das apostas, com data e critério, está no [registro de expiração](HISTORICO.md).

### Leitura executiva

**Três confusões custam caro:** recuperação **≠** RAG (buscar é metade, e a maioria das falhas de produção está na outra); candidatos **≠** contexto (entre os 50 devolvidos e os 5 enviados há decisões sem dono); e **fundamentada ≠ correta** — são eixos independentes, e confundi-los faz consertar no lugar errado. **A herança que muda a postura:** RAG é subcampo de *Information Retrieval*, com track próprio no TREC; herdou a arquitetura em estágios, as métricas e a cultura de benchmark, e acrescentou um consumidor que **lê** os resultados em vez de mostrá-los — o que muda o que significa "bom": não basta estar entre os dez primeiros, precisa caber no orçamento e vir com procedência. **Quando um problema parecer novo aqui, verifique se IR não o resolveu em 1998.** **O que roubar:** entre no livro pela **tabela de sintomas**, com o seu problema real na mão. **O que vai expirar:** o que compensa limitação de modelo ou assume um preço. **O que não:** arquitetura em estágios, procedência, a distinção fundamentada×correta, e medir.

## Mão na massa — rag-zero, etapa 0

Na etapa 0 você levanta o chão do `rag-zero`: um chat mínimo sobre FastAPI, com o modelo atrás de uma `LLMPort`, e um instrumento que vai acompanhar o livro inteiro — o **contador que imprime, por requisição, quantos tokens vieram de cada bloco do contexto**. Nenhuma técnica de RAG ainda. Só o chão e o instrumento.

## Verificação

1. Um colega diz "nosso recall está em 0,92, o RAG está pronto". O que falta medir, e por quê?
2. Classifique na taxonomia: *"o assistente responde bem a perguntas isoladas, mas erra quando o usuário faz três seguidas sobre o mesmo assunto"*.
3. Escolha uma técnica que você usa hoje e aplique o critério de expiração. Ela sobrevive a modelos duas vezes melhores?
