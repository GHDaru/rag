# 0009 — Escopo da edição 1.0

- **Status:** Aceito
- **Data:** 2026-08-09
- **Contexto (feature/spec):** `001-edicao-1-0`

## Contexto

O autor autorizou uma execução longa para fechar a **primeira versão** do livro. O
ROADMAP tinha oito rodadas; as rodadas 1, 1b e 2 estavam concluídas e a 3 (`rag-zero`)
em 7 de 17 etapas. Faltava decidir **o que é condição de 1.0** e o que é pós-1.0.

Dois pareceres independentes foram solicitados antes da decisão, em contexto fresco, e
suas acusações foram **verificadas uma a uma** contra o repositório antes de virarem
plano. Todas se confirmaram.

**Parecer de processo** — veredito *não conforme*, por incoerência declarada e ausência
de rastro:

- O `README.md` anunciava **"Edição 0.2"** com a edição vigente em 0.6, e se contradizia
  em duas linhas consecutivas: *"Os 22 Apêndices A estão preenchidos"* seguido de *"Os
  Apêndices A estão enfileirados, não escritos"*.
- **29 cabeçalhos de capítulo** com a edição errada (25 em `0.4`, 4 em `0.2`).
- `CITATION.cff` e `.zenodo.json` descreviam o objeto da constituição **2.0.0**, revogada
  — *"RAG é tratado como a técnica central da engenharia de contexto, não como moldura"*.
  O artefato que torna a obra citável citava o livro anterior.
- `CLAUDE.md` resumia o Princípio VIII pela redação revogada.
- **`specs/` não existia**, e `.specify/feature.json` apontava para
  `specs/075-capa-news-recente` — diretório inexistente, herdado do livro irmão. Cinco
  edições foram produzidas sem nenhum `plan.md`, que é **o único lugar onde o
  Constitution Check mora**. Um ciclo sem `plan.md` é um ciclo sem portão.
- **Nenhum ADR (*Architecture Decision Record*) deste projeto**, embora o índice
  prometesse que *"ADRs a partir do 0009 são deste projeto"* — e decisões grandes
  (renomear o livro, constituição 3.0.0, criar o cap. 04) nunca foram registradas.

**Parecer de didática** — veredito: *o leitor sai sabendo **decidir e diagnosticar**, não
**construir***:

- **20 dos 25 capítulos não têm um único bloco de código.** O cap. 15 prescreve as três
  exigências do prompt de fundamentação e **nunca mostra o prompt**.
- Os 25 blocos "Mão na massa" descrevem o `rag-zero` em prosa, **sem caminho de arquivo,
  sem comando e sem saída esperada** — e `rag-zero/` **não está em `sumario.json`**: para
  quem lê o site publicado, a espinha 4C/ID não existe.
- Nove capítulos descrevem no presente etapas que **não foram construídas**.
- **Siglas órfãs, inclusive a do título:** *Retrieval-Augmented Generation* nunca é
  expandida no corpo dos caps. 00 e 01; *Large Language Model* (LLM) não é expandida em
  lugar nenhum; `top_k` é usado ~20 vezes sem definição e sem verbete.
- **Remissões erradas em pontos de decisão:** a tabela de diagnóstico do cap. 21 — o
  instrumento central do livro — manda ao cap. 11 o que está no 15.

## Decisão

**A 1.0 fecha por coerência e por escada, não por volume.** O escopo é:

1. **Portão de processo** — `specs/001-edicao-1-0/` com `spec.md`, `plan.md` (com
   Constitution Check contra os oito princípios) e `tasks.md`; ADRs deste projeto a
   partir deste.
2. **Coerência declarada** — datação, `README.md`, metadado de citação, `CLAUDE.md`,
   remissões e numeração de etapas.
3. **A escada de execução visível** — pelo menos um artefato concreto por capítulo onde
   hoje há só prescrição; cada "Mão na massa" com arquivo, comando e saída esperada; o
   `rag-zero` no sumário do livro.
