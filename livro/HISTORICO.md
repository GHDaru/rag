# Histórico e Registro de Expiração

> O livro é vivo (Princípio IV): toda edição é datada, registrada e **atribuída** — inclusive quanto ao modelo de IA usado, porque saídas de LLM não são determinísticas e a rastreabilidade é parte do rigor.
>
> Esta página tem duas metades: o **histórico de edições** (o que mudou, quando, por quem) e o **registro de expiração** (o placar das apostas do cap. 24 — previsões feitas com data, para serem cobradas depois).

## Histórico de edições

### Edição 0.4 — 2026-08-09 · Os 22 Apêndices A, e a rodada 2 fechada

**O que é.** O item que faltava para concluir a rodada 2: o **tratamento por implementação**. O Princípio II exige que a fonte-base seja a técnica reprodutível — *paper* **mais** implementação pública — e o corpo dos capítulos recebia só a primeira metade. Os apêndices eram um "enfileirado: X · Y · Z".

**O que mudou:** os **22 Apêndices A** passaram de fila a conteúdo. Cada um é uma tabela com a implementação de referência, URL, e — a parte que dá valor — **a pegadinha**: o que a documentação não diz e o livro aprendeu a perguntar. Alguns exemplos do que só aparece aí:

- **Self-RAG exige treino.** O método treina o modelo a emitir *reflection tokens*; se você não vai treinar nem usar um modelo já treinado assim, o padrão simplesmente não está disponível — enquanto o CRAG é *"plug-and-play"*. É a diferença que decide qual dos dois você consegue adotar, e ela não está no corpo do capítulo.
- **O cache semântico precisa da permissão na chave.** Sem isso ele serve a resposta de um usuário a outro — o incidente do cap. 04 entrando por outra porta.
- **O índice vetorial aproximado troca recall por latência.** Recall que cai sem explicação costuma ser parâmetro de busca do índice, não o modelo de embedding.
- **O *late chunking* degrada em silêncio** quando o documento excede o embedder de contexto longo.
- **Um dicionário de três colunas** (cap. 02) mostrando que LangChain, LlamaIndex e Haystack convergem na mesma anatomia e divergem só no vocabulário — o argumento de aprender componentes em vez de framework, demonstrado em tabela.

**Verificação dos links.** Os 32 repositórios citados foram conferidos **um a um** contra o repositório real, com o README lido para confirmar que é o projeto certo. O acesso direto ao GitHub está bloqueado nesta sessão para repositórios fora do escopo; a conferência foi feita por `raw.githubusercontent`, que resolve. Uma correção veio daí: `anthropics/anthropic-cookbook` foi renomeado para *Claude Cookbooks*.

**Rodada 2 concluída.** Os três critérios: ≥60% em ✓ (**76%**), nenhum número sem condição experimental, e **22 de 22 Apêndices A preenchidos**. O que sobrou — 13 referências de menor peso e a evidência do cap. 04 — migra para a rodada 4, onde vira **medição própria** em vez de busca bibliográfica.

**Atribuição:** direção editorial — Gilsiley Henrique Darú. Redação e verificação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-09.

### Edição 0.3 — 2026-08-04 · Rodada 2: o livro passa a ser citável

**O que é.** A rodada de **evidência**. Até aqui o livro tinha um mapa de fontes e nenhuma delas conferida — 55 referências ⏳, zero ✓. Esta edição leva **42 delas (76%) a ✓**, acima do critério de 60% da rodada.

**O que foi feito:**

- **Os 49 identificadores arXiv do repositório foram resolvidos contra o arXiv real**, com um ID falso de controle para provar que o teste discrimina. **Nenhum inventado, nenhum título divergente.** A citação alucinada — a falha mais corrosiva possível num livro assim — está descartada como classe.
- **42 referências passaram a ✓**: texto lido, afirmação do livro conferida contra o original.
- **As ~20 técnicas nomeadas que estavam sem URL ganharam fonte primária.** RAPTOR, Self-RAG, CRAG, FLARE, Adaptive RAG, HyDE, step-back, late chunking, proposição e GraphRAG entraram no livro pela porta dos guias de praticante, e a rodada 2 confirmou que **todas chegam ao paper que as propôs**. O que se revelou distorcido foi um número, não uma técnica.
- **Condição experimental ao lado de cada número validado** — o modelo de 540B do Chain-of-Thought, o GPT-4 acoplado ao RAPTOR, o cenário zero-shot sem rótulo do HyDE, o custo por milhão de tokens do *contextual retrieval*.

