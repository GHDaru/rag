# Bibliografia

> Fontes científicas e da indústria, por capítulo, com **status de validação**.
>
> Edição 0.4 · captura em 2026-08 · **rodada 2 (evidência) — concluída no critério de validação**.

## Como ler o status (Princípio I da constituição)

| Status | Significa |
|---|---|
| ✓ | **Validada** — a referência foi localizada, lida no essencial, e a afirmação que o livro faz sobre ela foi conferida contra o texto original. Pode ser citada no corpo de um capítulo. |
| ⏳ | **A validar** — ID e título **conferidos contra o arXiv**, mas o texto não foi lido e a afirmação do livro não foi checada. Aparece nos capítulos marcada como `[a validar]`. |
| ✗ | **Rejeitada** — não sustenta a afirmação que o livro fazia. Fica registrada com o motivo, porque saber o que **não** vale é resultado. |

### O que a rodada 2 fez, e o que ainda não fez

**Feito — as duas levas:**

1. **Todos os 49 identificadores arXiv do repositório foram resolvidos contra o arXiv real**, com um ID falso como controle (que devolve *"Article identifier not recognized"*, provando que o teste discrimina). **Nenhum ID inventado, nenhum título divergente.** A classe de erro mais corrosiva para um livro — a citação alucinada — está descartada.
2. **42 das 55 referências (76%) passaram à validação plena (✓)**: o texto foi lido e a afirmação que o livro faz sobre elas, conferida. Isso cumpre o critério de conclusão da rodada 2 (≥ 60%).
3. **~20 técnicas nomeadas que estavam sem URL ganharam fonte primária.** Elas tinham entrado pela porta dos guias de praticante (RAPTOR, Self-RAG, CRAG, FLARE, Adaptive RAG, HyDE, step-back, late chunking, proposição, GraphRAG…) e agora apontam para o paper que as propôs.
4. **Quatro afirmações do livro foram corrigidas** contra a fonte — ver *Correções* abaixo. Duas delas atingiam a espinha de um capítulo.

**Não feito:** 13 referências seguem ⏳ — com ID conferido e texto não lido. São, por desenho, as de menor peso estrutural: otimizadores secundários de prompt (P7–P10), modos de falha de memória (M2–M5), e três de escopo estreito (Q3, E3, Z1). Nenhuma sustenta sozinha uma tese de capítulo. Falta também **preencher os Apêndices A**, que é o item restante do critério de conclusão.---

## Correções que esta rodada produziu

> Registradas por inteiro porque, pelo Princípio I, **o que a evidência derruba vale tanto quanto o que ela sustenta**.

### ✗ C1 — *Lost in the Middle* não sustentava a afirmação do cap. 20