4. **O piso do `rag-zero`** — etapa 2 (*Naive RAG* ponta a ponta, que é a **linha de
   base** sem a qual nenhuma tabela de ganho do livro compara com nada), etapa 1
   (contratos), etapas 7 e 8, e a etapa 14 completa. As demais ficam **declaradas como
   especificadas**, não descritas no presente.
5. **Higiene de leitura** — siglas expandidas na primeira ocorrência e no glossário; uma
   página "Como ler este livro" com pré-requisitos e trilhas.
6. **Evidência sem dívida escondida** — critério verificável: **nenhuma afirmação do
   corpo apoiada em fonte não-✓**. Vale validar **ou** enfraquecer a afirmação.
7. **Gate** — revisão independente em contexto fresco (quem executou não verifica),
   *Definition of Done* (DoD) verificável, e registro no `HISTORICO.md`.

**Fora da 1.0, explicitamente:** rodada 4 (medição própria), rodada 5 (as 58 técnicas do
*The Prompt Report*), rodada 6 (Radar e placar de expiração), rodada 7 (edição em
inglês), *Digital Object Identifier* (DOI) e PDF consolidado, deploy do chat companion
(ver ADR 0010), e as etapas 15–16 do `rag-zero`.

## Alternativas avaliadas

- **A — 1.0 = ROADMAP inteiro (rodadas 3 a 5).** Prós: cobertura máxima. Contras: a
  rodada 4 exige, pela metodologia do próprio `benchmark/README.md`, dois corpora e três
  execuções com dispersão — é programa de pesquisa, não item de fechamento. A rodada 5
  aumentaria o catálogo de técnicas, que é exatamente o que a tese do cap. 02 critica.
  **Escopo inflado disfarçado de rigor.**
- **B — 1.0 = só coerência (parar de escrever e arrumar).** Prós: barato, rápido.
  Contras: não resolve a quebra que o parecer didático aponta como central — o livro
  continuaria ensinando a decidir sem ensinar a construir, com a espinha invisível.
- **C — coerência + escada visível + piso da trilha (a escolhida).** Prós: ataca as duas
  quebras reais com custo baixo comparado ao já feito; a 1.0 entrega o que promete.
  Contras: deixa 10 das 17 etapas fora, o que exige **declarar maturidade em vez de
  fingir** — custo aceito e coberto pelo Princípio IV.

## Justificativa

Os dois pareceres, produzidos sem contato entre si, convergiram na mesma causa: **o livro
não está bloqueado por falta de conteúdo, e sim por coerência entre o que ele afirma e o
que ele entrega.** O processo apontou incoerência de estado; a didática, incoerência de
promessa. A alternativa C é a única que trata as duas.

O peso decisivo veio de duas observações. Primeira: *"se o long run começar pela
construção sem passar pelo portão, ele produz mais volume sobre um estado já descrito de
forma incorreta"* — que é precisamente o modo de falha que este repositório **já
demonstrou** (o README contradizendo a si mesmo em duas linhas). Segunda: *"o que falta
não é conteúdo novo, é tornar visível a metade prática que já existe"* — o `rag-zero`
está construído em 7 etapas e **invisível para quem lê o site**.

## Consequências

- **Positivas:** a 1.0 passa a ter critério de aceite verificável em vez de sensação de
  completude; o Princípio VII volta a ter rastro material; o leitor ganha a escada de
  execução que o método 4C/ID promete desde a edição 0.1.
- **Negativas / custos aceitos:** a 1.0 sai com **10 de 17 etapas** do `rag-zero` não
  construídas e com 13 referências ⏳. Ambos ficam **declarados** — o Princípio IV
  autoriza declarar maturidade; o que ele proíbe é fingir. O catálogo de técnicas
  permanece parcial em relação à taxonomia de referência, por decisão (YAGNI).
- **Reversibilidade:** alta. Tudo que ficou fora está no ROADMAP como pós-1.0 e volta em
  rodada própria. Nenhum item excluído fecha porta: a medição própria, o inglês e o DOI
  são aditivos.