**As quatro correções — o resultado mais valioso da rodada:**

1. **✗ *Lost in the Middle* não sustentava a afirmação do cap. 20.** O livro dizia que a degradação em contexto longo "não é linear com o comprimento, é dirigida pela similaridade entre alvo e distratores", e citava aquele paper. Ele estabelece degradação **posicional** e não trata de distratores. Pior: a fonte que **de fato** mede distratores (relatório *Context Rot*, 18 modelos) contradiz a outra metade — isolando a variável, **o comprimento degrada sozinho**, mesmo em tarefa trivial. O certo é "é o comprimento, e distratores próximos tornam a queda mais íngreme". Era a afirmação que o próprio livro marcava como a mais frágil; estava frágil pelos dois lados.
2. **✗ As quatro métricas não são todas do paper do RAGAS.** O original propõe **três** — *faithfulness*, *answer relevance*, *context relevance*. O par *context precision* / *context recall* é da **biblioteca**, que desdobrou o terceiro. O livro construiu um capítulo inteiro sobre o quarteto atribuindo-o à fonte errada.
3. **⚠ O `67%` do *contextual retrieval* ganhou a curva inteira**: taxa de falha no top-20 caindo de 5,7% para 3,7% (técnica sozinha), 2,9% (com BM25) e 1,9% (com reranker). O número que circula é o da pilha completa.

**Nota de método que vale registrar.** A primeira consulta automática ao PDF do RAGAS devolveu uma citação **inventada** — "We propose four metrics" — que teria confirmado o erro do livro em vez de revelá-lo. Só apareceu porque o texto foi extraído e lido diretamente. **Resumo automático de fonte não é validação.** É exatamente para isso que o status ✓ existe.

**O que a validação também **acrescentou** ao livro, além de corrigir:** cinco **métricas intrínsecas de chunking** que permitem avaliar o corte sem pipeline inteiro (cap. 05); a *heterogeneous memory contamination* e a cura por papel funcional na escrita (caps. 19, 22); o corpus sintético ficcional do U-NIAH como método para separar recuperação de memorização (cap. 20); e a precisão de que *zero-shot* e *few-shot* são irmãos sob **In-Context Learning**, não pares dos outros quatro ramos (cap. 12).

**Estado da evidência:** **42 ✓ · 13 ⏳ · 3 ✗**. As 13 restantes são de menor peso estrutural — nenhuma sustenta sozinha uma tese de capítulo. **Fica aberto** o preenchimento dos Apêndices A, que é o item restante do critério de conclusão da rodada.

**Atribuição:** direção editorial — Gilsiley Henrique Darú. Validação, correções e redação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-04.

### Adendo 0.2.1 — 2026-08-04 · Geração de metadado, e a dívida da renumeração

**A pergunta do editor:** *"na ingestão, acredito que teremos coisas do tipo geração de metadados, etc, ou não é isto?"* — e estava certo: o cap. 04 listava "enriquecimento" numa linha de tabela e depois só tratava do metadado **que já existe** (origem, data, permissão). A camada onde o metadado é **criado** é justamente a parte cara e mais rendosa da ingestão, e faltava.

**O que mudou:**

