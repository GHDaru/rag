# 15 — Avaliação de Sistemas de Contexto

> **Estado da arte capturado em 2026-08** · edição 0.1 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** As quatro métricas e a tabela de diagnóstico estão fechadas; o tratamento por ferramenta e benchmark é a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Separar** a avaliação da recuperação da avaliação da geração — e explicar por que juntá-las impede o diagnóstico;
2. **Definir** as quatro métricas de referência e o que cada uma revela;
3. **Diagnosticar** uma falha de RAG a partir da combinação de métricas;
4. **Montar** um conjunto de avaliação com dados sintéticos sem cair no viés de avaliar o modelo com ele mesmo.

## O problema

"O RAG não está bom" é um sintoma com pelo menos quatro causas distintas — e as quatro exigem intervenções diferentes, em partes diferentes do sistema. Sem separar as medições, o time otimiza no lugar errado, com sorte por meses.

A separação mínima é entre **achar** e **usar**:

- A recuperação trouxe o que precisava? (falha aqui = caps. 09 e 10)
- A resposta usou o que foi trazido, sem inventar? (falha aqui = geração, prompt, cap. 02/04)

Um sistema pode ter recuperação excelente e resposta péssima. E — o caso que mais engana — pode ter recuperação péssima e resposta que **parece** boa, porque o modelo preencheu as lacunas com conhecimento paramétrico plausível. Este segundo caso passa em qualquer avaliação superficial e falha exatamente onde importa: no caso raro, no dado novo, no que a empresa tem de específico.

## Fundamentos científicos

