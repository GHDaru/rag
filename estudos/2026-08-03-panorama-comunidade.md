# Panorama da comunidade — engenharia de prompt, engenharia de contexto e RAG

> Nota de pesquisa · captura em **2026-08-03** · insumo para o sumário da edição 0.1.
> Levantamento de reconhecimento: mapeia o terreno e justifica a estrutura do livro.
> **Não é bibliografia validada** — os itens marcados `[a validar]` só entram no corpo dos capítulos depois de passarem pela skill `academic-research` (Princípio I).

## 1. A pergunta que originou o livro

> *"Engenharia de contexto poderia assumir como substituto do RAG?"*

**Não como substituto — como moldura.** As duas coisas não estão no mesmo nível de abstração:

| | Engenharia de contexto | RAG |
|---|---|---|
| **O que é** | a disciplina de decidir **quais tokens ocupam a janela** em tempo de inferência | uma **técnica** de preencher parte desses tokens buscando em um corpus externo |
| **Escopo** | instrução, few-shot, histórico, memória, resultado de ferramenta, estado do ambiente, *e* trechos recuperados | os trechos recuperados |
| **Decisão típica** | "o que cabe, em que ordem, e o que sai quando faltar espaço" | "que trechos deste corpus respondem a esta pergunta" |
| **Falha típica** | *context rot*, contexto podre, orçamento estourado, instrução afogada | recall baixo, chunk cortado no meio, resposta não fundamentada |

Ou seja: **RAG é um subconjunto próprio da engenharia de contexto** — o subconjunto que resolve o problema "o conhecimento não está nos pesos e não cabe todo na janela". Quem troca o rótulo "RAG" por "engenharia de contexto" e continua fazendo a mesma coisa só renomeou o pipeline. Quem adota a moldura passa a fazer perguntas que o RAG sozinho não faz: *quanto* do orçamento vale gastar com recuperação, se aquele trecho compete com a memória de longo prazo, se recuperar agora ou deixar o agente decidir depois.

