# 08 — Entendimento da Consulta

> **Estado da arte capturado em 2026-08** · edição 1.0 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** Componente que aprofunda: **entendimento da consulta** (cap. 02).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Diagnosticar** quando o problema está na pergunta, e não no índice;
2. **Escolher** entre reescrita, expansão, decomposição, HyDE e step-back pelo que cada uma corrige;
3. **Resolver** referências entre turnos — a falha mais comum e menos tratada em RAG conversacional;
4. **Avaliar** o custo destas técnicas, que é pago **em toda pergunta**.

## O problema

Os capítulos anteriores trabalharam o lado do índice. Este trabalha o lado da pergunta — e é frequentemente onde está o ganho mais barato.

O usuário não escreve consultas: escreve perguntas. E entre a pergunta e o documento há distâncias que nenhum reranking fecha:

- **Vocabulário.** O usuário pergunta "por que meu pedido não chegou?"; o documento diz "SLA de entrega em regiões remotas". Zero termos em comum, e a distância semântica é maior do que parece.
- **Referência.** "E no ano passado?" não é uma consulta buscável. Sozinha, ela não significa nada — e é assim que metade das perguntas de uma conversa chega ao retriever.
- **Composição.** "Compare a política de férias com a de licença" são duas buscas, não uma.
- **Nível.** "Posso cancelar depois de 30 dias?" às vezes precisa do princípio geral (a política de cancelamento), não do trecho específico.

Melhorar o índice para curar isso é caro e demorado. Melhorar a consulta é uma chamada de modelo — mas paga **em toda pergunta**, para sempre.

## Fundamentos científicos

