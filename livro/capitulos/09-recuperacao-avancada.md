# 09 — Recuperação Avançada

> **Estado da arte capturado em 2026-08** · edição 0.3 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** Componentes que aprofunda: **chunking** e **embedding**, do lado da indexação (cap. 02).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Explicar** a falha que as técnicas deste capítulo curam: o chunk que perdeu de onde veio;
2. **Comparar** *contextual retrieval* e *late chunking* pela conta, não pela fama;
3. **Decidir** entre empurrar trabalho para a indexação ou para a consulta;
4. **Aplicar** a regra de sequência: medir, uma técnica por vez, remover o que não pagou.

## O problema

Os capítulos 06 e 07 otimizam **como se busca**. Este otimiza **o que está no índice** — sem mexer no corpus (cap. 04), que já está governado, e sem mexer na pergunta (cap. 08).

A falha específica: **o chunk perdeu o contexto de onde veio.** "A margem caiu 12%" é um trecho inútil sem saber de que produto e de que trimestre. O documento sabia; o chunk não. E o índice trata o chunk como se ele se bastasse.

O sintoma é característico: a busca traz trechos que são *sobre* o assunto certo, e a resposta sai errada ou vaga porque nenhum deles diz **de quê** está falando.

E o aviso que abre o capítulo, porque é o erro mais caro daqui: **cada técnica custa**, e aplicar todas por precaução é a forma mais comum de tornar um RAG caro sem torná-lo bom.

## Fundamentos científicos

