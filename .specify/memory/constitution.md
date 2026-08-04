# Constituição — Livro de Engenharia de Prompt e Engenharia de Contexto

> A lei do projeto. Todo trabalho (edição de capítulo, catalogação de técnica, código do `contexto-zero`, pesquisa) segue estes princípios. Em conflito entre pedido pontual e constituição, a constituição prevalece — ou o conflito é explicitado antes de agir. Documentos operacionais: `livro/GUIA-EDITORIAL.md` (como escrever), `benchmark/README.md` (como avaliar uma técnica), `ROADMAP.md` (o que vem por rodada).

## Princípios centrais

### I. Evidência acima de retórica (NÃO-NEGOCIÁVEL)
Toda afirmação sobre uma técnica exige **evidência de primeira mão**: a fonte primária (paper, documentação oficial do provedor ou post de engenharia assinado), com URL verificável. Toda citação científica exige **status validado** (✓) em `livro/bibliografia.md`. Números (ganho de recall, redução de falha, custo) só entram no corpo **com a fonte da medição ao lado** e com a condição experimental declarada — "melhora a acurácia" sem número e sem benchmark é retórica, não engenharia.

### II. A fonte-base é a técnica reprodutível
O livro nasce de duas leituras que se cruzam: o **paper** (o que foi proposto e medido) e a **implementação pública** (como isso vira código que roda). Uma técnica só entra no corpo quando tem as duas — proposta e materialização consultável. Marketing de fornecedor não substitui nenhuma das duas.
- O **corpo do capítulo** recebe o **estado da arte**: a síntese, o trade-off, o "quando usar".
- O **Apêndice A** de cada capítulo recebe o tratamento por implementação/framework (com repositório, arquivo ou notebook) — é a espinha empírica e a complementação online.

### III. Método pedagógico combinado (o framework do livro)
Todo capítulo e toda etapa da construção seguem a combinação:
- **Backward Design** (Wiggins): escrever de trás para frente — objetivos (verbos de Bloom) → evidências/verificação → conteúdo.
- **4C/ID** (van Merriënboer): a trilha prática (`contexto-zero`) é a espinha — etapas = *learning tasks* (tarefas inteiras); capítulos = *supportive information*; boxes no código = *just-in-time*; katas = *part-task practice*.
- **Diátaxis**: quatro tipos de texto, **nunca misturados** na mesma seção — capítulos = *explanation*, construção = *tutorial*, catálogo de técnicas = *reference*, "o que roubar" = *how-to*.
- **Carga Cognitiva** (Sweller): *worked examples* antes de exercício; *completion problems* ("complete", não "crie do zero"); *fading* do andaime etapa a etapa; uma ideia nova por vez.
O esqueleto de capítulo (8 seções + Apêndice A) é a materialização deste princípio e é obrigatório.

### IV. Livro vivo (datação e expiração)
Coerência com a tese central (cláusula de expiração): o que se descreve é temporário — e nesta disciplina, notoriamente. Todo capítulo declara **data de captura** no cabeçalho; distinguem-se três datas (evento / captura / rodada de revisão); toda edição atualiza `livro/HISTORICO.md`, incluindo o **registro de expiração** (o placar das previsões). Reavaliar = nova rodada, nunca sobrescrever silenciosamente. Toda edição registra também a **versão do modelo de IA** usada (e a sessão), porque saídas de LLM são não-determinísticas e a rastreabilidade é parte do rigor (Guia §6.C).

### V. Segurança e credenciais
Nenhum segredo (chave de API, token) entra em arquivo, commit ou texto publicado — nunca. Credenciais vivem só em ambiente / `.env` gitignored. Chave exposta é chave comprometida: alertar e orientar revogação. O código didático demonstra a prática correta (a regra do cap. 17 aplicada ao próprio projeto). Dado recuperado é **conteúdo não confiável** por padrão — o livro nunca ensina um pipeline que trate resultado de retrieval como instrução.

### VI. Neutralidade e acessibilidade
A análise é vendor-agnóstica: técnicas são comparadas por problema resolvido, nunca por marca. Nenhum framework é o "jeito certo"; todo capítulo mostra a versão manual antes da versão com biblioteca. O livro é acessível — a trilha prática roda a custo zero (endpoint gratuito documentado, com créditos ao provedor) e sem GPU. Prosa em português; termos técnicos consagrados (prompt, contexto, retrieval, chunk, embedding, reranking) sem tradução.

