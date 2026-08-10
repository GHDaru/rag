# 21 — Avaliação e Observabilidade

> **Estado da arte capturado em 2026-08** · edição 1.0 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** Componentes que aprofunda: **avaliador** e **observabilidade** (cap. 02). As quatro métricas e a tabela de diagnóstico estão fechadas; o tratamento por ferramenta e benchmark é a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Separar** a avaliação da recuperação da avaliação da geração — e explicar por que juntá-las impede o diagnóstico;
2. **Definir** as quatro métricas de referência e o que cada uma revela;
3. **Diagnosticar** uma falha de RAG a partir da combinação de métricas;
4. **Montar** um conjunto de avaliação com dados sintéticos sem cair no viés de avaliar o modelo com ele mesmo.

## O problema

"O RAG não está bom" é um sintoma com pelo menos quatro causas distintas — e as quatro exigem intervenções diferentes, em partes diferentes do sistema. Sem separar as medições, o time otimiza no lugar errado, com sorte por meses.

A separação mínima é entre **achar** e **usar**:

- A recuperação trouxe o que precisava? (falha aqui = caps. 05–10)
- A resposta usou o que foi trazido, sem inventar? (falha aqui = geração, prompt, cap. 11/13)

Um sistema pode ter recuperação excelente e resposta péssima. E — o caso que mais engana — pode ter recuperação péssima e resposta que **parece** boa, porque o modelo preencheu as lacunas com conhecimento paramétrico plausível. Este segundo caso passa em qualquer avaliação superficial e falha exatamente onde importa: no caso raro, no dado novo, no que a empresa tem de específico.

## Fundamentos científicos

