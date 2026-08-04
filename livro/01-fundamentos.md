# 01 — Fundamentos

> **Estado da arte capturado em 2026-08** · edição 0.1 (esqueleto) · [histórico e registro de expiração](HISTORICO.md)
>
> **Maturidade: fundação.** O vocabulário e a taxonomia estão fechados. As referências marcadas `[a validar]` viram citação com status ✓ na rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Definir** os termos que o livro inteiro usa: janela, token, contexto, prompt, chunk, embedding, recuperação, memória;
2. **Descrever** o caminho de uma requisição — o que o sistema monta antes de a inferência começar;
3. **Classificar** um problema real na taxonomia por sintoma (é prompt? é recuperação? é orçamento? é memória?);
4. **Aplicar** a cláusula de expiração: identificar, num texto técnico desta área, o que provavelmente não vale mais em 18 meses.

## O problema

Todo campo novo sofre de vocabulário instável, e este sofre mais do que a média: "contexto" nomeia ao mesmo tempo a janela física do modelo, o conteúdo que se coloca nela, o arquivo de regras do projeto e a disciplina inteira. Sem desambiguar, duas pessoas discutem arquitetura falando de coisas diferentes com a mesma palavra.

Este capítulo fixa os termos e desenha o mapa. É o capítulo de referência ao qual os outros voltam.

## Fundamentos científicos