A edição 0.2 afirmava que a degradação em contexto longo **"não é linear com o comprimento: é dirigida pela similaridade entre alvo e distratores"**, ancorada em [arXiv 2307.03172](https://arxiv.org/abs/2307.03172). Lido o original: o paper estabelece degradação **posicional** — *"performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle"* — e **não trata de distratores nem de similaridade semântica**.

A fonte correta é o relatório *Context Rot* da Chroma (abaixo) — que, lido, **contradiz a outra metade da afirmação**: isolando a variável, o comprimento degrada **sozinho**, mesmo em tarefas triviais. O livro dizia "não é o comprimento"; o certo é **"é o comprimento, e distratores próximos tornam a queda mais íngreme"**. Corrigido no cap. 20 e no glossário.

### ✗ C2 — as quatro métricas não são todas do paper do RAGAS

O livro atribuía ao paper do RAGAS o quarteto *faithfulness · answer relevance · context precision · context recall*. Lido o original ([arXiv 2309.15217](https://arxiv.org/abs/2309.15217), EACL 2024): *"We focus in particular three quality aspects… First, **Faithfulness**… Second, **Answer Relevance**… Finally, **Context Relevance**"*. O par *context precision / context recall* é da **biblioteca**, que desdobrou *context relevance* em duas. Corrigido no cap. 21, no glossário e no apêndice do ecossistema.

> Nota de método: a primeira consulta automática a este PDF devolveu uma citação inventada afirmando *"We propose four metrics"*. O erro só apareceu porque o texto foi extraído e lido diretamente. **Resumo automático de fonte não é validação** — é exatamente o que o status ✓ existe para impedir.

### ✗ C4 — a escolha entre *contextual retrieval* e *late chunking* não é só de preço

O cap. 09 afirmava que as duas técnicas resolvem a mesma falha e que a decisão entre elas é **"aritmética, não estética"** — ou seja, só orçamento. A comparação direta ([arXiv 2504.19754](https://arxiv.org/abs/2504.19754)) mede outra coisa: *"**contextual retrieval preserves semantic coherence more effectively** but requires greater computational resources. In contrast, **late chunking offers higher efficiency but tends to sacrifice relevance and completeness**"*. Há **troca de qualidade**, não só de custo. Corrigido no cap. 09 — a decisão tem dois eixos.

### ⚠ C3 — o `67%` do *contextual retrieval*, com a condição ao lado

O caso de deriva que o [panorama §6.2](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md) documentava agora tem os números da fonte primária. Todos sobre a **taxa de falha de recuperação no top-20**, partindo de **5,7%**:

| Configuração | Taxa de falha | Redução |
|---|:---:|:---:|
| linha de base | 5,7% | — |
| *Contextual Embeddings* | 3,7% | **35%** |
| + *Contextual BM25* | 2,9% | **49%** |
| + reranking | 1,9% | **67%** |

O `67%` é **a pilha inteira, com reranker** — e circula em fontes secundárias como mérito da técnica sozinha. Custo declarado: contexto de 50–100 tokens por chunk, gerado por um modelo pequeno, a **US$ 1,02 por milhão de tokens de documento** com cache de prompt.

---

## Fundacionais e surveys estruturantes

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| **F0** | **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** — [arXiv 2005.11401](https://arxiv.org/abs/2005.11401) (Lewis et al., 2020) | o paper que cunha o termo: combinar memória **paramétrica** e **não-paramétrica**; e já levanta *"providing provenance for their decisions"* como problema — a procedência do cap. 02 nasce aqui | ✓ |
| **S0** ⭐ | **Retrieval-Augmented Generation for LLMs: A Survey** — [arXiv 2312.10997](https://arxiv.org/abs/2312.10997) (Gao et al.) | a taxonomia **Naive → Advanced → Modular** (caps. 01, 03) e a base tripartite **retrieval · generation · augmentation** (cap. 02), ambas verbatim no abstract | ✓ |
| **S5b** ⭐ | **Modular RAG: LEGO-like Reconfigurable Frameworks** — [arXiv 2407.21059](https://arxiv.org/abs/2407.21059) | *"decomposing complex RAG systems into independent modules and specialized operators"*, e que o modular **"transcends the traditional linear architecture"** — o teste de modularidade do cap. 03 | ✓ |
| S1 ⭐ | **The Prompt Report** — [arXiv 2406.06608](https://arxiv.org/abs/2406.06608) | revisão **PRISMA**: 33 termos de vocabulário, **58 técnicas textuais**, 40 para outros modais. A estrutura do cap. 12 é a dela — com a precisão de que *zero-shot* e *few-shot* são irmãos sob **In-Context Learning**, não pares dos outros quatro ramos. Classifica **step-back sob *thought generation***, corroborando a ressalva de Q2 | ✓ |
| S2 | **A Survey of Context Engineering for LLMs** — [arXiv 2507.13334](https://arxiv.org/abs/2507.13334) | síntese de **mais de 1.400 papers**. Componentes: *context retrieval and generation*, *context processing*, *context management*; implementações: **RAG**, sistemas de memória com uso de ferramenta, e multiagente. É o mapa que situa a fronteira com o livro irmão | ✓ |
| S3 ⭐ | **Agentic RAG: A Survey** — [arXiv 2501.09136](https://arxiv.org/abs/2501.09136) | a limitação que justifica o cap. 18 (*"constrained by **static workflows**"*) e os quatro padrões, verbatim: *"reflection, planning, tool use, and multi-agent collaboration"*, para *"dynamically manage retrieval strategies"* | ✓ |
| S4 | *Exploring Prompt Engineering: A Systematic Review with SWOT* — [arXiv 2410.12843](https://arxiv.org/abs/2410.12843) | análise SWOT das técnicas com ênfase em princípios linguísticos; cobre abordagens por template e *fine-tuning*. Peso editorial menor: é análise qualitativa, sem medição | ✓ |
| S5 | *A Systematic Review of Key RAG Systems* — [arXiv 2507.18910](https://arxiv.org/abs/2507.18910) | revisão ano a ano, de QA em domínio aberto ao estado atual; examina mecanismos de recuperação, geração seq2seq e **estratégias de fusão**, e trata do desdobramento em **sistemas de empresa** | ✓ |
| S5c | **Reasoning RAG via System 1 or System 2** — [arXiv 2506.10408](https://arxiv.org/abs/2506.10408) | a divisão que o livro usa entre Partes III e V: ***predefined reasoning*** (*"follows fixed modular pipelines"*) × ***agentic reasoning*** (*"the model **autonomously orchestrates** tool interaction during inference"*) | ✓ |
| S6 | *Context Engineering 2.0* — [arXiv 2510.26493](https://arxiv.org/abs/2510.26493) | argumenta que a prática **antecede o hype em mais de vinte anos** (desde o início dos anos 1990), em fases marcadas pelo nível de inteligência da máquina. Bom antídoto para o cap. 24: o que parece novo raramente é | ✓ |

## 01 — Fundamentos · 20 — A Janela como Orçamento

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| J1 | **Lost in the Middle** — [arXiv 2307.03172](https://arxiv.org/abs/2307.03172) | degradação **posicional**: melhor nas pontas, pior no meio, *"even for explicitly long-context models"*. **Só isso** — ver correção C1 | ✓ |
| J2 ⭐ | **Context Rot: How Increasing Input Tokens Impacts LLM Performance** — [Chroma](https://www.trychroma.com/research/context-rot) (Hong, Troynikov, Huber · 2025-07-14 · **18 modelos**, quatro fornecedores) | (a) isolando a variável, **o comprimento degrada sozinho**, mesmo em tarefas triviais; (b) a queda é mais íngreme quando a similaridade pergunta–alvo é baixa; (c) **um único distrator já reduz o desempenho**, e distratores **não têm impacto uniforme** | ✓ |
| J3 | **U-NIAH** — [arXiv 2503.00353](https://arxiv.org/abs/2503.00353) | contexto longo × RAG no **mesmo protocolo controlado**, com *multi-needle*, *long-needle* e *needle-in-needle*. O detalhe de método que vale copiar: corpus **sintético e ficcional** (*Starlight Academy*) *"to eliminate biases from pre-trained knowledge"* | ✓ |

> **Fonte da indústria, não revisada por pares.** J2 é relatório técnico de uma empresa de banco vetorial — parte interessada no argumento "curadoria supera janela cheia". O livro adota o que o relatório **mede** (protocolo descrito, 18 modelos) e marca a origem. É a mesma régua aplicada aos guias de praticante.

## 04 — Corpus · 05 — Chunking e Representação

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| K1 ⭐ | **Dense X Retrieval: What Retrieval Granularity Should We Use?** — [arXiv 2312.06648](https://arxiv.org/abs/2312.06648) | a **proposição** como unidade: *"atomic expressions… each encapsulating a distinct factoid… concise, self-contained"*; e que a granularidade fina **supera passagem** na recuperação — com ganho a jusante **"given a specific computation budget"** | ✓ |
| K2 ⭐ | **Reconstructing Context: Evaluating Advanced Chunking Strategies for RAG** — [arXiv 2504.19754](https://arxiv.org/abs/2504.19754) | a comparação direta *late chunking* × *contextual retrieval*: o segundo *"preserves semantic coherence more effectively but requires greater computational resources"*; o primeiro *"offers higher efficiency but **tends to sacrifice relevance and completeness**"*. **Ver correção C4** | ✓ |
| K3 | **Adaptive Chunking** — [arXiv 2603.25333](https://arxiv.org/abs/2603.25333) | seleção do método **por documento**, e a lacuna que nomeia: *"chunking **lacks a dedicated evaluation framework**… independently of downstream performance"*. Propõe cinco métricas **intrínsecas** (completude de referências, coesão interna, coerência com o documento, integridade de bloco, conformidade de tamanho) | ✓ |
| K4 | **Cross-Document Topic-Aligned (CDTA) Chunking** — [arXiv 2601.05265](https://arxiv.org/abs/2601.05265) | nomeia *"the knowledge fragmentation problem"* e corta no nível do **corpus**. Números com condição: HotpotQA, *faithfulness* **0,93** × 0,83 (contextual retrieval) × 0,78 (semântico), p < 0,05; em `k = 3`, **0,91** × 0,68. Indexação mais cara, mas *"reduce query-time retrieval needs"* | ✓ |
| K5 | **MemGuard** — [arXiv 2605.28009](https://arxiv.org/abs/2605.28009) | a *heterogeneous memory contamination*: colapsar fatos estáveis, eventos e regras no mesmo espaço faz com que sejam usados *"as interchangeable evidence"*. A cura — **papel funcional explícito no momento da escrita** — é a procedência do cap. 04 aplicada à memória (caps. 19, 22) | ✓ |

> **Lacuna mantida (prioridade da segunda leva).** Segue sem trabalho localizado que meça o impacto **isolado** de frescor, deduplicação e procedência sobre métricas de RAG. Se não existir, vira experimento próprio na rodada 4.

## 06 — Busca · 07 — Reranking

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| B1 ⭐ | **BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of IR Models** — [arXiv 2104.08663](https://arxiv.org/abs/2104.08663) | 18 datasets, 10 sistemas. E as duas afirmações centrais dos caps. 06–07, verbatim: ***"BM25 is a robust baseline"*** e *"re-ranking and late-interaction-based models on average achieve the best zero-shot performances, **however, at high computational costs**"* | ✓ |
| B2 ⭐ | **MTEB: Massive Text Embedding Benchmark** — [arXiv 2210.07316](https://arxiv.org/abs/2210.07316) | 8 tarefas, 58 datasets, 112 idiomas, 33 modelos — e o achado que sustenta a neutralidade do cap. 05: ***"no particular text embedding method dominates across all tasks"*** | ✓ |

## 08 — Entendimento da Consulta

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| Q1 ⭐ | **HyDE** — *Precise Zero-Shot Dense Retrieval without Relevance Labels* — [arXiv 2212.10496](https://arxiv.org/abs/2212.10496) | gerar um documento hipotético e buscar por ele; o encoder *"filtering out the incorrect details"*. **Condição experimental:** proposto para o cenário **zero-shot, sem rótulo de relevância**, comparado a um retriever denso **não supervisionado** — o caso a favor enfraquece quando já existe híbrido bom | ✓ |
| Q2 | **Step-Back Prompting** — *Take a Step Back* — [arXiv 2310.06117](https://arxiv.org/abs/2310.06117) | abstrair para o princípio antes de raciocinar. **Ressalva registrada:** o paper propõe uma técnica de **raciocínio**, avaliada em STEM/QA/multi-hop (PaLM-2L: MMLU Física +7%, Química +11%, TimeQA +27%, MuSiQue +7%) — o uso **como etapa de recuperação** é leitura derivada, do livro e da prática, não do paper | ✓ |
| Q3 | *Sifei at SemEval-2026 Task 8: Hybrid Retrieval and Query Rewriting for Multi-Turn RAG* — [arXiv 2606.28352](https://arxiv.org/abs/2606.28352) | reescrita em conversa. **É um paper de sistema de competição** (SemEval), não um método geral — peso editorial reduzido | ⏳ |

## 09 — Recuperação Avançada

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| V1 ⭐ | **Contextual Retrieval** — [Anthropic](https://www.anthropic.com/engineering/contextual-retrieval) (2024) | prefixar cada chunk com 50–100 tokens de contexto antes de embeddar e de indexar no BM25. **Números e custo na correção C3** — o `67%` é a pilha com reranker | ✓ |
| V2 ⭐ | **Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models** — [arXiv 2409.04701](https://arxiv.org/abs/2409.04701) | *"first embed all tokens of the long text, with chunking applied **after the transformer model and just before mean pooling**"*, e — o ponto econômico do capítulo — ***"works without additional training"***: nenhuma chamada de LLM | ✓ |

## 10 — Recuperação Estruturada

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| G1 ⭐ | **RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval** — [arXiv 2401.18059](https://arxiv.org/abs/2401.18059) | *"recursively embedding, clustering, and summarizing chunks… constructing a tree"*, com recuperação *"at different levels of abstraction"*. **Número com condição:** QuALITY **+20% de acurácia absoluta** sobre o melhor anterior, **acoplado ao GPT-4** | ✓ |
| G2 ⭐ | **GraphRAG** — *From Local to Global: A Graph RAG Approach to Query-Focused Summarization* — [arXiv 2404.16130](https://arxiv.org/abs/2404.16130) | a falha, verbatim: *"RAG fails on global questions directed at an entire text corpus, such as **'What are the main themes in the dataset?'**"* — e o mecanismo em duas etapas: grafo de entidades, depois **resumos de comunidade** pré-gerados. Confirma também a conta do cap. 10: a extração de entidades é etapa extra que o RAPTOR não tem | ✓ |
| G3 | *GraphSearch: An Agentic Deep Searching Workflow for Graph RAG* — [arXiv 2509.22009](https://arxiv.org/abs/2509.22009) | grafo + agente | ⏳ |

## 11–14 · 16–17 — Prompt, raciocínio e otimização

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| P1 ⭐ | **Chain-of-Thought Prompting Elicits Reasoning in LLMs** — [arXiv 2201.11903](https://arxiv.org/abs/2201.11903) | a família *thought generation*. **Condição:** o efeito *"emerge naturally in **sufficiently large** language models"* — 540B, **oito** exemplares, GSM8K. Em modelo pequeno, não se reproduz | ✓ |
| P2 ⭐ | **Self-Consistency Improves Chain of Thought Reasoning** — [arXiv 2203.11171](https://arxiv.org/abs/2203.11171) | amostrar caminhos diversos e *"marginalizing out"* — a família *ensembling*. Ganhos: GSM8K **+17,9%**, SVAMP **+11,0%**, AQuA **+12,2%** | ✓ |
| P3 ⭐ | **ReAct: Synergizing Reasoning and Acting** — [arXiv 2210.03629](https://arxiv.org/abs/2210.03629) | raciocínio e ação *"in an interleaved manner"*, com as ações servindo para *"interface with external sources, such as knowledge bases"* — a ponte cap. 12 → cap. 18 | ✓ |
| P4 ⭐ | **DSPy: Compiling Declarative LM Calls into Self-Improving Pipelines** — [arXiv 2310.03714](https://arxiv.org/abs/2310.03714) | prompt como artefato **compilado**: *"a compiler that will optimize any DSPy pipeline to maximize a given metric"*, contra os *"hard-coded prompt templates… discovered via trial and error"* | ✓ |
| P5 | **MIPROv2** — *Optimizing Instructions and Demonstrations for Multi-Stage LM Programs* — [arXiv 2406.11695](https://arxiv.org/abs/2406.11695) | instruções **e** exemplos conjuntamente, *"without access to module-level labels or gradients"*, com modelo surrogate sobre mini-lotes | ✓ |
| P6 | **GEPA: Reflective Prompt Evolution Can Outperform RL** — [arXiv 2507.19457](https://arxiv.org/abs/2507.19457) | reflexão em linguagem natural sobre **trajetórias** (*"reasoning, tool calls, and tool outputs"*) e combinação pela **fronteira de Pareto** | ✓ |
| P7 | *TextGrad: Automatic "Differentiation" via Text* — [arXiv 2406.07496](https://arxiv.org/abs/2406.07496) | prompt como variável otimizável | ⏳ |
| P8 | *Promptomatix* — [arXiv 2507.14241](https://arxiv.org/abs/2507.14241) | redução do setup manual | ⏳ |
| P9 | *Automatic Prompt Optimization for KG Construction* — [arXiv 2506.19773](https://arxiv.org/abs/2506.19773) | ganho dependente de tarefa | ⏳ |
| P10 | *A comparative evaluation of CoT-based prompt engineering for medical QA* — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0010482525009655) | o ranking muda com domínio e modelo | ⏳ |

> **Alerta do Princípio I, mantido:** os números comparativos entre otimizadores vêm de avaliações dos próprios proponentes. Nenhum entra no corpo sem modelo e orçamento declarados ao lado.

## 18 — RAG Agêntico

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| A1 ⭐ | **Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection** — [arXiv 2310.11511](https://arxiv.org/abs/2310.11511) | *"trains a single arbitrary LM that adaptively retrieves passages on-demand"* usando **reflection tokens**. Confirma a tese do capítulo: o julgamento fica **dentro** do modelo — e por isso exige **treino**, não só prompt | ✓ |
| A2 ⭐ | **CRAG: Corrective Retrieval Augmented Generation** — [arXiv 2401.15884](https://arxiv.org/abs/2401.15884) | *"a **lightweight retrieval evaluator**… returning a **confidence degree** based on which different knowledge retrieval actions can be triggered"*, com busca web como extensão. Julgamento **fora** do modelo — auditável, e *"plug-and-play"* | ✓ |
| A3 ⭐ | **FLARE** — *Active Retrieval Augmented Generation* — [arXiv 2305.06983](https://arxiv.org/abs/2305.06983) | recupera **durante** a geração: *"iteratively uses a prediction of the upcoming sentence… to retrieve relevant documents to regenerate the sentence **if it contains low-confidence tokens**"* | ✓ |
| A4 ⭐ | **Adaptive-RAG** — [arXiv 2403.14403](https://arxiv.org/abs/2403.14403) | classificador (um LM menor) prevê a complexidade e roteia entre *"the iterative and single-step retrieval-augmented LLMs, **as well as the no-retrieval methods**"* — os três graus do capítulo, verbatim | ✓ |

## 19 — RAG Conversacional

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| M1 | **MemGPT: Towards LLMs as Operating Systems** — [arXiv 2310.08560](https://arxiv.org/abs/2310.08560) | *"virtual context management"* inspirado em **hierarquia de memória de sistema operacional**, com movimentação entre níveis e interrupções | ✓ |
| M2 | *ES-Mem: Event Segmentation-Based Memory* — [arXiv 2601.07582](https://arxiv.org/abs/2601.07582) | segmentar por evento | ⏳ |
| M3 | *MemR³: Memory Retrieval via Reflective Reasoning* — [arXiv 2512.20237](https://arxiv.org/abs/2512.20237) | recuperação reflexiva de memória | ⏳ |
| M4 | *MemSyco-Bench: Benchmarking Sycophancy in Agent Memory* — [arXiv 2607.01071](https://arxiv.org/abs/2607.01071) | bajulação acumulada | ⏳ |
| M5 | *Nautilus Compass: Black-box Persona Drift Detection* — [arXiv 2605.09863](https://arxiv.org/abs/2605.09863) | deriva de persona (caps. 14, 19) | ⏳ |

## 21 — Avaliação e Observabilidade

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| E1 ⭐ | **Ragas: Automated Evaluation of RAG** — [arXiv 2309.15217](https://arxiv.org/abs/2309.15217) · EACL 2024 | avaliação **reference-free**, *"without having to rely on ground truth human annotations"*, sobre **três** aspectos: *faithfulness*, *answer relevance*, *context relevance*. **Ver correção C2** — o par precision/recall é da biblioteca | ✓ |
| E2 | BEIR e MTEB | ver B1 e B2 | ✓ |
| E3 | *FAB-Bench: A Framework for Adaptive RAG Benchmarking **in Semiconductor Manufacturing*** — [arXiv 2605.26476](https://arxiv.org/abs/2605.26476) | benchmark geral não transfere para domínio. **O domínio faz parte da citação** — é um benchmark de um setor, não geral | ⏳ |

## 22 — Segurança do Corpus e da Recuperação

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| X1 | [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | *prompt injection* como **LLM01**. Confirmado por fonte revisada independente, que o repete sem ressalva: *"Prompt injection is listed as the **number-one vulnerability class** in the OWASP Top 10 for LLM Applications"* (X2) | ✓ |
| X2 | *Are AI-assisted Development Tools Immune to Prompt Injection?* — [arXiv 2603.21642](https://arxiv.org/abs/2603.21642) | **primeira análise empírica** de *tool poisoning* em **sete clientes MCP reais**, nomeados. Mesmo vetor deste livro: conteúdo lido virando instrução obedecida | ✓ |
| X3 | *Multimodal Prompt Injection Attacks* — [arXiv 2509.05883](https://arxiv.org/abs/2509.05883) | **oito modelos comerciais** testados *"without supplementary sanitization, relying solely on its built-in safeguards"* — fraquezas exploráveis em todos. É a medição da linha de base sem camada própria | ✓ |
| X4 | *Know Thy Enemy* (InstruCoT) — [arXiv 2601.04666](https://arxiv.org/abs/2601.04666) | *fine-tuning* com CoT em nível de instrução. As duas dificuldades que ele nomeia explicam por que nenhuma defesa fecha: vetores **diversos**, e instruções injetadas que *"lack clear semantic boundaries from the surrounding context"* | ✓ |

## 23 — Custo, Latência e Cache

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| Z1 | *SmoothAgent: Efficient Long-Horizon LLM-Based Agent Serving* — [arXiv 2607.00151](https://arxiv.org/abs/2607.00151) | eficiência em horizonte longo | ⏳ |
| Z2 | Documentação de *prompt caching* dos provedores | cache por prefixo; invalidadores | ⏳ |

---

## Fontes da indústria (coleções e guias)

Não recebem ✓/⏳ — são recursos consultáveis, verificados apenas quanto à existência e ao que descrevem:

- [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/prompt-engineering-guide) — guia de referência da comunidade
- [Meirtz/Awesome-Context-Engineering](https://github.com/Meirtz/Awesome-Context-Engineering) — coleção associada ao survey S2
- [asinghcsu/AgenticRAG-Survey](https://github.com/asinghcsu/AgenticRAG-Survey) — companion do survey S3
- [gepa-ai/gepa](https://github.com/gepa-ai/gepa) — implementação de referência do P6
- [promptfoo — OWASP LLM Top 10](https://www.promptfoo.dev/docs/red-team/owasp-llm-top-10/) — red teaming mapeado à classificação
- Tópico [`context-engineering`](https://github.com/topics/context-engineering) no GitHub

**Guias de praticante sobre RAG em produção** (consultados em 2026-08-04; [análise crítica no panorama](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md#6-adendo-2026-08-04--guias-de-praticante-sobre-rag-em-produção)):

- [RAG Architecture in 2026](https://futureagi.com/blog/rag-architecture-llm-2025/) (Future AGI)
- [Building Production RAG](https://www.premai.io/blog/building-production-rag-architecture-chunking-evaluation-monitoring-2026-guide/) (Prem AI)
- [12 Advanced RAG Techniques](https://atlan.com/know/advanced-rag-techniques/) (Atlan)

> **Estes três são fonte secundária** e **nenhum número deles entra no corpo do livro**. O papel deles foi localizar técnicas nomeadas — e a rodada 2 mostra que o papel foi cumprido: **as dez técnicas que entraram por essa porta chegaram todas ao paper original, e nenhuma se revelou inexistente.** O que se revelou distorcido foi um **número** (a correção C3), não uma técnica. É a distinção que o Princípio I faz.

O mapeamento completo do ecossistema por problema está no [Apêndice — O ecossistema](apendice-ecossistema.md).
