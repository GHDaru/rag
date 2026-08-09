# ROADMAP — Engenharia de RAG

> As rodadas planejadas do livro vivo. Cada rodada é um lote de trabalho que vira **uma ou mais specs** (`specs/NNN-nome/`), cada uma em sua branch, conforme o Princípio VII da [constituição](.specify/memory/constitution.md).
>
> Última atualização: **2026-08-09** · edição vigente: **0.4** (ver [Histórico](livro/HISTORICO.md))

## Onde estamos

**Edição 0.4 — o esqueleto do sistema, com a rodada de evidência concluída.** O livro é *Engenharia de RAG* e o esqueleto está de pé: **25 capítulos** em cinco partes (arquitetura · corpus · recuperação · geração · sistema em produção), cada um com argumento fechado, o componente da arquitetura que aprofunda declarado no cabeçalho, e a etapa correspondente do `rag-zero` descrita. Mais o aparato — catálogo de técnicas, mapa do ecossistema, glossário, bibliografia mapeada, grafo do livro — e o site publicando.

O que a 0.2 fez além de renomear: os três capítulos que fechavam a lacuna real (**02** anatomia, **03** arquiteturas de referência, **15** geração fundamentada), a Parte III desdobrada em cinco, e a fronteira com o livro irmão tornada explícita na constituição.

O que **ainda não** existe, e é deliberado:

| Ausente | Por quê | Volta em |
|---|---|:---:|
| Referências validadas (status ✓) | **42 de 55 (76%)** — rodada 2 ✅ concluída; as 13 restantes são de menor peso | — |
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

## Rodada 2 — Evidência ✅ (concluída em 2026-08-09)

**Objetivo:** transformar o mapa em livro citável. Nenhuma outra rodada deveria vir antes desta — a credibilidade do projeto depende dela.

### Feito (edição 0.3, 2026-08-04)

1. ✅ **Os 49 identificadores arXiv resolvidos** contra o arXiv real, com ID falso de controle. **Nenhum inventado, nenhum título divergente** — a classe de erro mais corrosiva está descartada.
2. ✅ **42 das 55 referências em ✓ (76%)** — texto lido, afirmação do livro conferida. Acima do critério de 60%.
3. ✅ **As ~20 técnicas nomeadas ganharam fonte primária.** Entraram pelos guias de praticante (RAPTOR, Self-RAG, CRAG, FLARE, Adaptive RAG, HyDE, step-back, late chunking, proposição, GraphRAG) e **todas chegaram ao paper que as propôs**.
4. ✅ **Quatro afirmações corrigidas** ([detalhe](livro/bibliografia.md#correções-que-esta-rodada-produziu)):
   - *Lost in the Middle* **não sustentava** a afirmação do cap. 20 sobre distratores — e a fonte que sustenta contradiz a outra metade;
   - as quatro métricas do RAGAS **não são todas do paper** (ele propõe três);
   - a escolha entre *contextual retrieval* e *late chunking* **não é só de preço** — há troca de qualidade medida;
   - o `67%` do *contextual retrieval* agora aparece com a curva inteira e o custo em dólar.
5. ✅ **Condição experimental ao lado de todo número validado.**

### Aberto

1. **As 13 referências ⏳** — otimizadores secundários (P7–P10), modos de falha de memória (M2–M5), e três de escopo estreito (Q3, E3, Z1). Nenhuma sustenta sozinha uma tese de capítulo.
3. **Base de evidência do cap. 04.** Segue o capítulo mais fraco em citação, e a pergunta continua sem resposta: **existe medição publicada do impacto isolado de frescor e deduplicação sobre métricas de RAG?** Se não existir, vira experimento próprio na rodada 4.
4. **Aprofundar o corpo** dos capítulos onde a validação trouxe material novo — em especial 05 (métricas intrínsecas de chunking) e 09 (a troca de qualidade).

**Critério de conclusão — os três atingidos:** ≥ 60% das referências em ✓ (**76%**); nenhum número no corpo sem condição experimental (**feito** para os validados); nenhum capítulo com Apêndice A vazio (**22 de 22 preenchidos**, cada implementação citada com URL conferida).

**Rodada 2 concluída.** O que sobrou (13 referências de menor peso e a evidência do cap. 04) migra para a rodada 4, onde vira medição própria em vez de busca bibliográfica.

---

## Rodada 3 — `rag-zero` (a trilha prática)

**Objetivo:** o livro executável. **17 etapas** (0–16), Python + FastAPI, custo zero e sem GPU. A Parte IV inteira converge para a etapa 10, porque é um gerador só — construído em camadas.

**Escopo:**

| Etapa | Capítulo | Entrega |
|:---:|:---:|---|
| 0 | 01 | chat mínimo + `LLMPort` + **contador de tokens por bloco** (o instrumento do livro) |
| 1 | 02 | os dois caminhos separados no código, com os quatro contratos explícitos |
| 2 | 03 | o Naive RAG inteiro, ponta a ponta — a linha de base honesta |
| 3 | 04 | **ingestão**: extração, dedup, metadado com status, geração de metadado, política de saída |
| 4 | 05 | chunking estrutural + embeddings, com a unidade de busca desacoplada da de entrega |
| 5 | 06 | BM25 na mão (~40 linhas), depois denso, depois a fusão por posição — os três medidos |
| 6 | 07 | reranking com nota usada como limiar, e a curva de N |
| 7 | 08 | reescrita, HyDE e roteamento, cada um medido contra a linha de base |
| 8 | 09 | contextual retrieval × late chunking, com as duas contas lado a lado |
| 9 | 10 | RAPTOR reduzido (~80 linhas) + roteador por nível. Grafo fica de fora, e a etapa explica por quê |
| 10 | 11–17 | **o gerador**: prompt em blocos, schema, camadas por volatilidade, fundamentação com citação e abstenção, eval de prompt |
| 11 | 18 | recuperação como ferramenta + reflexão + teto de iterações |
| 12 | 19 | resolução de referência entre turnos + memória com procedência e exclusão real |
| 13 | 20 | orçamento com política de corte declarada |
| 14 | 21 | as quatro métricas + tabela de diagnóstico |
| 15 | 22 | **atacar o próprio sistema** e medir o que cada camada bloqueia |
| 16 | 23 | painel: custo por parcela + cache + latência + qualidade |

**Também nesta rodada:** ligar o **chat companion** em produção (o companion *é* o `rag-zero` rodando, e vira o exemplo real que o livro disseca), com gating de capacidades por capítulo.

**Critério de conclusão:** as 17 etapas executáveis com testes verdes; o companion no ar respondendo sobre o livro.

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