- **A disciplina tem taxonomia formal.** O survey *A Survey of Context Engineering for LLMs* ([arXiv 2507.13334](https://arxiv.org/abs/2507.13334)) organiza a área a partir de 1400+ trabalhos em três **componentes** — recuperação e geração de contexto, processamento de contexto, gestão de contexto — e quatro **implementações** que os combinam: RAG, sistemas de memória, raciocínio integrado a ferramentas e sistemas multiagente. Esta é a espinha da Parte II do livro. `[a validar]`
- **O prompting também tem taxonomia formal.** *The Prompt Report* ([arXiv 2406.06608](https://arxiv.org/abs/2406.06608)) cataloga 58 técnicas de prompting textual e 33 termos de vocabulário, em seis famílias: *zero-shot*, *few-shot*, *thought generation*, *ensembling*, *self-criticism* e *decomposition*. É a espinha da Parte I. `[a validar]`
- **A degradação não é linear.** *Lost in the Middle* ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)) mostra que informação posicionada no meio de um contexto longo é sistematicamente pior aproveitada do que a que está nas bordas. Não é um detalhe de tuning: é uma restrição arquitetural que decide onde cada coisa vai. `[a validar]`

(Bibliografia completa e status de validação: [`bibliografia.md`](bibliografia.md).)

## Fontes da indústria

- **[Prompt Engineering Guide](https://github.com/dair-ai/prompt-engineering-guide)** (DAIR.AI) — o guia de referência da área. O dado editorial mais interessante não é o conteúdo, é o índice: o mesmo repositório cobre *prompt engineering*, *context engineering*, *RAG* e *agentes*. A comunidade já trata o par como uma coisa só.
- **[Awesome-Context-Engineering](https://github.com/Meirtz/Awesome-Context-Engineering)** — a coleção viva associada ao survey 2507.13334; ponto de partida do garimpo de cada capítulo da Parte II.
- **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** — fixa o vocabulário de risco que o cap. 16 usa; *prompt injection* é LLM01 em todas as edições publicadas.

## O estado da arte

### 1. O vocabulário mínimo

| Termo | O que é neste livro | O que **não** é |
|---|---|---|
| **token** | a unidade que o modelo processa e que a fatura cobra | não é palavra |
| **janela de contexto** | o limite físico de tokens de uma chamada | não é "memória do modelo" |
| **contexto** | o conteúdo efetivamente montado para uma chamada | não é a janela (o limite) nem o arquivo de regras (uma das fontes) |
| **prompt** | a parte do contexto que é instrução autoral e estável | não é o contexto todo |
| **chunk** | o pedaço de documento que é indexado e recuperado como unidade | não é parágrafo, necessariamente |
| **embedding** | representação vetorial usada para medir similaridade semântica | não é compreensão |
| **recuperação (*retrieval*)** | selecionar trechos de um corpus por relevância a uma consulta | não é RAG (RAG = recuperação **+** geração fundamentada) |
| **memória** | estado que sobrevive além do turno atual, deliberadamente mantido | não é o histórico bruto da conversa |
| **orçamento de contexto** | a alocação explícita de tokens entre os concorrentes | não é "o que couber" |

A distinção que mais rende no dia a dia é a última linha da tabela do meio: **recuperação não é RAG**. Buscar é metade. RAG é buscar *e* gerar uma resposta fundamentada no que se buscou — e o segundo termo é onde mora a maior parte das falhas de produção (cap. 15).

### 2. O caminho de uma requisição

Toda arquitetura desta área, por mais elaborada, é uma variação deste caminho:

```
pedido do usuário
   │
   ├─ [prompt]     instrução + exemplos + formato pedido      ← Parte I
   ├─ [regras]     política do sistema, persona, restrições   ← cap. 05
   ├─ [memória]    o que ficou de sessões anteriores          ← cap. 12
   ├─ [recuperado] trechos buscados no corpus                 ← caps. 09-11
   ├─ [ferramenta] resultados de chamadas externas            ← cap. 14
   └─ [histórico]  os turnos desta conversa (talvez compactado) ← cap. 13
   │
   ▼
   MONTAGEM  ── decide ordem, corte e orçamento ──────────────  cap. 08
   ▼
   inferência ──► resposta ──► avaliação (cap. 15) e custo (cap. 17)
```

Duas leituras deste desenho valem o capítulo inteiro:

- **A montagem é o produto.** Os componentes são commodities — todo mundo tem um vector store, todo mundo tem um modelo. A diferença de qualidade entre dois sistemas está quase sempre na linha "MONTAGEM": o que entra, em que ordem, e o que é sacrificado quando falta espaço.
- **Os concorrentes disputam o mesmo orçamento.** Memória, recuperação, histórico e resultado de ferramenta competem por tokens. Aumentar o `top_k` da recuperação não é uma decisão isolada: é tirar espaço de outro. Quase nenhum sistema em produção declara essa alocação explicitamente — e é por isso que quase todos degradam quando a conversa fica longa.

### 3. A taxonomia por sintoma

O jeito útil de entrar no livro não é por tema, é por sintoma. Leve o seu problema real a esta tabela:

| Sintoma observado | Provável natureza | Onde ler |
|---|---|---|
| A resposta varia muito entre execuções idênticas | prompt (falta de âncora ou de formato) | caps. 02, 04 |
| O modelo erra em tarefas que exigem passos | prompt (falta de estratégia de raciocínio) | cap. 03 |
| "Melhorei o prompt" e não sei se melhorou | falta de eval | cap. 07 |
| O modelo não sabe informação da minha organização | contexto (falta recuperação) | cap. 09 |
| Ele recupera coisa errada / não encontra o óbvio | recuperação (chunking, busca, ranking) | caps. 09, 10 |
| Ele recupera certo mas responde errado | geração não fundamentada | cap. 15 |
| Piora quando a conversa fica longa | orçamento e *context rot* | caps. 08, 13 |
| Esquece o que o usuário disse semana passada | memória | cap. 12 |
| Um documento fez o agente agir contra o usuário | segurança (*prompt injection*) | cap. 16 |
| Funciona, mas custa/demora demais | custo, latência, cache | cap. 17 |

### 4. A cláusula de expiração

A tese que o livro assume desde o primeiro capítulo: **boa parte do que se descreve aqui é temporária, e a honestidade é dizer qual parte.**

Três forças fazem o conteúdo expirar nesta área, em velocidades diferentes:

1. **Capacidade do modelo.** Toda técnica que existe para compensar uma limitação some quando a limitação some. Muita engenharia de prompt de 2023 morreu porque os modelos passaram a fazer aquilo sozinhos.
2. **Preço e janela.** Decisões de orçamento assumem uma relação custo/token e um tamanho de janela. Ambos mudaram de ordem de grandeza mais de uma vez.
3. **Padronização.** O que hoje é técnica manual vira funcionalidade de plataforma (saída estruturada é o caso exemplar) — e o capítulo que ensinava a fazer na mão vira história.

O que **não** expira, e é onde o livro aposta seu peso: o raciocínio de **orçamento** (o que vale a pena ocupar a janela), a **separação instrução × dado** (que é segurança, não estilo) e a **disciplina de medir** — porque essas são propriedades do problema, não do modelo da vez.

O registro dessas apostas, com data e veredito posterior, fica no [registro de expiração](HISTORICO.md).

### Leitura executiva

**Contexto** é o que se monta; **janela** é o limite; **prompt** é a parte autoral e estável; **recuperação não é RAG** (RAG é recuperação + geração fundamentada). Toda arquitetura da área é uma variação do mesmo caminho, e o produto está na linha da **montagem** — porque os concorrentes (prompt, memória, recuperado, ferramenta, histórico) disputam **um orçamento único** que quase ninguém declara. **O que roubar:** entre no livro pela tabela de sintomas, não pelo sumário; e escreva a alocação de tokens do seu sistema em uma linha antes de mexer em qualquer `top_k`. **O que vai expirar:** as técnicas que compensam limitação de modelo. **O que não vai:** orçamento, separação instrução×dado, e medir.

## Mão na massa — contexto-zero, etapa 0

Na etapa 0 você levanta o esqueleto do `contexto-zero`: um chat mínimo (HTML+JS) sobre FastAPI, com o modelo atrás de uma `LLMPort` — a porta que impede o livro inteiro de apodrecer junto com um fornecedor. Nenhuma técnica ainda: só o chão sobre o qual as quinze etapas seguintes se apoiam, e um script que imprime a **contagem de tokens de cada bloco** do contexto montado. Esse contador é o instrumento do livro: você vai olhar para ele em todos os capítulos.

> A trilha prática entra na **rodada 3** do ROADMAP. Nesta edição, as seções "Mão na massa" descrevem a etapa e seu objetivo pedagógico.

## Verificação

1. Um colega diz "aumentei a janela para 200k, agora não preciso mais de RAG". Cite duas razões — uma de qualidade, uma de custo — para duvidar.
2. Classifique na taxonomia por sintoma: *"o assistente responde bem nas primeiras 5 perguntas e depois começa a ignorar as regras do sistema"*. Qual é a natureza do problema e por quê?
3. Aponte, no seu próprio sistema, quem são os concorrentes pelo orçamento de contexto. Qual deles você nunca mediu?
