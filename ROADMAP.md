# ROADMAP — Engenharia de RAG

> As rodadas planejadas do livro vivo. Cada rodada é um lote de trabalho que vira **uma ou mais specs** (`specs/NNN-nome/`), cada uma em sua branch, conforme o Princípio VII da [constituição](.specify/memory/constitution.md).
>
> Última atualização: **2026-08-04** · edição vigente: **0.2** (ver [Histórico](livro/HISTORICO.md))

## Onde estamos

**Edição 0.1 — a fundação.** O esqueleto está de pé: moldura definida, sumário em três partes, 19 capítulos com argumento fechado e explicação de abertura, catálogo de técnicas, mapa do ecossistema, glossário, bibliografia mapeada e o site publicando.

O que **ainda não** existe, e é deliberado:

| Ausente | Por quê | Volta em |
|---|---|:---:|
| Referências validadas (status ✓) | o levantamento localizou; validar exige ler | rodada 2 |
| Profundidade nos capítulos | a v1 prioriza a moldura completa sobre a profundidade parcial | rodadas 2–3 |
| Trilha prática `rag-zero` | descrita nos capítulos, não implementada | rodada 3 |
| Avaliação comparada de ferramentas | exige metodologia própria | rodada 4 |
| Chat companion ligado | backend existe, corpus e capacidades adaptados; falta o deploy | rodada 3 |
| Edição em inglês | fora do escopo da v1, por decisão | rodada 7 |
| Radar de atualização | fora do escopo da v1, por decisão | rodada 6 |

---

## Rodada 1b — Reestruturação para Engenharia de RAG ✅ (concluída em 2026-08-04)

**Entregue:** constituição 3.0.0 (o objeto é o sistema; componente declarado por capítulo; fronteira com o livro irmão) · 3 capítulos novos (02 anatomia, 03 arquiteturas, 15 geração fundamentada) · Parte III desdobrada em 5 · 2 capítulos devolvidos ao livro irmão · survey de Gao registrada · `rag-zero` com 17 etapas · capa nova.

---

## Rodada 1 — Fundação ✅ (concluída em 2026-08-04)

**Entregue:** constituição 2.0.0 · panorama da comunidade · sumário em 3 partes · 19 capítulos (esqueleto + explicação) · catálogo de técnicas · apêndice do ecossistema · glossário · bibliografia com status · guia editorial · histórico e registro de expiração · motor de publicação adaptado (PT-only, sem Radar, grafo remapeado).

---

## Rodada 2 — Evidência (a que tira os ⏳)

**Objetivo:** transformar o mapa em livro citável. Nenhuma outra rodada deveria vir antes desta — a credibilidade do projeto depende dela.

**Escopo:**
1. **Validar os surveys estruturantes** (S1, S2, S3 da [bibliografia](livro/bibliografia.md)) pela skill `academic-research`: ler, conferir o que o livro afirma sobre eles, registrar ✓.
2. **Validar a lacuna prioritária**: a afirmação do cap. 20 de que a degradação em contexto longo é dirigida pela **similaridade entre alvo e distratores** (hoje a citação mais frágil do livro).
3. **Registrar condição experimental** de todo número citado — em especial os de otimização de prompt (cap. 16), *contextual retrieval* (cap. 09) e memória (cap. 19), todos auto-reportados pelos proponentes.
4. **Preencher os Apêndices A** dos capítulos com o tratamento por implementação.
5. **Aprofundar o corpo** dos capítulos onde a validação trouxer material novo.
6. **Validar as seis técnicas nomeadas** que entraram no adendo 0.1.1 (RAPTOR · Self-RAG · CRAG · FLARE · Adaptive RAG · step-back), cada uma com fonte primária e condição experimental.
7. **Dar base de evidência ao cap. 04** (Ingestão e Governança do Corpus, criado no adendo 0.1.2). É hoje o capítulo mais fraco do livro em citação: a área trata ingestão como pré-processamento e raramente a estuda. Pergunta a responder: **existe medição publicada do impacto isolado de frescor e deduplicação sobre métricas de RAG?** Se não existir, vira experimento próprio na rodada 4.

**Critério de conclusão:** ao menos 60% das referências com status ✓; nenhum número no corpo sem condição experimental; nenhum capítulo com Apêndice A vazio.

**Sugestão de fatiamento em specs:** `002-evidencia-parte-i` (caps. 11–17) · `003-evidencia-parte-ii` (caps. 20–14) · `004-evidencia-parte-iii` (caps. 21–24).

---

## Rodada 3 — `rag-zero` (a trilha prática)

**Objetivo:** o livro executável. 18 etapas, uma por capítulo, Python + FastAPI, custo zero e sem GPU.

**Escopo:**

| Etapa | Capítulo | Entrega |
|:---:|:---:|---|
| 0 | 01 | chat mínimo + `LLMPort` + **contador de tokens por bloco** (o instrumento do livro) |
| 1 | 02 | prompt em blocos nomeados + teste de separação instrução×dado |
| 2 | 03 | duas famílias de raciocínio, comparadas com números |
| 3 | 04 | schema + validação + ciclo de reparo com teto |
| 4 | 05 | cinco camadas + cascata + **teste de estabilidade de prefixo** |
| 5 | 06 | otimizador mínimo na mão (60 linhas), depois com framework |
| 6 | 07 | conjunto de eval + **calibração do juiz** |
| 7 | 08 | orçamento com política de corte declarada |
| 8 | 09 | **ingestão**: extração, dedup, metadado com status, política de saída |
| 9 | 10 | BM25 na mão (~40 linhas) + chunking estrutural |
| 10 | 10–11 | embeddings + fusão + reranking + contextual retrieval, com medição por estágio |
| 11 | 12 | recuperação como ferramenta + reflexão + teto |
| 12 | 13 | memória com procedência, data e exclusão real |
| 13 | 14 | compactação + estado estruturado que nunca compacta |
| 14 | 15 | ferramentas com teto no adaptador e procedência marcada |
| 15 | 16 | as quatro métricas + tabela de diagnóstico |
| 16 | 17 | **atacar o próprio sistema** e medir o que cada camada bloqueia |
| 17 | 18 | painel: custo por parcela + cache + latência + qualidade |