A literatura sustenta essa hierarquia: o survey de engenharia de contexto trata RAG explicitamente como uma das **implementações** construídas sobre os componentes (recuperação/geração, processamento e gestão de contexto), ao lado de sistemas de memória, raciocínio integrado a ferramentas e sistemas multiagente ([arXiv 2507.13334](https://arxiv.org/abs/2507.13334)).

**Consequência editorial**, adotada como Princípio VIII: o livro trata **duas disciplinas em relação** — prompt (o que se escreve) e contexto (o que se monta em runtime) — e o RAG ocupa três capítulos dentro da segunda, não o título do livro.

## 2. A academia

### 2.1 Os três surveys que ancoram as três partes

| Survey | Papel no livro | Status |
|---|---|---|
| **The Prompt Report: A Systematic Survey of Prompting Techniques** — [arXiv 2406.06608](https://arxiv.org/abs/2406.06608) | Ancora a Parte I. Cataloga **58 técnicas de prompting textual** e **33 termos de vocabulário**, organizadas em seis famílias: *zero-shot*, *few-shot*, *thought generation*, *ensembling*, *self-criticism*, *decomposition*. É a taxonomia mais citada da área e a espinha do nosso `apendice-tecnicas.md`. | `[a validar]` |
| **A Survey of Context Engineering for Large Language Models** — [arXiv 2507.13334](https://arxiv.org/abs/2507.13334) | Ancora a Parte II. Sistematiza a disciplina a partir de **1400+ papers**, com a taxonomia em três componentes (recuperação e geração de contexto · processamento de contexto · gestão de contexto) e quatro implementações (RAG · memória · *tool-integrated reasoning* · multiagente). Traz também o achado que vira tese do livro: a **assimetria** entre a capacidade dos modelos de *compreender* contexto complexo e a de *produzir* saída igualmente complexa. | `[a validar]` |
| **Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG** — [arXiv 2501.09136](https://arxiv.org/abs/2501.09136) | Ancora o cap. 11. Formaliza o RAG em que um agente **decide** a estratégia de recuperação (reflexão, planejamento, uso de ferramenta, colaboração multiagente) em vez de executar um pipeline fixo. | `[a validar]` |

Complementos de segunda ordem, úteis mas não estruturantes: *Exploring Prompt Engineering: A Systematic Review with SWOT Analysis* ([arXiv 2410.12843](https://arxiv.org/abs/2410.12843)); *A Systematic Review of Key RAG Systems* ([arXiv 2507.18910](https://arxiv.org/abs/2507.18910)); *Context Engineering 2.0* ([arXiv 2510.26493](https://arxiv.org/abs/2510.26493)).

### 2.2 Os papers canônicos por problema

Estes são os que provavelmente aparecem como fundamento citado dentro dos capítulos:

- **Degradação posicional** — *Lost in the Middle* ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)): informação no meio de contexto longo é mal utilizada. Fundamenta o cap. 08 e mata o instinto de "mandar tudo". `[a validar]`
- **Raciocínio em passos** — Chain-of-Thought; **Self-Consistency** (amostrar vários caminhos e votar); **ReAct** (ciclo pensamento → ação → observação, que é a ponte entre a Parte I e o RAG agêntico). Fundamentam o cap. 03. `[a validar]`
- **Contexto longo × recuperação** — *U-NIAH: Unified RAG and LLM Evaluation for Long Context Needle-In-A-Haystack* ([arXiv 2503.00353](https://arxiv.org/abs/2503.00353)): avaliação unificada dos dois regimes no mesmo teste. É a evidência que sustenta a leitura híbrida do cap. 08. `[a validar]`
- **Chunking** — *Reconstructing Context: Evaluating Advanced Chunking Strategies for RAG* ([arXiv 2504.19754](https://arxiv.org/abs/2504.19754)): compara as estratégias avançadas em vez de assumi-las. Fundamenta o cap. 09. `[a validar]`
- **Otimização automática de prompt** — **GEPA** (otimizador reflexivo genético-Pareto, avaliado contra GRPO e MIPROv2) e **TextGrad** (o prompt como variável textual otimizável, com "gradiente" em linguagem natural). Fundamentam o cap. 06. `[a validar]`

### 2.3 O que a academia ainda não fechou (as fronteiras)

Três disputas abertas que o livro deve registrar **como disputas**, não como consenso:

1. **Onde para a janela e começa a recuperação.** A leitura de 2026 é híbrida — recuperar um conjunto focado e raciocinar em contexto longo sobre ele — mas o ponto de corte varia por modelo, por forma do dado e por orçamento de latência. Ninguém tem a regra universal.
2. **Memória × recuperação.** Memória de agente e RAG resolvem problemas parecidos com arquiteturas diferentes (fatos extraídos e reescritos × trechos recuperados na íntegra). A fronteira entre "isso é memória" e "isso é retrieval sobre o histórico" ainda é decidida caso a caso.
3. **Avaliação.** Não existe um benchmark único de RAG; a prática é combinar dois ou três cobrindo estágios diferentes (recuperação pura × geração fundamentada). Métricas por LLM-as-judge são o padrão de fato e a fraqueza metodológica ao mesmo tempo.

## 3. A indústria e os repositórios públicos

### 3.1 As coleções vivas (o mapa que a comunidade mantém)

| Repositório | O que é | Papel no livro |
|---|---|---|
| [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/prompt-engineering-guide) | O guia de referência da área — guias, papers, notebooks. Notável: **já cobre prompt engineering, context engineering, RAG e agentes no mesmo repositório**, o que é evidência independente de que o par é uma coisa só. | Referência de entrada; comparar cobertura por capítulo. |
| [Meirtz/Awesome-Context-Engineering](https://github.com/Meirtz/Awesome-Context-Engineering) | Coleção do survey 2507.13334 — centenas de papers, frameworks e guias de implementação. | Fonte de garimpo para o Apêndice A dos caps. 08–14. |
| [asinghcsu/AgenticRAG-Survey](https://github.com/asinghcsu/AgenticRAG-Survey) | Companion do survey de RAG agêntico. | Fonte do cap. 11. |
| [promptslab/Awesome-Prompt-Engineering](https://github.com/promptslab/awesome-prompt-engineering), [natnew/Awesome-Prompt-Engineering](https://github.com/natnew/Awesome-Prompt-Engineering) | Coleções curadas de prompt. | Garimpo do catálogo de técnicas. |
| Tópico [`context-engineering`](https://github.com/topics/context-engineering) no GitHub | O termômetro do que a comunidade está publicando agora. | Insumo do futuro Radar (rodada 6). |

### 3.2 Frameworks e ferramentas, por problema que resolvem

Organizado pelo problema — não por popularidade, e nunca como recomendação (Princípio VI):

- **Otimizar prompt automaticamente**: **DSPy** (com os otimizadores BootstrapFewShot, COPRO, **MIPROv2** e **GEPA**), [gepa-ai/gepa](https://github.com/gepa-ai/gepa), **TextGrad**, **Promptomatix** ([arXiv 2507.14241](https://arxiv.org/abs/2507.14241)). A tese comum: o prompt deixa de ser artesanato e vira artefato compilado contra uma métrica.
- **Recuperar**: o eixo denso (embeddings + vector store) × esparso (BM25) × **híbrido com fusão de ranking**, mais **reranking** como terceiro estágio. As técnicas de fronteira são **Contextual Retrieval** (prefixar cada chunk com um resumo do seu lugar no documento, antes de embeddar) e **Late Chunking** (embeddar o documento inteiro e só então cortar, antes do pooling — mais barato, porque usa só o modelo de embedding).
- **Lembrar**: **Mem0** (extração de fatos salientes em memórias compactas; ~41k estrelas), **Zep** (grafo de conhecimento **temporal** sobre recuperação densa, para raciocinar sobre fatos que mudam), **Letta/MemGPT** (o LLM como SO que pagina sua própria memória entre *main context*, *recall* e *archival*). Três arquiteturas, três trade-offs — material do cap. 12.
- **Avaliar**: **RAGAS** (as quatro métricas de fato: *faithfulness*, *answer relevance*, *context precision*, *context recall*), **DeepEval** (as mesmas ideias com integração de CI/CD), **TruLens**; e do lado da recuperação pura, **BEIR** e **MTEB**. Material do cap. 15.
- **Atacar e defender**: **OWASP Top 10 for LLM Applications** — *prompt injection* é **LLM01 em todas as edições publicadas**, de 2023 até a lista vigente. As defesas recomendadas são de profundidade (separar instrução de dado, menor privilégio nas ferramentas, filtragem de entrada/saída, aprovação humana para ação de alto risco, teste adversarial recorrente). Material do cap. 16.

### 3.3 Os números que a indústria publicou (e que precisam de contexto experimental)

Anotados aqui **com a ressalva do Princípio I**: são medições do próprio proponente, em corpus próprio, e servem de hipótese a reproduzir — não de fato estabelecido.

- **Contextual Retrieval** (Anthropic, fim de 2024): embeddings contextuais sozinhos reduziriam a falha de recuperação em top-20 em ~35%; combinados com BM25, ~49%; somando reranking, ~67%. O padrão que interessa não é o número — é a **forma da curva**: os três estágios são cumulativos, e o reranking é o que mais paga por último.
- **Memória**: Zep reporta 94,7% em LoCoMo e 90,2% em LongMemEval. Números de fornecedor, em benchmark que o fornecedor escolheu.

O livro trata estes números como o Princípio I manda: citáveis com a fonte e a condição ao lado, jamais como "está provado que".

## 4. O que este panorama recomenda para o sumário

1. **Três partes, não duas.** Prompt (o que se escreve) → Contexto (o que se monta) → Sistema (avaliar, proteger, pagar a conta). A terceira parte existe porque avaliação e segurança atravessam as duas primeiras e morreriam espalhadas.
2. **RAG em três capítulos, não em um.** A distância entre "busca híbrida com reranking" (cap. 09), "contextual retrieval e GraphRAG" (cap. 10) e "o agente decide quando recuperar" (cap. 11) é grande demais para um capítulo só — e é exatamente onde a maioria dos projetos trava.
3. **Otimização automática de prompt merece capítulo próprio** (cap. 06). É a mudança mais estrutural da Parte I: separa quem escreve prompt à mão de quem compila prompt contra métrica.
4. **A tensão contexto longo × recuperação é um capítulo, não uma nota de rodapé** (cap. 08). É a pergunta que todo leitor traz.
5. **O catálogo de técnicas vira apêndice de referência**, separado dos capítulos (Diátaxis: *reference* nunca se mistura com *explanation*).

## 5. Método deste levantamento

Busca aberta na web em 2026-08-03, cruzando quatro eixos (survey acadêmico · repositório público · framework de produção · fonte de fornecedor) para cada um dos três temas. Critério de inclusão: aparecer em pelo menos duas buscas independentes **ou** ser fonte primária de uma técnica nomeada. Nenhum item foi lido na íntegra nesta passada — por isso `[a validar]`. A validação (leitura, conferência de número, registro em `livro/bibliografia.md` com status ✓) é trabalho da **rodada 2** do [ROADMAP](../ROADMAP.md).

**Viés declarado**: buscas em inglês, motor único, sem acesso a bases pagas. Literatura não indexada e trabalho publicado fora de arXiv/GitHub está sub-representado.