### VII. Spec-driven e branch-per-melhoria (NÃO-NEGOCIÁVEL)
**Toda melhoria — inclusive as pedagógicas e editoriais — passa pelo spec-kit: `spec` → `plan` → `tasks` → `implement`, cada uma em sua própria branch.** Não há "só editar direto no main": um capítulo novo, um refinamento de método, uma etapa do `contexto-zero`, uma feature de infraestrutura — todos nascem de um spec (`specs/NNN-nome/spec.md`), ganham um plano e uma lista de tarefas, e só então são implementados, na branch `NNN-nome`. O merge para `main` acontece quando a melhoria está coerente e verificada.
- **Exceção única**: emendas a *esta constituição* (governança) podem ser feitas diretamente — mas são registradas aqui e no `HISTORICO.md`.
- Correções triviais (typo, link quebrado, ajuste de uma linha) podem ir direto ao main com commit descritivo; a regra vale para *melhorias*, não para consertos pontuais.
- **Exceção de fundação (edição 0.1)**: o ciclo de bootstrap que cria o esqueleto do livro é, ele próprio, a fundação sobre a qual o spec-kit passa a operar. Da edição 0.2 em diante, a regra vale sem ressalva.

### VIII. O escopo é o par, não a moda
O livro trata **duas disciplinas em relação**: engenharia de prompt (o que se escreve) e engenharia de contexto (o que se monta em runtime). **RAG não é o tema do livro — é a técnica central da segunda disciplina**, e é tratado como tal: com capítulos próprios, mas dentro da moldura maior. Nenhum capítulo pode existir sem responder à pergunta "que decisão sobre o que o modelo vê este capítulo ajuda a tomar?".

## Restrições da construção (contexto-zero)
1. **DDD leve** — linguagem ubíqua = glossário do livro; padrão tático só onde paga; DDD como consequência nomeada no código, não teoria.
2. **Arquitetura hexagonal por refatoração** — cada porta (`LLMPort`, `RetrieverPort`, `MemoryPort`, `EvalPort`) nasce da dor do capítulo correspondente; nunca estrutura antecipada.
3. **Do zero antes da biblioteca** — toda técnica é implementada na mão primeiro (BM25 em ~40 linhas antes de um vector DB); a biblioteca entra depois, nomeada como escolha, não como pré-requisito.
4. **Anti-apodrecimento** — modelo atrás de `LLMPort`; etapas autocontidas e executáveis; erros didáticos deliberados são comentados como tais.
5. **Chat congelado** — HTML+JS servido pelo backend; só evolui quando um capítulo exigir superfície nova. Stack: Python + FastAPI.

## Fluxo de trabalho e portões de qualidade
- Toda melhoria usa o spec-kit (princípio VII): `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` (com `/speckit-clarify` quando ambíguo), em branch `NNN-nome`. Os planos devem respeitar esta constituição.
- Pesquisa científica segue a skill `academic-research` (localizar → validar → registrar → integrar).
- **Revisão em duas camadas** (Guia §6.A, tradição Sommers/Flower-Hayes): antes do copyedit de superfície, um passo de **revisão *developmental*** — re-ver estrutura e sentido do texto (o argumento fecha? a ordem serve ao leitor? há redundância/lacuna?). "Escrever é reescrever": nenhum trecho novo é publicado sem esse passo.
- Antes de publicar (commit/push): evidência presente (I), fonte-base respeitada (II), esqueleto/método aplicado (III), **revisão developmental feita** e datação/histórico atualizados — **com a versão do modelo registrada** — quando o estado da arte mudou (IV), sem segredos (V), moldura do par preservada (VIII).
- Commits descrevem o "porquê"; o repositório é o registro. Push só quando o trabalho está coerente.

## Governança
Esta constituição prevalece sobre preferências pontuais. Emendas são registradas aqui e no `livro/HISTORICO.md`. O `CLAUDE.md` da raiz aponta para este documento como fonte de autoridade.

**Versão**: 2.0.0 | **Ratificada**: 2026-08-03 | **Origem**: derivada da constituição 1.2.0 do livro *Engenharia de Harness* (mesmo método, domínio novo). Mudanças de 1.2.0 → 2.0.0: Princípio II reescrito (a fonte-base deixa de ser "o código de harnesses" e passa a ser "paper + implementação pública"); Princípio I ganha a exigência de condição experimental junto do número; Princípio V ganha a cláusula de conteúdo recuperado não confiável; **Princípio VIII (novo)** fixa a moldura do par prompt×contexto e o lugar do RAG; restrição 3 da construção (do zero antes da biblioteca) é nova.