**Também nesta rodada:** ligar o **chat companion** em produção (o companion *é* o `rag-zero` rodando, e vira o exemplo real que o livro disseca), com gating de capacidades por capítulo.

**Critério de conclusão:** as 18 etapas executáveis com testes verdes; o companion no ar respondendo sobre o livro.

---

## Rodada 4 — Avaliação de técnicas (o "benchmark" deste livro)

**Objetivo:** o equivalente empírico ao benchmark de harnesses do livro irmão — mas aqui o objeto avaliado é **a técnica**, não o produto.

**Escopo:**
1. **Metodologia** em `benchmark/README.md`: dimensões, escala, exigência de evidência, e o que **não** se avalia.
2. **Corpus de avaliação próprio** — o texto deste livro mais um corpus de domínio, com perguntas verificadas por gente.
3. **Avaliar as técnicas do catálogo** que forem mensuráveis: híbrido × denso × esparso; contextual retrieval × late chunking; com e sem reranking; famílias de raciocínio; otimizadores de prompt.
4. **Publicar a condição experimental completa** — modelos, corpus, orçamento, data. Sem isso o número não vale, e o livro não pode cobrar dos outros o que não faz.

**Critério de conclusão:** cada técnica avaliada tem número **reproduzível** com receita publicada.

---

## Rodada 5 — Catálogo completo

**Objetivo:** expandir o [catálogo de técnicas](livro/apendice-tecnicas.md) para a cobertura da taxonomia de referência (as 58 técnicas do *Prompt Report*, mais o lado de contexto), com uma ficha por técnica: fonte primária · o que resolve · quando usa · o que custa · condição da medição publicada.

Depende da rodada 2 (validação) e se beneficia da 4 (medição própria).

---

## Rodada 6 — Livro vivo: Radar e revisão do placar

**Objetivo:** ligar o mecanismo de atualização contínua.

**Escopo:**
1. **Radar** — acompanhamento datado do que aparece na área (papers, técnicas, ferramentas), com impacto classificado e ligação ao capítulo afetado.
2. **Revisão do registro de expiração** — fechar as apostas cujo prazo venceu (A1 e A5 vencem em 2027-08), com veredito ✅/❌/🔄. **Aposta refutada não se apaga.**
3. **Recaptura de datas** nos capítulos cujo estado da arte mudou.
4. **Subir os pisos** de qualidade do grafo (nós e arestas), calibrados hoje para a edição 0.1.

---

## Rodada 7 — Edição em inglês

**Objetivo:** a tradução, com o PT como fonte canônica e o EN como artefato derivado, com **selo de sincronia** (cada fonte EN carrega o hash do PT que traduziu; o build compara e marca "em dia" ou "atrasado" — tradução velha nunca finge ser atual).

O motor já tem essa capacidade implementada e desligada; religá-la é reintroduzir `publicar/sumario.en.json` e `livro/en/`.

---

## Rodada 8 — Edição 1.0

**Objetivo:** a obra citável.

**Escopo:** revisão developmental completa · registro de DOI (Zenodo/DataCite) com versionamento por edição · PDF consolidado revisado · `CITATION.cff` e `.zenodo.json` atualizados.

---

## Como uma rodada vira trabalho

Cada rodada se decompõe em specs, e cada spec segue o ciclo:

```
specify → checklist/clarify → plan (Constitution Check) → tasks → implement → registrar → merge
```

1. `bash .specify/scripts/bash/create-new-feature.sh "<nome>"` cria `specs/NNN-nome/`
2. `git checkout -b NNN-nome`
3. `spec.md` (o quê/porquê) → `plan.md` (como, com o Constitution Check) → `tasks.md` (verificável)
4. implementar e **verificar**: `cd publicar && npm run build` verde
5. atualizar [`livro/HISTORICO.md`](livro/HISTORICO.md) — com o modelo de IA registrado
6. `git merge --no-ff NNN-nome` na `main` — **o merge é o que publica**

**Uma rodada não precisa ser uma spec só.** Rodadas grandes (2, 3) rendem melhor fatiadas por parte do livro, com um merge por lote.

## Princípios que restringem toda rodada

Do mais restritivo ao menos, para consulta rápida:

- **Nenhum número sem condição experimental** (I) — nem de fornecedor grande, nem quando confirma o que queríamos.
- **Paper + implementação pública** antes de entrar no corpo (II).
- **Um capítulo não existe** sem responder "que decisão sobre o que o modelo vê ele ajuda a tomar?" (VIII).
- **Do zero antes da biblioteca** na trilha prática (restrição 3).
- **Toda melhoria em branch própria**, via spec-kit (VII).
- **Toda edição datada e atribuída**, com o modelo de IA registrado (IV).