- **Cap. 04 ganha duas seções.** *Geração de metadado* — as três procedências (**herdado**, **derivado**, **gerado**), e o que vale gerar em ordem de retorno: resumo contextual (que é o *contextual retrieval* do cap. 09 sob outro nome), **perguntas hipotéticas** (HyDE invertido e movido para a indexação, pago uma vez em vez de em toda consulta), vigência extraída da prosa, classificação, entidades. E *o metadado gerado errado é pior que o ausente* — a falha silenciosa em que o documento certo some **antes** da busca, com o log mostrando uma consulta normal; daí a regra de que metadado gerado **impulsiona, nunca filtra de forma dura**.
- **A dívida da renumeração 0.2, paga.** A reestruturação renumerou os capítulos mas não alcançou o **aparato**: o catálogo de técnicas inteiro ainda apontava para a numeração original (busca em "09", RAPTOR em "10"), o glossário tinha o cluster de recuperação errado, e cinco capítulos citavam partes do sumário antigo ("a Parte II adiciona superfície de ataque"). Corrigido em 16 referências de capítulo e nas três páginas de aparato.
- **Catálogo reorganizado** na ordem das partes atuais, com as técnicas dos dois capítulos removidos retiradas e as da geração fundamentada (cap. 15) acrescentadas. As "sete que valem começar por aqui" viram **oito**, e agora começam pelo corpus — não pelo prompt.
- **Glossário** com os verbetes que a edição 0.2 passou a exigir: os quatro paradigmas, contrato, procedência, fusão por posição, metadado gerado, abstenção, fundamentação, atribuição por afirmação, multi-hop, pergunta global.

**Atribuição:** crítica editorial — Gilsiley Henrique Darú. Redação e correção — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-04.

### Edição 0.2 — 2026-08-04 · O livro vira *Engenharia de RAG*

**A crítica que originou a rodada**, do editor: o livro anterior (*Engenharia de Prompt e Engenharia de Contexto*) **duplicava o livro irmão**. Quatro capítulos — memória, compactação, ferramentas/MCP, segurança de contexto — eram território do *Engenharia de Harness*, e o que era genuinamente deste livro (corpus, recuperação, RAG avançado, agêntico) estava espremido no meio. A crítica estava certa.

**O que mudou:**

- **Nome e objeto.** O livro passa a ser **Engenharia de RAG** — *como se constrói um sistema em volta da recuperação da informação*. Cunhagem nossa, como "Engenharia de Harness"; a pesquisa confirmou que não existe termo consagrado (existe **RAG**, universal, e *Information Retrieval*, o campo que o absorveu — há track de RAG no TREC).
- **Constituição 3.0.0.** Princípio VIII reescrito: o objeto é o **sistema**, todo capítulo declara o **componente da arquitetura** que aprofunda, e a **fronteira com o livro irmão** é explícita — gestão de contexto de agente é de lá; aqui entra só o que decide a recuperação ou a fundamentação.
- **Três capítulos novos**, que fechavam a lacuna real: **02 — Anatomia de um Sistema de RAG** (dois caminhos, 16 componentes, os contratos), **03 — Arquiteturas de Referência** (Naive → Advanced → Modular → Agêntico, e os quatro padrões de fluxo) e **15 — Geração Fundamentada** (o "G" que faltava: grounding, citação verificável, abstenção).
- **A Parte III desdobrada** em cinco capítulos (busca, reranking, consulta, avançada, estruturada), onde antes havia dois.
- **A Parte IV mantida inteira** — os seis capítulos de engenharia de prompt ficam, agora a serviço da geração. Decisão do editor, contra a proposta inicial de condensá-los.
- **Dois capítulos removidos** (compactação; ferramentas e MCP) e devolvidos ao livro irmão; o que era de RAG neles foi absorvido pelos caps. 19 e 18.
- `contexto-zero` → **`rag-zero`**, com 17 etapas realinhadas.

**A correção de evidência que esta edição registra:** a survey de Gao et al. ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)) — **a referência mais citada de RAG** — não constava do levantamento da edição 0.1. Falha do panorama, que trouxe a revisão sistemática e a de RAG agêntico e passou batido pela fundacional. Ela agora ancora os caps. 01–03, junto de *Modular RAG* (2407.21059). Registrar a omissão é mais útil que corrigi-la em silêncio.

**Estado da evidência:** segue **nenhuma referência com status ✓**. A validação é a rodada 2.

**Atribuição:** crítica editorial, decisão de nome e de escopo — Gilsiley Henrique Darú. Pesquisa de terminologia, reestruturação e redação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-04.