- **Benchmarks de recuperação** — **BEIR** (recuperação zero-shot em domínios variados) e **MTEB** (avaliação ampla de modelos de embedding) medem o estágio isolado. São a referência para escolher modelo de embedding sem confundir com o resto do pipeline. `[a validar]`
- **Avaliação ponta a ponta** — não há benchmark único de RAG; a prática recomendada é combinar dois ou três, cobrindo estágios distintos: recuperação pura (BEIR), fidelidade da geração, e conjuntos próprios do domínio. `[a validar]`
- **Avaliação sob contexto longo** — *U-NIAH* ([arXiv 2503.00353](https://arxiv.org/abs/2503.00353)) unifica a avaliação de RAG e de contexto longo no mesmo protocolo, permitindo comparar os dois regimes em vez de discuti-los por anedota (cap. 08). `[a validar]`
- **Benchmarks de domínio** — há uma tendência de frameworks de benchmarking adaptativo por setor (por exemplo, [FAB-Bench](https://arxiv.org/abs/2605.26476), para manufatura de semicondutores), que é sintoma de um fato inconveniente: **resultado em benchmark geral não transfere para domínio específico**. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **RAGAS** — estabeleceu o vocabulário de fato da área com quatro métricas por LLM-as-judge: *faithfulness*, *answer relevance*, *context precision* e *context recall*; e suporta geração de conjunto de teste a partir do próprio corpus.
- **DeepEval** — as mesmas ideias com foco em integração de CI/CD. A leitura de 2026 é complementar, não concorrente: **RAGAS fornece o arcabouço conceitual; DeepEval, a execução em pipeline**.
- **TruLens** e a família de observabilidade — instrumentação de execução, útil para o que este livro chama de trajetória (cap. 11).
- **A prática que separa** — os times que conseguem melhorar RAG são os que têm um conjunto de avaliação **do próprio domínio**, com respostas verificadas por gente. Todo o resto é diagnóstico assistido.

## O estado da arte

### 1. As quatro métricas, e o que cada uma responde

| Métrica | Pergunta | Estágio | Falha indica |
|---|---|---|---|
| **Context recall** | os trechos necessários foram recuperados? | recuperação | índice, chunking, busca (caps. 09–10) |
| **Context precision** | os trechos recuperados eram relevantes? | recuperação | `top_k` alto, ranking fraco, orçamento desperdiçado (cap. 08) |
| **Faithfulness** | a resposta é sustentada pelo que foi recuperado? | geração | alucinação; prompt sem regra de fundamentação (cap. 02) |
| **Answer relevance** | a resposta responde à pergunta feita? | geração | o modelo respondeu outra coisa |

*Faithfulness* é a que mais importa e a mais mal compreendida. Ela é calculada decompondo a resposta em afirmações e verificando quantas são **inferíveis do contexto fornecido**. Uma resposta factualmente correta mas não sustentada pelo contexto tem *faithfulness* baixa — e isso é o comportamento desejado, não um defeito da métrica: significa que o modelo respondeu de memória, e você não tem garantia nenhuma sobre a próxima pergunta.

### 2. A tabela de diagnóstico

A combinação das métricas localiza o problema — é o instrumento que o cap. 10 pede antes de escolher técnica:

| Recall | Precision | Faithfulness | Diagnóstico | Onde agir |
|:---:|:---:|:---:|---|---|
| baixo | — | — | não acha | chunking, busca híbrida, reescrita (caps. 09, 10) |
| alto | baixo | — | acha e traz lixo junto | reranking, `top_k` menor (cap. 09) |
| alto | alto | baixo | tem tudo e inventa | prompt de fundamentação, regra de abstenção (cap. 02) |
| alto | alto | alto | e ainda erra | a pergunta exige raciocínio (cap. 03) ou multi-hop (cap. 10) |

Esta tabela é, sozinha, o motivo de o capítulo existir. Sem ela, "melhorar o RAG" é tentativa e erro caro.

### 3. Conjuntos de avaliação: de onde vêm

Três origens, em ordem crescente de valor e de custo:

- **Sintético a partir do corpus.** Gera-se perguntas a partir dos documentos. Barato, cobre volume, e tem um viés conhecido: perguntas geradas de um trecho são respondíveis por aquele trecho, o que **superestima** o recall e não testa multi-hop nem pergunta mal formulada.
- **Perguntas reais de usuários**, com resposta verificada por gente. Caro, insubstituível — é o único conjunto que contém as ambiguidades e os erros de digitação do mundo real.
- **Casos de falha registrados.** O mesmo princípio do cap. 07: todo incidente vira caso. É o conjunto que cresce sozinho e com valor.

O erro estrutural a evitar: gerar perguntas **e** julgar respostas com o mesmo modelo que gera as respostas. O sistema passa a ser avaliado pelo seu próprio viés, e o número resultante mede consistência, não qualidade.

### 4. O que a instrumentação atual não cobre

- **Trajetória.** Em RAG agêntico (cap. 11), duas execuções com a mesma resposta podem ter custos muito diferentes. Nenhuma das quatro métricas vê isso.
- **Conversa.** As métricas são por turno. A falha do cap. 13 — esquecer o combinado no turno 3 — é invisível para todas elas.
- **Custo como métrica de primeira classe.** Qualidade sem custo ao lado leva a decisões que não sobrevivem à revisão de fatura (cap. 17).
- **Deriva.** O corpus muda, o modelo muda, o padrão de pergunta muda. Sem execução periódica sobre um conjunto fixo, a degradação lenta é invisível até virar reclamação.

### Leitura executiva

"O RAG não está bom" tem pelo menos quatro causas distintas, e a separação mínima é entre **achar** e **usar**. **O que roubar:** a **tabela de diagnóstico** — recall baixo = não acha (chunking/busca); recall alto + precision baixo = traz lixo junto (reranking, `top_k` menor); recall e precision altos + faithfulness baixa = **tem tudo e inventa** (prompt de fundamentação). Sem ela, "melhorar o RAG" é tentativa e erro caro. **A métrica mais mal compreendida:** *faithfulness* baixa numa resposta **factualmente correta** não é defeito da métrica — significa que o modelo respondeu de memória, e você não tem garantia nenhuma sobre a próxima pergunta. Esse é o caso que mais engana, porque parece bom. **Sobre conjuntos:** sintético a partir do corpus é barato e **superestima o recall** (a pergunta gerada de um trecho é respondível por aquele trecho); pergunta real com resposta verificada por gente é insubstituível. **Nunca** gere as perguntas e julgue as respostas com o mesmo modelo que responde — isso mede consistência, não qualidade. **As lacunas abertas:** trajetória, conversa (não só turno), custo ao lado da qualidade, e deriva.

## Mão na massa — contexto-zero, etapa 14

Na etapa 14 você monta o eval do `contexto-zero`: 30 perguntas sobre o texto deste livro (metade sintéticas, metade escritas por você), as quatro métricas implementadas com juiz de família diferente, e a tabela de diagnóstico impressa ao final. A etapa termina com um exercício desconfortável e deliberado: rodar o eval sobre a etapa 8 (só BM25) e sobre a etapa 9 (pipeline completo) e verificar se o ganho que você **esperava** aparece. O exercício de completude: o cálculo de *faithfulness* vem esqueletado — você implementa a decomposição em afirmações e descobre onde a métrica é frágil.

## Verificação

1. *Context recall* 0,9, *context precision* 0,4, *faithfulness* 0,85. Qual é o problema, e qual o custo escondido dele? (Dica: cap. 08.)
2. Por que uma resposta correta pode — e deve — receber *faithfulness* baixa? O que isso avisa sobre o sistema?
3. Você gerou 200 perguntas sinteticamente e o recall ficou em 0,95. Cite duas razões para não comemorar.

---

## Apêndice A — Como cada ferramenta e benchmark avalia

> Tratamento por ferramenta e benchmark, com o que mede e o que não mede — complementação online, expandida a cada rodada.

**Rodada 1 (edição 0.1)**: as quatro métricas e a tabela de diagnóstico estão descritas. O tratamento por ferramenta — a definição operacional exata de cada métrica em cada implementação (elas divergem), o custo de rodar, e a integração em CI — é o trabalho da **rodada 2** do ROADMAP, e converge com o Apêndice A do cap. 07.

Enfileirado: RAGAS (definição de cada métrica) · DeepEval e execução em CI · TruLens e observabilidade · BEIR e MTEB (o que medem do estágio de recuperação) · U-NIAH (avaliação unificada dos dois regimes) · benchmarks de domínio e o que a proliferação deles revela.