- **A comparação direta entre as duas** — [arXiv 2504.19754](https://arxiv.org/abs/2504.19754) põe *late chunking* e *contextual retrieval* lado a lado e conclui: *"**contextual retrieval preserves semantic coherence more effectively but requires greater computational resources**. In contrast, **late chunking offers higher efficiency but tends to sacrifice relevance and completeness**"*. ✓

  **Correção registrada (rodada 2).** A edição 0.2 dizia que as duas resolvem a mesma falha e que a escolha entre elas é **"aritmética, não estética"** — isto é, só uma questão de preço. A evidência corrige: **há troca de qualidade, não só de custo**. O *late chunking* é mais barato **e** entrega menos coerência. A decisão continua sendo sua, mas ela tem dois eixos, não um.
- **Corte alinhado entre documentos** — [arXiv 2601.05265](https://arxiv.org/abs/2601.05265) reconstrói o conhecimento **no nível do corpus**: identifica tópicos entre documentos e sintetiza segmentos em chunks unificados. Números com a condição: no HotpotQA (multi-hop), *faithfulness* **0,93** contra **0,83** do *contextual retrieval* e **0,78** do corte semântico (p < 0,05); em `k = 3`, mantém **0,91** enquanto os métodos semânticos caem para **0,68**. O custo de indexação é maior — e a contrapartida é exatamente a assimetria da próxima seção: chunks mais densos *"reduce query-time retrieval needs"*. ✓
- **O lugar no paradigma** — a survey de Gao ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)) nomeia esta etapa: *"To tackle the indexing issues, Advanced RAG **refines its indexing techniques** through the use of a sliding window approach, fine-grained segmentation, and the **incorporation of metadata**"*. Note o terceiro item — **metadado é listado como refinamento de indexação**, que é exatamente o argumento do cap. 04 visto daqui. O movimento de 2026 é o deslocamento do esforço de otimização para esta etapa. ✓

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **Contextual Retrieval** ([Anthropic](https://www.anthropic.com/engineering/contextual-retrieval), 2024) — antes de embeddar, prefixa-se cada chunk com **50–100 tokens** de contexto gerado por um modelo pequeno, e o mesmo prefixo entra no índice BM25. Custo declarado: **US$ 1,02 por milhão de tokens de documento**, com cache de prompt. ✓
- **Late Chunking** ([arXiv 2409.04701](https://arxiv.org/abs/2409.04701), Jina AI) — inverte a ordem: *"first embed all tokens of the long text, with chunking applied **after the transformer model and just before mean pooling**"*. Cada chunk carrega contexto dos vizinhos, e o método ***"works without additional training"*** — nenhuma chamada de LLM, nenhum treino. Resolve a mesma falha por muito menos dinheiro, limitado pelo comprimento máximo do embedder (cap. 05). ✓
- **A ressalva do Princípio I, agora com os números da fonte** — todos sobre a **taxa de falha de recuperação no top-20**, partindo de 5,7%:

  | Configuração | Taxa de falha | Redução |
  |---|:---:|:---:|
  | linha de base | 5,7% | — |
  | *Contextual Embeddings* | 3,7% | **35%** |
  | + *Contextual BM25* | 2,9% | **49%** |
  | + reranking | 1,9% | **67%** |

  O `67%` é **a pilha inteira, com reranker** — e circula em fontes secundárias como mérito da técnica sozinha. Note também o que a tabela diz ao capítulo anterior: o salto de 35% para 49% é **só por acrescentar BM25**, o que é a busca híbrida do cap. 06 aparecendo de novo, agora medida. ✓ ([caso de deriva no panorama §6.2](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md))

## O estado da arte

### 1. Duas curas, contas muito diferentes

| Técnica | O que faz | Custo de indexação | Limite |
|---|---|---|---|
| **Contextual Retrieval** | prefixa cada chunk com um resumo do seu lugar no documento, antes de embeddar | **1 chamada de LLM por chunk** | preço, em corpus grande |
| **Late Chunking** | embeda o documento inteiro, corta depois do transformer | só o modelo de embedding | comprimento máximo do embedder |

Esta tabela é a mensagem do capítulo — com a ressalva que a comparação publicada acrescenta. As duas atacam **a mesma falha**, e a diferença de conta é de ordem de grandeza; mas elas **não entregam o mesmo resultado**: o *contextual retrieval* preserva mais coerência semântica, e o *late chunking* sacrifica relevância e completude em troca de eficiência. Para corpus de milhões de chunks com orçamento apertado, a decisão pende para o barato — sabendo o que se está trocando.

O que decide entre elas:

- **Tamanho do corpus** — quantas chamadas de LLM você está disposto a pagar uma vez.
- **Tamanho dos documentos** — se eles excedem o comprimento máximo do embedder, *late chunking* não se aplica inteiro.
- **Volatilidade** — corpus que muda toda hora reprocessa sempre, e aí o custo "uma vez" vira recorrente.

### 2. A assimetria que decide muita coisa

Custo de **indexação** é pago uma vez e amortizado por todas as consultas. Custo de **consulta** (cap. 08) é pago para sempre.

| O seu caso | Empurre o trabalho para |
|---|---|
| Muitas consultas, corpus estável | **indexação** — amortiza |
| Poucas consultas, corpus volátil | **consulta** — não reprocessa nada |
| Muitas consultas, corpus volátil | o caso difícil: reindexação incremental (cap. 04) |

O terceiro caso é onde a maioria dos sistemas de empresa vive, e é o que torna a política de reindexação do cap. 04 uma decisão de arquitetura, não de manutenção.

### 3. A regra de sequência

Como este capítulo é uma lista de melhorias possíveis, a regra de **como** aplicá-las vale mais que qualquer uma delas:

1. **Meça primeiro** qual falha você tem (cap. 21). Se *context recall* está baixo, o problema é achar — e pode estar no corpus (04), na representação (05) ou na busca (06), não aqui. Se está alto e *faithfulness* está baixa, o problema é a geração (15).
2. **Aplique uma técnica por vez**, com medição antes e depois. Duas de uma vez e você não sabe qual pagou.
3. **Remova o que não pagou.** Complexidade não removida é dívida permanente — e um pipeline de cinco estágios que ninguém entende é pior que um simples que erra de forma conhecida.

O passo 3 é o que quase ninguém faz, e é o que separa um sistema que evolui de um que só acumula.

### Leitura executiva

A falha deste capítulo é uma só: **o chunk perdeu o contexto de onde veio** — "a margem caiu 12%" é inútil sem saber de que produto e trimestre. **O que roubar:** *contextual retrieval* e *late chunking* curam a **mesma** falha com contas de ordem de grandeza diferente — a primeira paga **uma chamada de LLM por chunk** sobre o corpus inteiro (US$ 1,02 por milhão de tokens de documento, com cache); a segunda usa **só o modelo de embedding**, sem treino adicional, limitada pelo comprimento máximo dele. Para corpus grande, a decisão é aritmética, não estética. **A assimetria que decide muita coisa:** indexação é paga uma vez e amortizada; consulta é paga para sempre — muitas consultas sobre corpus estável pedem indexação, corpus volátil pede o lado da pergunta, e "muitas consultas + corpus volátil" é o caso difícil que transforma reindexação incremental em decisão de arquitetura. **A regra que vale mais que as técnicas:** meça qual falha você tem antes de escolher, aplique **uma por vez** com medição dos dois lados, e **remova o que não pagou** — este último passo quase ninguém faz, e é o que separa um sistema que evolui de um que só acumula. **Sobre os números publicados:** o 67% do *contextual retrieval* é a **taxa de falha no top-20 caindo de 5,7% para 1,9% com a pilha inteira, reranker incluído** — sozinha, a técnica leva a 3,7% (35%). Cite a curva, não o número. **E a escolha entre as duas não é só de preço:** a comparação publicada mostra que o *late chunking* economiza sacrificando relevância e completude.

## Mão na massa — rag-zero, etapa 8

Na etapa 8 você aplica *contextual retrieval* a um subconjunto do corpus do `rag-zero` e mede: ganho de recall, custo de indexação em chamadas, e tempo. Depois faz o mesmo com uma aproximação de *late chunking*, e coloca as duas contas lado a lado. A etapa entrega a tabela comparativa — e o achado é que a escolha depende de números do seu corpus, não da reputação da técnica. O exercício de completude: o prompt que gera o contexto do chunk vem esqueletado; você descobre que a qualidade dele decide o ganho inteiro.

## Verificação

1. Você tem 2 milhões de chunks e orçamento apertado de indexação. Entre as duas técnicas, qual escolhe — e, dada a troca de qualidade medida, o que precisa verificar antes de aceitar a mais barata?
2. Seu corpus muda várias vezes por dia e recebe milhares de consultas. Por que esse é o caso difícil, e o que ele exige do cap. 04?
3. Você aplicou três técnicas de uma vez e o recall subiu 8 pontos. Qual é o problema com essa informação?

---

## Apêndice A — Como cada técnica avançada é implementada

**Rodada 1 (edição 0.2)**: as duas curas e a economia comparada estão descritas. O tratamento por técnica — com a condição experimental de cada número publicado, que é onde o Princípio I mais aperta neste capítulo — é o trabalho da **rodada 2** do ROADMAP.

Enfileirado: Contextual Retrieval (o corpus em que foi medido) · Late Chunking e o limite do embedder · chunking avaliado (2504.19754) · corte alinhado entre documentos (2601.05265) · indexação refinada no Advanced RAG (2312.10997).