### Edição 0.1 — 2026-08-04 · Fundação: o esqueleto das duas disciplinas

**O que é.** A primeira versão pública do livro. Estabelece a moldura (prompt × contexto, com RAG dentro da segunda), o sumário completo em três partes, os 19 capítulos com esqueleto e explicação de abertura, o catálogo de técnicas, o mapa do ecossistema e o glossário.

**O que foi feito:**
- **Constituição 2.0.0** — derivada da 1.2.0 do livro *Engenharia de Harness* (mesmo método pedagógico e editorial, domínio novo). Princípio II reescrito: a fonte-base deixa de ser "o código de harnesses" e passa a ser **paper + implementação pública**. Princípio VIII criado: fixa a moldura do par e o lugar do RAG.
- **Levantamento da comunidade** — [panorama](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md) cruzando academia (surveys estruturantes), repositórios públicos, frameworks e técnicas, e respondendo à pergunta que originou o projeto ("engenharia de contexto substitui RAG?" — não como substituto, como moldura).
- **Sumário em três partes** — Parte I (Engenharia de Prompt, caps. 11–17), Parte II (Engenharia de Contexto, caps. 20–14, com RAG em três capítulos), Parte III (o sistema em produção, caps. 21–23), mais abertura (00–01) e fechamento (18).
- **Aparato** — catálogo de técnicas, apêndice do ecossistema, glossário, bibliografia com status de validação, grafo do livro.
- **Motor de publicação** adaptado: PT-only, sem Radar, com o grafo remapeado para o novo domínio.

