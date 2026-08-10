# 18 — RAG Agêntico

> **Estado da arte capturado em 2026-08** · edição 1.0 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** Componente que aprofunda: **orquestrador** (cap. 02). A distinção pipeline × agente e os padrões estão fechados; o tratamento por implementação é a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Distinguir** RAG como pipeline fixo de RAG como decisão do agente;
2. **Identificar** os padrões agênticos aplicados à recuperação (reflexão, planejamento, roteamento, colaboração);
3. **Avaliar** o custo real da autonomia: latência, tokens, imprevisibilidade e superfície de ataque;
4. **Definir** os limites que tornam um laço de recuperação seguro e terminável.

## O problema

Nos caps. 06 a 10, a recuperação é um **pipeline**: chega a pergunta, busca-se, monta-se o contexto, gera-se. O caminho é sempre o mesmo, mesmo quando a pergunta não pede busca nenhuma, mesmo quando a primeira busca voltou vazia, mesmo quando a resposta exigiria três buscas encadeadas.

RAG agêntico inverte o controle: o modelo **decide** se busca, o que busca, onde busca, e se o que voltou basta. A recuperação deixa de ser etapa e vira **ferramenta** — uma tool com schema (cap. 13), exposta ao modelo junto das outras.

O ganho é claro — o sistema passa a lidar com perguntas que nenhum pipeline fixo atende. O custo é o que este capítulo insiste em cobrar: um sistema que decide é um sistema cujo custo, latência e comportamento você não conhece de antemão.

## Fundamentos científicos

