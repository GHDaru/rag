# Apêndice — O ecossistema

> Frameworks, bibliotecas e coleções **organizados pelo problema que resolvem** — não por popularidade, e nunca como recomendação (Princípio VI: nenhum framework é "o jeito certo").
>
> Edição 1.0 · captura em 2026-08. Origem: [panorama da comunidade](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md).
>
> **Como ler:** esta página é *reference* (Diátaxis) — consulta, não leitura linear. A avaliação comparada por dimensão, com evidência, é a **rodada 4** do [ROADMAP](https://github.com/GHDaru/rag/blob/main/ROADMAP.md); até lá, o que está aqui é mapa, não veredito.

## Otimizar prompt automaticamente (cap. 16)

| Ferramenta | Abordagem | Nota |
|---|---|---|
| **DSPy** | declara assinaturas e módulos; otimizadores escrevem o texto | o framework que impôs o modelo mental de "compilar prompt" |
| **BootstrapFewShot** (DSPy) | busca quais demonstrações incluir | o mais barato; primeiro recurso |
| **COPRO** (DSPy) | busca por instrução | |
| **MIPROv2** (DSPy) | instruções + exemplos, via otimização bayesiana | para sistemas compostos |
| **GEPA** · [gepa-ai/gepa](https://github.com/gepa-ai/gepa) | evolução por reflexão sobre traços de execução | devolve explicação legível junto do artefato |
| **TextGrad** | prompt como variável textual otimizável | mais simples de montar; melhor com dificuldade uniforme |
| **Promptomatix** · [arXiv 2507.14241](https://arxiv.org/abs/2507.14241) | reduz o setup manual exigido | |

## Recuperar (caps. 05–10)

**Busca esparsa** — BM25 e variantes. Acha termo literal, código, identificador. É a linha de base honesta e o remédio para "o RAG não encontra o óbvio".

**Busca densa** — modelos de embedding + armazenamento vetorial. Acha paráfrase e sinônimo. Falha em termo raro fora do domínio de treino.

**Híbrido** — fusão de rankings dos dois. O upgrade de melhor relação benefício/esforço do livro, porque os erros das duas famílias são complementares.

**Reranking** — modelos *cross-encoder* sobre os primeiros N candidatos. Caro por documento, alto retorno marginal.

**Técnicas de indexação avançada**:

| Técnica | Custo onde | Resolve |
|---|---|---|
| **Contextual Retrieval** (Anthropic) | indexação: 1 chamada de LLM por chunk | chunk sem contexto |
| **Late Chunking** (Jina AI) | indexação: só o modelo de embedding | chunk sem contexto, muito mais barato |
| **HyDE** | consulta: 1 chamada por pergunta | pergunta que não se parece com a resposta |
| **Reescrita de consulta** | consulta | vocabulário do domínio; referência entre turnos |
| **GraphRAG** e família | indexação pesada + consulta | multi-hop e perguntas globais |

## Lembrar (cap. 19)

| Sistema | Arquitetura | Escolha quando |
|---|---|---|
| **Mem0** | extrai fatos salientes e guarda como memórias compactas | personalização; memória "plug-and-play" |
| **Zep** | grafo de conhecimento **temporal** sobre recuperação densa | os fatos mudam de valor de verdade com o tempo |
| **Letta** (ex-MemGPT) | o LLM pagina a própria memória (*main* / *recall* / *archival*) | agentes de execução longa |

> Ressalva registrada pelos praticantes: a paginação autogerida adiciona complexidade e latência que nem sempre se pagam em benchmarks padrão. E os números publicados de memória (LoCoMo, LongMemEval) são majoritariamente auto-reportados — leia com o Princípio I na mão.

## Avaliar (caps. 17, 21)

| Ferramenta | Papel |
|---|---|
| **RAGAS** | fixou o vocabulário de fato. Paper (EACL 2024): *faithfulness*, *answer relevance*, *context relevance* — reference-free. Biblioteca: desdobra o terceiro em *context precision* / *context recall*; gera conjunto de teste a partir do corpus |
| **DeepEval** | as mesmas ideias com foco em execução em CI/CD |
| **TruLens** | instrumentação e observabilidade de execução |
| **BEIR** | recuperação zero-shot em domínios variados (mede só o estágio de recuperação) |
| **MTEB** | avaliação ampla de modelos de embedding |
| **promptfoo** | avaliação + red teaming, com casos mapeados ao OWASP LLM Top 10 |

A leitura de 2026: **RAGAS fornece o arcabouço conceitual; DeepEval, a execução em pipeline.** São complementares, não concorrentes.

## Proteger (cap. 22)

- **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** — a classificação de referência. *Prompt injection* é LLM01 em todas as edições publicadas.
- **Ferramentas de red teaming** — teste adversarial em pipeline, com cobertura mapeada à classificação. A conexão importante: **teste adversarial é eval**, e roda no mesmo lugar (cap. 17).

## Fora do escopo deste livro

- **MCP (Model Context Protocol)** e os frameworks de orquestração de agente aparecem em toda lista de "ferramentas de RAG", mas resolvem **integração**, não recuperação. O tratamento deles é do livro irmão, *[Engenharia de Harness](https://ghdaru.github.io/harness_engineering/)* — aqui eles entram só quando a recuperação vira ferramenta na mão do modelo (cap. 18).

## As coleções vivas (por onde continuar)

| Coleção | O que reúne |
|---|---|
| [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/prompt-engineering-guide) | prompt, contexto, RAG e agentes no mesmo índice — o sinal de que o par é uma disciplina só |
| [Meirtz/Awesome-Context-Engineering](https://github.com/Meirtz/Awesome-Context-Engineering) | centenas de papers e implementações do lado do contexto — a fronteira com o livro irmão |
| [asinghcsu/AgenticRAG-Survey](https://github.com/asinghcsu/AgenticRAG-Survey) | o companion do survey de RAG agêntico |
| [promptslab](https://github.com/promptslab/awesome-prompt-engineering) · [natnew](https://github.com/natnew/Awesome-Prompt-Engineering) | variantes e casos de uso por domínio |
| [tópico `context-engineering`](https://github.com/topics/context-engineering) | o termômetro do que a comunidade publica agora |

---

## O que falta neste apêndice

Registrado por honestidade (Princípio I), e é trabalho das próximas rodadas:

- **Nenhuma avaliação comparada.** Não há nota, ranking nem "melhor para". Isso exige metodologia e evidência — é a rodada 4.
- **Ausências conhecidas**: bancos vetoriais e motores de busca (deliberadamente fora — o livro trata de técnica, não de infraestrutura de armazenamento); frameworks de orquestração de agentes (adjacentes, entram se um capítulo exigir); ferramentas de observabilidade de LLM (entram junto com o cap. 21 aprofundado).
- **Viés declarado**: levantamento em inglês, por busca aberta, sem bases pagas. Projetos fora do eixo GitHub/arXiv estão sub-representados.