- **Benchmarks de recuperação** — **BEIR** ([arXiv 2104.08663](https://arxiv.org/abs/2104.08663), 18 datasets × 10 sistemas) e **MTEB** ([arXiv 2210.07316](https://arxiv.org/abs/2210.07316), 8 tarefas × 58 datasets × 112 idiomas × 33 modelos) medem o estágio isolado. Os dois entregam um achado que é regra de projeto: *"BM25 is a robust baseline"* e *"no particular text embedding method dominates across all tasks"*. Ou seja: **compare sempre contra o BM25, e desconfie de "o melhor embedder"**. ✓
- **Avaliação ponta a ponta** — não há benchmark único de RAG; a prática recomendada é combinar dois ou três, cobrindo estágios distintos: recuperação pura (BEIR), fidelidade da geração, e conjuntos próprios do domínio. `[a validar]`
- **Avaliação sob contexto longo** — *U-NIAH* ([arXiv 2503.00353](https://arxiv.org/abs/2503.00353)) unifica a avaliação de RAG e de contexto longo no mesmo protocolo, permitindo comparar os dois regimes em vez de discuti-los por anedota (cap. 20). `[a validar]`
- **Benchmarks de domínio** — há uma tendência de frameworks de benchmarking adaptativo por setor (por exemplo, [FAB-Bench](https://arxiv.org/abs/2605.26476), **para manufatura de semicondutores** — o domínio faz parte da citação), sintoma de um fato inconveniente: **resultado em benchmark geral não transfere para domínio específico**. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **RAGAS** — estabeleceu o vocabulário de fato da área, e a atribuição precisa importa: o **paper** ([arXiv 2309.15217](https://arxiv.org/abs/2309.15217), EACL 2024) propõe **três** aspectos — *faithfulness*, *answer relevance* e ***context relevance*** ("the retrieved context should be focused, containing as little irrelevant information as possible"), todos **reference-free**, sem anotação humana. O par *context precision* / *context recall* que a área usa hoje é da **biblioteca**, não do paper: ela desdobrou *context relevance* em duas, porque as duas metades diagnosticam falhas diferentes — e é esse desdobramento que torna a tabela da próxima seção possível. ✓ (lido no original)
- **DeepEval** — as mesmas ideias com foco em integração de CI/CD. A leitura de 2026 é complementar, não concorrente: **RAGAS fornece o arcabouço conceitual; DeepEval, a execução em pipeline**.
- **TruLens** e a família de observabilidade — instrumentação de execução, útil para o que este livro chama de trajetória (cap. 18).
- **A prática que separa** — os times que conseguem melhorar RAG são os que têm um conjunto de avaliação **do próprio domínio**, com respostas verificadas por gente. Todo o resto é diagnóstico assistido.

## O estado da arte

### 1. As quatro métricas, e o que cada uma responde

| Métrica | Pergunta | Estágio | Falha indica |
|---|---|---|---|
| **Context recall** | os trechos necessários foram recuperados? | recuperação | índice, chunking, busca (caps. 05, 06, 09) |
| **Context precision** | os trechos recuperados eram relevantes? | recuperação | `top_k` alto, ranking fraco, orçamento desperdiçado (cap. 20) |
| **Faithfulness** | a resposta é sustentada pelo que foi recuperado? | geração | alucinação; prompt sem regra de fundamentação (cap. 11) |
| **Answer relevance** | a resposta responde à pergunta feita? | geração | o modelo respondeu outra coisa |

*Faithfulness* é a que mais importa e a mais mal compreendida. Ela é calculada decompondo a resposta em afirmações e verificando quantas são **inferíveis do contexto fornecido**. Uma resposta factualmente correta mas não sustentada pelo contexto tem *faithfulness* baixa — e isso é o comportamento desejado, não um defeito da métrica: significa que o modelo respondeu de memória, e você não tem garantia nenhuma sobre a próxima pergunta.

### 2. A tabela de diagnóstico

A combinação das métricas localiza o problema — é o instrumento que o cap. 09 pede antes de escolher técnica:

| Recall | Precision | Faithfulness | Diagnóstico | Onde agir |
|:---:|:---:|:---:|---|---|
| baixo | — | — | não acha | chunking, busca híbrida, reescrita (caps. 05, 06, 08) |
| alto | baixo | — | acha e traz lixo junto | reranking, `top_k` menor (cap. 07) |
| alto | alto | baixo | tem tudo e inventa | prompt de fundamentação, regra de abstenção (cap. 11) |
| alto | alto | alto | e ainda erra | a pergunta exige raciocínio (cap. 12) ou multi-hop (cap. 10) |

Esta tabela é, sozinha, o motivo de o capítulo existir. Sem ela, "melhorar o RAG" é tentativa e erro caro.

### 3. Conjuntos de avaliação: de onde vêm

Três origens, em ordem crescente de valor e de custo:

- **Sintético a partir do corpus.** Gera-se perguntas a partir dos documentos. Barato, cobre volume, e tem um viés conhecido: perguntas geradas de um trecho são respondíveis por aquele trecho, o que **superestima** o recall e não testa multi-hop nem pergunta mal formulada.
- **Perguntas reais de usuários**, com resposta verificada por gente. Caro, insubstituível — é o único conjunto que contém as ambiguidades e os erros de digitação do mundo real.
- **Casos de falha registrados.** O mesmo princípio do cap. 17: todo incidente vira caso. É o conjunto que cresce sozinho e com valor.

O erro estrutural a evitar: gerar perguntas **e** julgar respostas com o mesmo modelo que gera as respostas. O sistema passa a ser avaliado pelo seu próprio viés, e o número resultante mede consistência, não qualidade.

### 4. Do eval ao painel: os sinais de produção

Eval responde "está bom?" sobre um conjunto fixo. Produção precisa de sinais **contínuos**, que avisem quando algo mudou sem esperar a próxima rodada de avaliação. A prática consolidada separa por camada:

**Camada de recuperação**

- **Taxa de resultado zero** — quantas consultas voltam sem nada acima do limiar. É o sinal mais barato e mais informativo do pipeline: se sobe, ou o corpus tem lacuna, ou o padrão de pergunta mudou, ou o índice quebrou. E se está em **zero**, o alerta é outro: provavelmente não existe limiar nem caminho de abstenção (cap. 06), e o sistema está devolvendo ruído com cara de resposta.
- **Distribuição das notas do reranker** — não a média, a distribuição. Uma cauda que engorda perto do limiar indica corpus mudando antes de qualquer métrica de qualidade acusar.
- **Latência por percentil** (p50, p95, p99), separada da geração.

**Camada de geração**

- **Taxa de citação** — quantas respostas de fato referenciam o que foi recuperado. É *faithfulness* na versão barata, calculável sem juiz, em toda requisição.
- **Latência e contagem de tokens** por percentil.

Dois cuidados que separam painel de enfeite:

- **Limiar de alerta é local.** Números de referência publicados por fornecedores (p99 de recuperação abaixo de X ms, taxa de resultado zero abaixo de Y%) valem como ponto de partida, nunca como meta — dependem do corpus, do hardware e do que o produto tolera. Calibre com a sua própria linha de base.
- **O p99 é onde o cap. 18 aparece.** Um laço agêntico não mexe muito na mediana e alarga a cauda. Quem monitora só p50 não vê a autonomia chegando na fatura.

### 5. O que a instrumentação atual não cobre

- **Trajetória.** Em RAG agêntico (cap. 18), duas execuções com a mesma resposta podem ter custos muito diferentes. Nenhuma das quatro métricas vê isso.
- **Conversa.** As métricas são por turno. A falha do cap. 19 — perder a referência ao longo da conversa — é invisível para todas elas.
- **Custo como métrica de primeira classe.** Qualidade sem custo ao lado leva a decisões que não sobrevivem à revisão de fatura (cap. 23).
- **Deriva.** O corpus muda, o modelo muda, o padrão de pergunta muda. Sem execução periódica sobre um conjunto fixo, a degradação lenta é invisível até virar reclamação.

### Leitura executiva

"O RAG não está bom" tem pelo menos quatro causas distintas, e a separação mínima é entre **achar** e **usar**. **O que roubar:** a **tabela de diagnóstico** — recall baixo = não acha (chunking/busca); recall alto + precision baixo = traz lixo junto (reranking, `top_k` menor); recall e precision altos + faithfulness baixa = **tem tudo e inventa** (prompt de fundamentação). Sem ela, "melhorar o RAG" é tentativa e erro caro. **A métrica mais mal compreendida:** *faithfulness* baixa numa resposta **factualmente correta** não é defeito da métrica — significa que o modelo respondeu de memória, e você não tem garantia nenhuma sobre a próxima pergunta. Esse é o caso que mais engana, porque parece bom. **Sobre conjuntos:** sintético a partir do corpus é barato e **superestima o recall** (a pergunta gerada de um trecho é respondível por aquele trecho); pergunta real com resposta verificada por gente é insubstituível. **Nunca** gere as perguntas e julgue as respostas com o mesmo modelo que responde — isso mede consistência, não qualidade. **Do eval ao painel:** eval mede um conjunto fixo; produção precisa de sinais contínuos — e o mais barato e informativo é a **taxa de resultado zero**. Se ela sobe, algo mudou no corpus ou nas perguntas; se está em **zero**, provavelmente não há limiar nem caminho de abstenção, e o sistema devolve ruído com cara de resposta. Monitore também **p99** (é onde o laço agêntico do cap. 18 aparece, não na mediana) e a **taxa de citação**, que é *faithfulness* na versão barata, sem juiz. **As lacunas abertas:** trajetória, conversa (não só turno), custo ao lado da qualidade, e deriva.

## Mão na massa — `rag-zero`, etapa 14

Na etapa 14 você monta o eval do `rag-zero`: 30 perguntas sobre o texto deste livro (metade sintéticas, metade escritas por você), as quatro métricas implementadas com juiz de família diferente, e a tabela de diagnóstico impressa ao final. A etapa termina com um exercício desconfortável e deliberado: rodar o eval sobre a etapa 9 (só BM25) e sobre a etapa 10 (pipeline completo) e verificar se o ganho que você **esperava** aparece. O exercício de completude: o cálculo de *faithfulness* vem esqueletado — você implementa a decomposição em afirmações e descobre onde a métrica é frágil.

**Rode agora** — sem instalar nada, sem chave e sem GPU:

```bash
cd rag-zero
python3 etapas/etapa05_busca.py
```

Código: [`rag_zero/avaliacao.py`](https://github.com/GHDaru/rag/blob/main/rag-zero/rag_zero/avaliacao.py). O que você deve ver: as métricas de recuperação por estágio — e a armadilha do `recall@k` com gabarito grande.
## Verificação

1. *Context recall* 0,9, *context precision* 0,4, *faithfulness* 0,85. Qual é o problema, e qual o custo escondido dele? (Dica: cap. 20.)
2. Por que uma resposta correta pode — e deve — receber *faithfulness* baixa? O que isso avisa sobre o sistema?
3. Você gerou 200 perguntas sinteticamente e o recall ficou em 0,95. Cite duas razões para não comemorar.

---

## Apêndice A — Como cada ferramenta e benchmark avalia

> Tratamento por ferramenta, com o que mede **e o que não mede**.

| Ferramenta | Implementação | O que mede — e o que não |
|---|---|---|
| **RAGAS** | [explodinggradients/ragas](https://github.com/explodinggradients/ragas) | as quatro métricas operacionais, **reference-free**, e gera conjunto de teste a partir do corpus. **Atenção à atribuição:** o paper propõe três aspectos (*faithfulness*, *answer relevance*, *context relevance*); o par *precision*/*recall* é da biblioteca. |
| **DeepEval** | [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | as mesmas ideias com foco em **execução em CI**. A leitura de 2026: RAGAS dá o arcabouço conceitual, DeepEval a execução em pipeline. |
| **promptfoo** | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | avaliação **e** red teaming no mesmo lugar, com casos mapeados ao OWASP LLM Top 10 — o que materializa a tese do cap. 22 de que teste adversarial **é** eval. |
| **BEIR** | [beir-cellar/beir](https://github.com/beir-cellar/beir) | recuperação zero-shot em 18 datasets. **Não mede** geração, nem o seu domínio. |
| **MTEB** | [embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb) | embeddings em 8 tarefas e 112 idiomas. **Não diz** qual serve para você — o próprio paper conclui que nenhum domina em todas as tarefas. |
| **Chunking, isolado** | as cinco métricas intrínsecas de [arXiv 2603.25333](https://arxiv.org/abs/2603.25333) | permitem avaliar o **corte** sem pipeline inteiro — a lacuna que a área tinha e que o cap. 05 registra. |

**O que nenhuma delas mede, e é a lacuna aberta do capítulo:** **trajetória**. Duas execuções agênticas com a mesma resposta e custos muito diferentes pontuam igual em todas as ferramentas acima.