- **A formalização** — *Agentic RAG: A Survey* ([arXiv 2501.09136](https://arxiv.org/abs/2501.09136)) sistematiza a área e nomeia a limitação que justifica o capítulo: sistemas tradicionais de RAG são *"constrained by **static workflows** and lack the adaptability required for multi-step reasoning"*. Os quatro padrões de projeto que ele lista são exatamente os do capítulo — *"reflection, planning, tool use, and multi-agent collaboration"* — usados para *"**dynamically manage retrieval strategies**"*. ✓
- **ReAct** ([arXiv 2210.03629](https://arxiv.org/abs/2210.03629)) — intercalar raciocínio e ação, com a ação servindo para *"interface with external sources, such as knowledge bases"*. Quando a ação é buscar, ReAct **é** RAG agêntico na sua forma mínima. Mesma técnica do cap. 12, agora como arquitetura. ✓
- **Raciocínio predefinido × agêntico** — [arXiv 2506.10408](https://arxiv.org/abs/2506.10408) separa a área em dois sistemas, e a distinção é a linha que este capítulo atravessa: ***predefined reasoning***, que *"follows fixed modular pipelines"*, e ***agentic reasoning***, em que *"the model **autonomously orchestrates** tool interaction during inference"*. Os caps. 06–10 são o primeiro; este é o segundo. ✓
- **Grafo + agente** — a convergência das duas linhas: o agente navega uma estrutura de grafo em vez de receber trechos ([arXiv 2509.22009](https://arxiv.org/abs/2509.22009)). A distinção que a literatura marca: GraphRAG muda **do que** se recupera; RAG agêntico muda **como**. `[a validar]`
- **Os problemas abertos** — os surveys da área convergem na lista: avaliação, coordenação, gestão de memória, eficiência e governança. Nenhum deles é resolvido; todos aparecem em produção. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **Recuperação como ferramenta** — na prática dominante, "buscar" vira uma tool com schema (cap. 13), exposta ao modelo junto das outras. Isso subordina o capítulo inteiro às regras do cap. 20 (o resultado ocupa orçamento) e do cap. 22 (o que voltou é conteúdo não confiável).
- **A pressão que veio dos agentes** — o movimento que mais forçou a evolução do RAG em 2026 foi a ascensão de agentes que executam processos de vários passos: eles planejam, executam e iteram, e um pipeline de recuperação de passo único não os serve.
- **Recuperação just-in-time** — a prática dos agentes de código: em vez de pré-carregar contexto, dar ao modelo as ferramentas para buscar quando precisar. Economiza orçamento e transfere a decisão para o momento em que há mais informação sobre ela.

## O estado da arte

### 1. O espectro, não a dicotomia

Entre pipeline fixo e agente autônomo há graus, e escolher o grau certo é a decisão de projeto:

| Grau | Quem decide | Ganho | Custo |
|---|---|---|---|
| **Pipeline fixo** | ninguém, é sempre igual | previsível, barato | falha fora da classe prevista |
| **Roteamento** | um classificador escolhe a fonte/estratégia | cobre múltiplos corpora | erro de roteamento é silencioso |
| **Recuperação sob demanda** | o modelo decide *se* busca | não paga busca quando não precisa | o modelo pode decidir errado |
| **Laço com reflexão** | o modelo avalia o resultado e busca de novo | atende multi-hop e busca vazia | latência e custo variáveis |
| **Multiagente** | agentes especializados por fonte | cobre domínios heterogêneos | coordenação, e falha difícil de depurar |

A recomendação honesta: **suba um grau por vez, e só com evidência de que o grau anterior falha.** A maior parte dos sistemas que adotaram multiagente por design teria sido melhor servida por roteamento com reflexão — que é depurável.

### 2. Os quatro padrões

- **Reflexão** — o agente critica o resultado da busca antes de usá-lo ("isto responde à pergunta? falta algo?") e decide buscar de novo. É o padrão de maior retorno e o mais barato de implementar; resolve o caso da busca vazia e o do resultado parcial.
- **Planejamento** — decompor a pergunta em subperguntas antes de buscar, e buscar cada uma. É a resposta natural ao multi-hop do cap. 10.
- **Roteamento** — escolher a fonte certa entre várias (documentação, banco, API, web) antes de buscar. É frequentemente o que o sistema realmente precisava quando alguém propôs "agente".
- **Colaboração** — agentes especializados por fonte ou por etapa, coordenados. É o padrão mais caro e o mais difícil de avaliar; exige justificativa explícita.

As quatro materializações nomeadas que a literatura consolidou — vale conhecer para não reinventar:

| Nome | O que faz | Padrão |
|---|---|---|
| **Self-RAG** | o modelo emite marcadores de reflexão que decidem *se* recupera e *se* o trecho sustenta a resposta | reflexão, treinada no modelo |
| **CRAG** (*Corrective RAG*) | um avaliador leve classifica o resultado (correto / ambíguo / errado) e dispara ação corretiva — refinar ou buscar em outra fonte | reflexão, com avaliador externo |
| **FLARE** | recupera **durante** a geração, quando o modelo fica incerto sobre o que vai escrever a seguir | reflexão, disparada por incerteza |
| **Adaptive RAG** | classifica a complexidade da pergunta e escolhe o grau — resposta direta, uma busca, ou laço | roteamento por complexidade |

A diferença entre elas é **onde mora o julgamento**: dentro do modelo (Self-RAG), num avaliador separado (CRAG), no sinal de incerteza da geração (FLARE), ou num classificador de entrada (Adaptive RAG). A última é a mais fácil de operar e depurar, e por isso costuma ser a primeira a tentar.

### 3. O custo da autonomia

Quatro custos que a literatura de entusiasmo omite:

- **Latência não determinística.** Um sistema que pode buscar 1 ou 5 vezes tem cauda de latência larga. Interfaces síncronas sofrem; contratos de SLA quebram.
- **Custo por pergunta imprevisível.** O orçamento do cap. 20 deixa de ser estático. É necessário um teto **por requisição**, não só por chamada.
- **Avaliação mais difícil.** Não se avalia mais uma resposta: avalia-se uma trajetória. Duas trajetórias diferentes podem chegar à mesma resposta certa, e uma delas custar 5×. O cap. 21 mede a resposta; a trajetória precisa de instrumentação própria.
- **Superfície de ataque maior.** Cada ida ao mundo externo traz conteúdo que pode conter instrução. Um agente que busca, lê e decide buscar de novo com base no que leu é, por construção, um alvo de *prompt injection* encadeada (cap. 22).

### 4. Os limites que tornam o laço seguro

Um laço de recuperação em produção precisa, sem exceção, de:

- **Teto de iterações** e comportamento definido ao atingi-lo (responder com o que tem e dizer que é parcial — nunca falhar em silêncio).
- **Teto de orçamento por requisição**, em tokens e em tempo, com corte determinístico.
- **Detecção de laço improdutivo** — a mesma consulta repetida, ou consultas que não trazem nada novo, precisam encerrar o ciclo.
- **Trajetória observável** — cada decisão de busca registrada com consulta, resultado e motivo. Sem isso, depurar é impossível e a conta é inexplicável.

### Leitura executiva

RAG agêntico inverte o controle: o modelo decide **se, o que e onde** buscar, e a recuperação deixa de ser etapa e vira **ferramenta**. Não é dicotomia, é **espectro** — pipeline fixo → roteamento → busca sob demanda → laço com reflexão → multiagente. **O que roubar:** suba **um grau por vez**, e só com evidência de que o anterior falha; e comece pela **reflexão** (criticar o resultado antes de usá-lo), que é o padrão mais barato e de maior retorno. As materializações nomeadas diferem por **onde mora o julgamento** — dentro do modelo (Self-RAG), num avaliador separado (CRAG), no sinal de incerteza da geração (FLARE) ou num classificador de entrada (Adaptive RAG); a última é a mais fácil de operar e depurar. Muito sistema que adotou multiagente por design precisava só de **roteamento** — que é depurável. **O custo que o entusiasmo omite:** latência de cauda larga, custo por pergunta imprevisível, avaliação de **trajetória** (e não de resposta), e superfície de *prompt injection* encadeada. **Inegociável em produção:** teto de iterações, teto de orçamento por requisição, detecção de laço improdutivo e trajetória observável — sem os quatro, o laço é um risco com aparência de recurso.

## Mão na massa — rag-zero, etapa 11

Na etapa 11 a recuperação do `rag-zero` vira ferramenta: o modelo passa a decidir se busca, com reflexão sobre o resultado e um teto de 3 iterações. A etapa entrega dois números lado a lado — o custo médio por pergunta antes e depois — porque o conteúdo pedagógico aqui é justamente que autonomia tem preço. O exercício de completude: a detecção de laço improdutivo vem esqueletada; você define o critério de "não trouxe nada novo" e descobre que ele é mais sutil do que parece.

## Verificação

1. Seu sistema tem três fontes (documentação, base de tickets, banco de produtos) e o RAG atual busca nas três sempre. Que grau do espectro resolve, e o que ele custa?
2. Duas execuções chegam à mesma resposta correta; uma fez 1 busca, outra fez 4. O eval do cap. 21 dá nota igual às duas. O que está faltando medir?
3. Por que um laço de recuperação sem detecção de repetição pode custar caro **mesmo com** teto de iterações?

---

## Apêndice A — Como cada implementação trata o RAG agêntico

> Tratamento por implementação, com URL. Todos os quatro papers da §2 têm código publicado pelos autores — o que é incomum, e vale registrar.

| Padrão | Implementação de referência | O que reter |
|---|---|---|
| **Self-RAG** | [AkariAsai/self-rag](https://github.com/AkariAsai/self-rag) | **Pegadinha decisiva:** o método **treina** o modelo a emitir *reflection tokens*. Não é prompt — se você não vai treinar nem usar um modelo já treinado assim, o padrão não está disponível para você. |
| **CRAG** | [HuskyInSalt/CRAG](https://github.com/HuskyInSalt/CRAG) | avaliador leve **fora** do modelo, devolvendo grau de confiança. É *"plug-and-play"* — acopla a um pipeline existente, o que o torna a escolha pragmática quando não se pode treinar. |
| **FLARE** | [jzbjyb/FLARE](https://github.com/jzbjyb/FLARE) | recupera durante a geração, disparado por tokens de baixa confiança. **Pegadinha:** o número de recuperações por resposta é **imprevisível**, o que quebra orçamento (cap. 20) e latência p99. |
| **Adaptive RAG** | [starsuzi/Adaptive-RAG](https://github.com/starsuzi/Adaptive-RAG) | classificador pequeno decide o grau. **Pegadinha:** o classificador é treinado com rótulos derivados dos resultados dos próprios modelos — trocar o gerador desalinha o roteador. |
| **ReAct como base** | o padrão está em todos os frameworks de agente | é o RAG agêntico mínimo, e o único que não exige nada além de prompt e uma ferramenta de busca. |

**O que nenhuma delas entrega, e você precisa colocar:** teto de iterações, orçamento de tokens por laço, e instrumentação de **trajetória** (cap. 21). Sem os três, o laço é um incidente esperando data.