**Fora do escopo, por decisão explícita:** edição em inglês, Radar de atualização automática, benchmark quantitativo de frameworks, e a trilha prática `rag-zero` (descrita nos capítulos, implementada na rodada 3). Ver [ROADMAP](https://github.com/GHDaru/rag/blob/main/ROADMAP.md).

**Estado da evidência (honestidade obrigatória, Princípio I):** **nenhuma referência tem status ✓ nesta edição.** Todas estão marcadas ⏳ na [bibliografia](bibliografia.md) e `[a validar]` nos capítulos. Os capítulos declaram maturidade "esboço" ou "fundação" no cabeçalho. A validação é a rodada 2.

**Atribuição:** direção editorial e decisões — Gilsiley Henrique Darú. Pesquisa, estruturação e redação assistidas por **Claude (Anthropic)**, modelo Opus 5, em sessão de 2026-08-03/04. Levantamento por busca aberta na web, sem acesso a bases pagas.

### Adendo 0.1.1 — 2026-08-04 · Técnicas nomeadas e o teto do corpus

Rodada curta, disparada por três guias de praticante indicados pelo editor ([análise no panorama §6](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md#6-adendo-2026-08-04--guias-de-praticante-sobre-rag-em-produção)). Um quarto guia devolveu HTTP 403 e fica como pendência declarada.

**O que entrou:**
- **Seis técnicas nomeadas** que o esqueleto tratava de forma genérica: RAPTOR (cap. 09), Self-RAG / CRAG / FLARE / Adaptive RAG (cap. 18), step-back prompting (cap. 09), sentence-window e proposition chunking (cap. 06). Todas ⏳, na fila da rodada 2.
- **Dois padrões que a organização revelou** e que não estavam escritos: *desacoplar a unidade de busca da unidade de entrega* (cap. 06) e *as materializações de RAG agêntico diferem por onde mora o julgamento* (cap. 18).
- **Sinais de produção** (cap. 21): taxa de resultado zero, distribuição de nota do reranker, taxa de citação, p99 por camada. E o **cache semântico** com seu modo de falha (cap. 23).
- **Seção nova "O teto que ninguém mede: o corpus"** (cap. 06) — frescor, procedência, deduplicação. Declarada como a seção mais fraca da edição.

**O que NÃO entrou, e é o registro que importa:** nenhum número das três fontes. São secundárias (praticante citando proponente), e o panorama §6.2 documenta o caso de **deriva numérica** do *contextual retrieval* — o 67% da Anthropic, que é resultado de três estágios cumulativos, aparece em fonte secundária como mérito de um só. Também ficou registrado como não utilizável o "80% das falhas de RAG vêm da ingestão", que circula **sem fonte alguma**.

**Pergunta editorial aberta para o editor:** governança/ingestão do corpus merece **capítulo próprio** na Parte II, ou continua como seção do cap. 06? É hoje a única parte do pipeline que nenhuma das três partes do livro cobre.

**Atribuição:** direção editorial — Gilsiley Henrique Darú (indicação das fontes). Análise, verificação e redação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-04.

### Adendo 0.1.2 — 2026-08-04 · O corpus vira capítulo

Decisão editorial do autor sobre a pergunta deixada em aberto no adendo 0.1.1: **governança e ingestão do corpus merecem capítulo próprio.**

- **Novo [cap. 04 — Ingestão e Governança do Corpus](capitulos/04-corpus.md)**, inserido **antes** da recuperação. A ordem é o argumento: o corpus é o teto de tudo que os caps. 06–18 otimizam, e quem aprende a otimizar antes de conhecer o teto passa meses ajustando `top_k` num corpus que nunca poderia responder bem.
- **Renumeração**: os antigos caps. 04–23 passam a 10–19. O `rag-zero` ganha a etapa 8 (ingestão) e passa a 18 etapas.
- **O capítulo declara a própria fragilidade**: é o de base científica mais fraca do livro, porque a literatura de RAG trata ingestão como pré-processamento e raramente a estuda. Fica registrada a pergunta que a rodada 2 deve responder — *existe medição publicada do impacto isolado de frescor e deduplicação sobre métricas de RAG?* Se não existir, vira experimento próprio na rodada 4.

**Atribuição:** decisão editorial — Gilsiley Henrique Darú. Redação e renumeração — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-04.

---

## Registro de expiração

O placar das apostas registradas no [cap. 24](24-convergencias.md). Uma aposta só vale se puder ser julgada — por isso cada uma tem critério de verificação e prazo.

| # | Aposta | Feita em | Prazo | Critério | Veredito |
|---|---|:---:|:---:|---|:---:|
| A1 | A metade sintática da saída estruturada (cap. 13) vira funcionalidade trivial e o capítulo encolhe para uma seção do cap. 11 | 2026-08 | 2027-08 | o capítulo é fundido | ⏳ aberta |
| A2 | Orçamento explícito de contexto vira prática padrão, com painel de composição por fonte | 2026-08 | 2028-02 | ferramentas de observabilidade trazem pronto | ⏳ aberta |
| A3 | Otimização automática de prompt **não** substitui a escrita manual na maioria dos projetos, mas vira padrão em alto volume | 2026-08 | 2028-08 | adoção reportada em levantamentos | ⏳ aberta |
| A4 | Nenhuma defesa por prompt contra injeção indireta será considerada suficiente | 2026-08 | 2028-08 | recomendação vigente do OWASP | ⏳ aberta |
| A5 | Avaliação de trajetória/conversa deixa de ser lacuna e ganha ferramenta madura | 2026-08 | 2027-08 | ferramenta adotada com métricas de sessão | ⏳ aberta |
| A6 | O rótulo "engenharia de contexto" perde força e o conteúdo é absorvido por "engenharia de sistemas de IA" | 2026-08 | 2028-08 | uso do termo na literatura e em vagas | ⏳ aberta |

**Como o placar é fechado:** na revisão de cada prazo (rodada 6 e seguintes), cada aposta recebe ✅ (confirmada), ❌ (refutada) ou 🔄 (ainda indefinida, com novo prazo). **Aposta refutada não é apagada** — é o registro mais valioso desta página, porque mostra onde o livro errou e por quê.

## Três datas, sempre distintas

O livro distingue rigorosamente (Princípio IV):

- **Data do evento** — quando a coisa descrita aconteceu (o paper foi publicado, a funcionalidade foi lançada).
- **Data de captura** — quando este livro olhou para aquilo. É a data no cabeçalho de cada capítulo.
- **Data da rodada** — quando a revisão sistemática aconteceu. É a data desta página.

Confundir as três é o erro que faz um livro técnico parecer atual quando não é.
