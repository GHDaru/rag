# Bibliografia

> Fontes científicas e da indústria, por capítulo, com **status de validação**.
>
> Edição 0.2 · captura em 2026-08.

## Como ler o status (Princípio I da constituição)

| Status | Significa |
|---|---|
| ✓ | **Validada** — a referência foi localizada, lida no essencial, e a afirmação que o livro faz sobre ela foi conferida contra o texto original. Pode ser citada no corpo de um capítulo. |
| ⏳ | **A validar** — a referência foi localizada em levantamento (ver [panorama da comunidade](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md)), mas **não** foi lida na íntegra. Aparece nos capítulos marcada como `[a validar]`. |
| ✗ | **Rejeitada** — não sustenta a afirmação, ou a fonte não resistiu à conferência. Fica registrada com o motivo, porque saber o que **não** vale é resultado. |

> **Correção registrada (edição 0.2).** A survey **S0** (Gao et al., 2312.10997) é a referência mais citada de RAG e **não constava** do levantamento inicial — falha do panorama da edição 0.1, que trouxe a revisão sistemática e a de RAG agêntico e passou batido pela fundacional. Ela é agora a âncora dos caps. 01–03. Registrar a omissão é mais útil que corrigi-la em silêncio.

**Estado da edição 0.2: nenhuma referência tem status ✓.** Isto é deliberado e é a consequência honesta do escopo desta versão: o levantamento localizou as fontes e desenhou o mapa; a **validação é a rodada 2** do [ROADMAP](https://github.com/GHDaru/rag/blob/main/ROADMAP.md), conduzida pela skill `academic-research` (localizar → validar → registrar → integrar).

Enquanto isso, **nenhuma afirmação numérica de fonte ⏳ aparece no corpo dos capítulos sem a marcação e sem a condição experimental ao lado.**

---

## Surveys estruturantes

| Ref. | Fonte | Usada em | Status |
|---|---|---|:---:|
| **S0** | **Retrieval-Augmented Generation for Large Language Models: A Survey** — [arXiv 2312.10997](https://arxiv.org/abs/2312.10997) (Gao et al.) | **caps. 01, 02, 03** e todo o livro | ⏳ |
| S1 | *The Prompt Report: A Systematic Survey of Prompting Techniques* — [arXiv 2406.06608](https://arxiv.org/abs/2406.06608) | caps. 01, 02, 03 | ⏳ |
| S2 | *A Survey of Context Engineering for Large Language Models* — [arXiv 2507.13334](https://arxiv.org/abs/2507.13334) | caps. 01, 04, 05, 08, 09, 12, 13, 14 | ⏳ |
| S3 | *Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG* — [arXiv 2501.09136](https://arxiv.org/abs/2501.09136) | cap. 18 | ⏳ |
| S4 | *Exploring Prompt Engineering: A Systematic Review with SWOT Analysis* — [arXiv 2410.12843](https://arxiv.org/abs/2410.12843) | cap. 12 | ⏳ |
| S5 | *A Systematic Review of Key RAG Systems* — [arXiv 2507.18910](https://arxiv.org/abs/2507.18910) | caps. 06, 09 | ⏳ |
| S5b | *Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks* — [arXiv 2407.21059](https://arxiv.org/html/2407.21059v1) | caps. 02, 03 | ⏳ |
| S5c | *Reasoning RAG via System 1 or System 2* — [arXiv 2506.10408](https://arxiv.org/abs/2506.10408) | caps. 02, 03, 18 | ⏳ |
| S6 | *Context Engineering 2.0: The Context of Context Engineering* — [arXiv 2510.26493](https://arxiv.org/abs/2510.26493) | cap. 24 | ⏳ |

## Por capítulo

### 01 — Fundamentos · 08 — A Janela como Orçamento

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| F1 | *Lost in the Middle: How Language Models Use Long Contexts* — [arXiv 2307.03172](https://arxiv.org/abs/2307.03172) | degradação posicional; "o que importa vai para as pontas" | ⏳ |
| F2 | *U-NIAH: Unified RAG and LLM Evaluation for Long Context Needle-In-A-Haystack* — [arXiv 2503.00353](https://arxiv.org/abs/2503.00353) | comparação dos dois regimes no mesmo protocolo | ⏳ |

> **Lacuna conhecida**: a afirmação do cap. 20 de que a degradação é dirigida pela **similaridade entre alvo e distratores** (e não pelo comprimento) é hoje a mais frágil do livro em termos de citação. É prioridade 1 da rodada 2.

### 03 — Técnicas de Raciocínio

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| R1 | Chain-of-Thought (proposta original) | família *thought generation* | ⏳ |
| R2 | Self-Consistency | família *ensembling* | ⏳ |
| R3 | ReAct | a ponte prompt → RAG agêntico (caps. 12, 09, 14) | ⏳ |
| R4 | *A comparative evaluation of CoT-based prompt engineering techniques for medical QA* — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0010482525009655) | o ranking de técnicas muda com domínio e modelo | ⏳ |

### 06 — Otimização Automática de Prompts

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| O1 | GEPA — otimizador reflexivo genético-Pareto · [gepa-ai/gepa](https://github.com/gepa-ai/gepa) | família "reflexão sobre traços" | ⏳ |
| O2 | MIPROv2 | família "busca por instrução" | ⏳ |
| O3 | TextGrad | prompt como variável otimizável | ⏳ |
| O4 | *Promptomatix* — [arXiv 2507.14241](https://arxiv.org/abs/2507.14241) | redução do setup manual | ⏳ |
| O5 | *Automatic Prompt Optimization for KG Construction* — [arXiv 2506.19773](https://arxiv.org/abs/2506.19773) | ganho dependente de tarefa | ⏳ |

> **Alerta do Princípio I**: todos os números comparativos desta seção vêm de avaliações dos próprios proponentes. A rodada 2 deve registrar, para cada um, **quais modelos e qual orçamento** foram usados — sem isso o número não entra no corpo.

### 09 — Recuperação · 10 — RAG Avançado

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| C1 | *Reconstructing Context: Evaluating Advanced Chunking Strategies for RAG* — [arXiv 2504.19754](https://arxiv.org/abs/2504.19754) | estratégias de chunking avaliadas | ⏳ |
| C2 | *Adaptive Chunking: Optimizing Chunking-Method Selection for RAG* — [arXiv 2603.25333](https://arxiv.org/abs/2603.25333) | seleção por documento, não fixa | ⏳ |
| C3 | *Cross-Document Topic-Aligned Chunking for RAG* — [arXiv 2601.05265](https://arxiv.org/abs/2601.05265) | tópicos que atravessam documentos | ⏳ |
| C4 | Contextual Retrieval (Anthropic) | prefixar contexto antes de embeddar | ⏳ |
| C5 | Late Chunking (Jina AI) | cortar depois do transformer | ⏳ |
| C6 | *Hybrid Retrieval and Query Rewriting for Multi-Turn RAG* — [arXiv 2606.28352](https://arxiv.org/abs/2606.28352) | reescrita de consulta em conversa | ⏳ |
| C7 | Surveys de GraphRAG e RAG baseado em grafo | quando grafo paga | ⏳ |
| C8 | **RAPTOR** — árvore de resumos recursivos por agrupamento | sumarização hierárquica; pergunta global | ⏳ |
| C9 | **HyDE** — documento hipotético como consulta | lado da pergunta | ⏳ |
| C10 | **Step-back prompting** — generalizar antes de recuperar | lado da pergunta | ⏳ |

### 11 — RAG Agêntico

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| A1 | S3 (survey de RAG agêntico) | os quatro padrões; o espectro | ⏳ |
| A2 | *GraphSearch: An Agentic Deep Searching Workflow for Graph RAG* — [arXiv 2509.22009](https://arxiv.org/abs/2509.22009) | convergência grafo + agente | ⏳ |
| A3 | **Self-RAG** — reflexão treinada no modelo (marcadores de recuperação e sustentação) | as materializações nomeadas | ⏳ |
| A4 | **CRAG** (*Corrective RAG*) — avaliador leve + ação corretiva | idem | ⏳ |
| A5 | **FLARE** — recuperação disparada por incerteza durante a geração | idem | ⏳ |
| A6 | **Adaptive RAG** — roteamento por complexidade da pergunta | idem | ⏳ |

### 12 — Memória e Estado

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| M1 | MemGPT / Letta | paginação autogerida | ⏳ |
| M2 | *ES-Mem: Event Segmentation-Based Memory for Long-Term Dialogue Agents* — [arXiv 2601.07582](https://arxiv.org/abs/2601.07582) | segmentar por evento (caps. 19, 14) | ⏳ |
| M3 | *MemR³: Memory Retrieval via Reflective Reasoning* — [arXiv 2512.20237](https://arxiv.org/abs/2512.20237) | recuperação reflexiva de memória | ⏳ |
| M4 | *MemGuard: Preventing Memory Contamination* — [arXiv 2605.28009](https://arxiv.org/abs/2605.28009) | contaminação (caps. 19, 22) | ⏳ |
| M5 | *MemSyco-Bench: Benchmarking Sycophancy in Agent Memory* — [arXiv 2607.01071](https://arxiv.org/abs/2607.01071) | bajulação acumulada | ⏳ |
| M6 | *Nautilus Compass: Black-box Persona Drift Detection* — [arXiv 2605.09863](https://arxiv.org/abs/2605.09863) | deriva de persona (caps. 14, 18) | ⏳ |

### 15 — Avaliação de Sistemas

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| E1 | BEIR | recuperação zero-shot | ⏳ |
| E2 | MTEB | modelos de embedding | ⏳ |
| E3 | RAGAS | as quatro métricas | ⏳ |
| E4 | *FAB-Bench: Adaptive RAG Benchmarking* — [arXiv 2605.26476](https://arxiv.org/abs/2605.26476) | benchmark geral não transfere para domínio | ⏳ |

### 16 — Segurança do Contexto

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| G1 | [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | LLM01; defesa em profundidade | ⏳ |
| G2 | *Are AI-assisted Development Tools Immune to Prompt Injection?* — [arXiv 2603.21642](https://arxiv.org/abs/2603.21642) | injeção via ferramenta (caps. 15, 17) | ⏳ |
| G3 | *Multimodal Prompt Injection Attacks* — [arXiv 2509.05883](https://arxiv.org/abs/2509.05883) | filtrar texto não basta | ⏳ |
| G4 | *Know Thy Enemy: Securing LLMs Against Prompt Injection…* — [arXiv 2601.04666](https://arxiv.org/abs/2601.04666) | defesas por treinamento | ⏳ |

### 17 — Custo, Latência e Cache

| Ref. | Fonte | Sustenta | Status |
|---|---|---|:---:|
| P1 | *SmoothAgent: Efficient Long-Horizon LLM-Based Agent Serving* — [arXiv 2607.00151](https://arxiv.org/abs/2607.00151) | eficiência de agentes de horizonte longo | ⏳ |
| P2 | Documentação de *prompt caching* dos provedores | cache por prefixo; invalidadores | ⏳ |

---

## Fontes da indústria (coleções e guias)

Não recebem status ✓/⏳ — são recursos consultáveis, verificados apenas quanto à existência e ao que descrevem:

- [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/prompt-engineering-guide) — guia de referência da comunidade (prompt + contexto + RAG + agentes)
- [Meirtz/Awesome-Context-Engineering](https://github.com/Meirtz/Awesome-Context-Engineering) — coleção associada ao survey S2
- [asinghcsu/AgenticRAG-Survey](https://github.com/asinghcsu/AgenticRAG-Survey) — companion do survey S3
- [promptslab/Awesome-Prompt-Engineering](https://github.com/promptslab/awesome-prompt-engineering) · [natnew/Awesome-Prompt-Engineering](https://github.com/natnew/Awesome-Prompt-Engineering)
- [promptfoo — OWASP LLM Top 10](https://www.promptfoo.dev/docs/red-team/owasp-llm-top-10/) — red teaming mapeado à classificação
- Tópico [`context-engineering`](https://github.com/topics/context-engineering) no GitHub

**Guias de praticante sobre RAG em produção** (consultados em 2026-08-04; ver a [análise crítica no panorama](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md#6-adendo-2026-08-04--guias-de-praticante-sobre-rag-em-produção)):

- [RAG Architecture in 2026](https://futureagi.com/blog/rag-architecture-llm-2025/) (Future AGI) — arquitetura em seis camadas e três padrões de orquestração
- [Building Production RAG](https://www.premai.io/blog/building-production-rag-architecture-chunking-evaluation-monitoring-2026-guide/) (Prem AI) — chunking, avaliação e **observabilidade com limiares por camada**
- [12 Advanced RAG Techniques](https://atlan.com/know/advanced-rag-techniques/) (Atlan) — as técnicas por estágio do pipeline, e o argumento de **governança do corpus**

> **Estes três são fonte secundária** (praticante, não proponente) e **nenhum número deles entra no corpo do livro**. Servem para localizar técnicas nomeadas — foi assim que RAPTOR, Self-RAG, CRAG, FLARE, Adaptive RAG e step-back entraram na fila de validação. O caso de deriva numérica documentado no panorama (§6) explica por quê.

O mapeamento completo do ecossistema por problema está no [Apêndice — O ecossistema](apendice-ecossistema.md).