- **HyDE** ([arXiv 2212.10496](https://arxiv.org/abs/2212.10496)) — gerar um documento hipotético que responda à pergunta e buscar por **ele**, porque uma resposta se parece mais com o documento do que a pergunta se parece. O documento gerado *"captures relevance patterns but is unreal and may contain false details"*, e é o gargalo denso do encoder que filtra o que foi inventado. **A condição experimental muda a recomendação:** foi proposto para o cenário **zero-shot, sem rótulo de relevância**, comparado a um retriever denso não supervisionado. Se você já tem híbrido bom (cap. 06), o caso a favor do HyDE é bem mais fraco do que a fama sugere. ✓
- **Step-back prompting** ([arXiv 2310.06117](https://arxiv.org/abs/2310.06117)) — generalizar a pergunta antes de recuperar, para trazer o princípio e não só o detalhe. É o inverso da decomposição: sobe um nível em vez de descer. **Ressalva de procedência:** o paper propõe uma técnica de **raciocínio** (abstrair para primeiros princípios), medida em STEM e QA — PaLM-2L com MMLU Física +7%, Química +11%, TimeQA +27%, MuSiQue +7%. Usá-la como **etapa de recuperação** é leitura derivada da prática, não do paper — e *The Prompt Report* corrobora, classificando-a sob *thought generation*, junto do CoT. ✓
- **Reescrita em múltiplos turnos** — trabalho aplicado combina reescrita de consulta e recuperação híbrida para RAG conversacional ([arXiv 2606.28352](https://arxiv.org/abs/2606.28352)) — a falha de referência no cenário mais difícil. É um **paper de sistema de competição** (SemEval-2026, tarefa 8), não um método geral: serve de indício de prática, não de evidência de superioridade. `[a validar]`
- **O lugar no paradigma** — na taxonomia de Gao ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)), estas são as técnicas de **pré-recuperação** do Advanced RAG. Junto com busca híbrida e reranking, formam os três acréscimos que definem o degrau (cap. 03). `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **A ordem de tentativa** que os praticantes convergem: reescrita primeiro, sempre. É a mais barata e resolve o caso mais comum.
- **O custo estrutural** — toda técnica deste capítulo acrescenta uma chamada **antes** de buscar, no caminho crítico. Em interfaces síncronas isso aparece direto na latência percebida.
- **O ganho invisível nos benchmarks** — conjuntos de avaliação sintéticos (cap. 21) têm perguntas bem formuladas e autocontidas. Eles **subestimam sistematicamente** o valor deste capítulo, porque não contêm as ambiguidades e referências do mundo real.

## O estado da arte

### 1. As cinco técnicas, por falha que corrigem

| Técnica | Corrige | Custo | Risco |
|---|---|---|---|
| **Reescrita** | vocabulário; referência entre turnos | 1 chamada | reescrever mudando a intenção |
| **Expansão / múltiplas consultas** | pergunta composta; cobertura | 1 chamada + N buscas | diluir o foco |
| **HyDE** | distância grande pergunta↔documento | 1 chamada | alucinar hipótese fora do domínio |
| **Step-back** | falta o princípio, não o detalhe | 1 chamada | trazer o genérico quando o específico bastava |
| **Roteamento** | fonte errada | 1 classificação | erro silencioso de rota |

As cinco atacam problemas diferentes, e a escolha é empírica. O que **não** é empírico é a ordem: **reescrita primeiro**, porque é a mais barata e cobre o caso mais frequente.

### 2. Resolução de referência: a falha esquecida

Merece seção própria por ser a mais comum em sistemas conversacionais e a menos tratada.

Numa conversa, boa parte das perguntas é **incompleta por construção**: "e o segundo caso?", "por que não?", "e no ano passado?". Enviadas cruas ao retriever, elas recuperam ruído — e o sintoma no usuário é "o assistente ficou burro depois de algumas perguntas".

A cura é **reescrever a pergunta para uma forma autocontida antes de buscar**, usando os turnos anteriores. "E no ano passado?" vira "Qual foi o faturamento da região Sul em 2025?".

Três detalhes que decidem se funciona:

- **Reescreva para buscar, não para responder.** A consulta autocontida serve ao retriever; o modelo continua vendo a pergunta original.
- **A reescrita é um ponto de falha silencioso.** Se ela erra a intenção, todo o resto erra junto, e o log da busca mostra uma consulta plausível. Registre a consulta reescrita na trajetória (cap. 18) — sem isso, o debug é impossível.
- **Nem toda pergunta precisa.** Detectar dependência do contexto antes de gastar a chamada é otimização simples e efetiva.

### 3. O custo é de consulta, e isso muda tudo

A assimetria do cap. 02 se aplica com força aqui: as técnicas deste capítulo são pagas **em toda pergunta, para sempre** — diferente das do cap. 09, pagas uma vez na indexação.

A consequência prática:

- Em sistemas com **muitas consultas sobre corpus estável**, prefira empurrar o trabalho para a indexação — é mais barato no acumulado.
- Em sistemas com **corpus volátil ou consultas esporádicas**, o lado da pergunta é a escolha certa, porque não exige reprocessar nada.
- Em qualquer caso, **medir antes**: por serem baratas de implementar, estas técnicas são adotadas sem verificação com frequência maior que a média.

### Leitura executiva

Melhorar o índice é caro e demorado; melhorar a **pergunta** costuma ser onde está o ganho mais rápido — e é a metade que quase todo pipeline ignora. Cinco técnicas, por falha que corrigem: **reescrita** (vocabulário e referência), **expansão** (pergunta composta), **HyDE** (distância grande pergunta↔documento), **step-back** (falta o princípio, não o detalhe), **roteamento** (fonte errada). **O que roubar:** a ordem de tentativa não é empírica — **reescrita primeiro, sempre**, por ser a mais barata e cobrir o caso mais frequente. **A falha esquecida:** em conversa, boa parte das perguntas é incompleta por construção ("e no ano passado?") e recupera ruído; reescreva para uma forma **autocontida antes de buscar** — mas reescreva *para buscar*, mantendo a pergunta original para responder, e **registre a consulta reescrita na trajetória**, porque ela é um ponto de falha silencioso que produz logs plausíveis. **A economia:** este custo é pago em **toda** pergunta, para sempre — ao contrário do cap. 09, pago uma vez. Corpus estável com muitas consultas pede indexação; corpus volátil pede o lado da pergunta. **E cuidado com o eval:** conjuntos sintéticos têm perguntas bem formuladas e **subestimam sistematicamente** o valor deste capítulo.

## Mão na massa — rag-zero, etapa 7

Na etapa 7 você acrescenta ao `rag-zero` a reescrita de consulta com resolução de referência, e valida com um conjunto de perguntas encadeadas ("o que é chunking?" → "e quando ele falha?" → "e no caso de PDF?"). O teste da etapa compara recall com e sem reescrita **apenas nas perguntas dependentes** — que é onde o ganho está e onde o eval sintético não olha. O exercício de completude: o detector de "esta pergunta depende do contexto" vem esqueletado; você define o critério e mede quanto ele economiza.

## Verificação

1. Seu RAG funciona bem na primeira pergunta e degrada a partir da terceira. Qual técnica deste capítulo é a primeira suspeita, e por quê?
2. Por que a reescrita deve alimentar o retriever, mas não substituir a pergunta original na geração?
3. Seu conjunto de avaliação é 100% sintético e mostra ganho zero com reescrita. Que hipótese você levanta antes de descartar a técnica?

---

## Apêndice A — Como cada abordagem trata a consulta

> Tratamento por implementação, com URL.

| Técnica | Implementação de referência | O que reter |
|---|---|---|
| **HyDE** | [texttron/hyde](https://github.com/texttron/hyde) (dos autores); `HyDEQueryTransform` no LlamaIndex | **Pegadinha:** o paper mede contra retriever **não supervisionado**, em cenário sem rótulo de relevância. Contra um híbrido bem ajustado, o ganho encolhe — e você paga uma chamada de LLM por pergunta, para sempre. |
| **Múltiplas consultas** | `MultiQueryRetriever` (LangChain), `SubQuestionQueryEngine` (LlamaIndex) | **Pegadinha:** N consultas geram N listas, e sem fusão por posição (cap. 06) você só multiplicou o custo. |
| **Reescrita / resolução de referência** | reescrita condicionada ao histórico, antes do retriever | é o caso de maior retorno em RAG conversacional (cap. 19). **Pegadinha:** reescrever cedo demais destrói a pergunta original — guarde as duas e busque com ambas quando houver dúvida. |
| **Step-back** | prompt, sem biblioteca dedicada | **Pegadinha de procedência:** é técnica de *thought generation* (assim classificada em *The Prompt Report*), não de recuperação. Usá-la aqui é adaptação; meça antes de adotar. |
| **Roteamento** | `RouterQueryEngine` (LlamaIndex), roteadores semânticos e por metadado | a survey de Gao descreve as duas famílias — por **metadado** (estreita o escopo) e **semântica** — e nota que o **híbrido das duas** é possível. É o que a prática de empresa faz. |

**A regra que atravessa a tabela:** tudo aqui é custo de **consulta**, pago para sempre. O cap. 09 mostra a alternativa — empurrar para a indexação, onde se paga uma vez.
